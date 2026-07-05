One atomic query does the redeem-and-credit in a single round trip, closing the double-redeem race without a manual transaction:

```js
app.post('/api/coupons/redeem', async (req, res, next) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'code is required' });

  try {
    const { rows } = await db.query(
      `WITH redeemed AS (
         UPDATE coupons SET used_at = now()
         WHERE code = $1 AND used_at IS NULL
         RETURNING amount
       )
       UPDATE users SET balance = balance + (SELECT amount FROM redeemed)
       WHERE id = $2 AND EXISTS (SELECT 1 FROM redeemed)
       RETURNING balance`,
      [code, req.user.id]
    );

    if (!rows.length) return res.status(400).json({ error: 'invalid or already redeemed coupon' });

    res.json({ balance: rows[0].balance });
  } catch (err) {
    next(err);
  }
});
```

Assumes `coupons(code, amount, used_at)` and `users(id, balance)`. The CTE marks the coupon used and credits the balance in one statement — a plain SELECT-then-UPDATE would let two concurrent requests both pass the "is it used" check and double-credit.
