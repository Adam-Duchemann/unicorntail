Assumes Postgres (`coupons(code, amount, redeemed_at)`, `users(id, balance)`) so the redeem + credit happens in one atomic statement — no double-redeem race:

```js
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'code is required' });

  const { rows } = await db.query(
    `WITH redeemed AS (
       UPDATE coupons SET redeemed_at = now()
       WHERE code = $2 AND redeemed_at IS NULL
       RETURNING amount
     )
     UPDATE users SET balance = balance + (SELECT amount FROM redeemed)
     WHERE id = $1 AND EXISTS (SELECT 1 FROM redeemed)
     RETURNING balance`,
    [req.user.id, code]
  );

  if (rows.length === 0) {
    return res.status(400).json({ error: 'invalid or already redeemed coupon' });
  }

  res.json({ balance: rows[0].balance });
});
```
