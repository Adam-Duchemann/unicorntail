No prior memory on this. Writing the endpoint as a single atomic query so a coupon can't be double-redeemed under concurrency:

```js
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (typeof code !== 'string' || !code) {
    return res.status(400).json({ error: 'code is required' });
  }

  // one atomic statement: claim the coupon (if unused) and credit it in the same step,
  // so concurrent redeems of the same code can't both succeed
  const { rows } = await db.query(
    `WITH claimed AS (
       UPDATE coupons SET used_at = now()
       WHERE code = $1 AND used_at IS NULL
       RETURNING amount
     )
     UPDATE users SET balance = balance + claimed.amount
     FROM claimed
     WHERE users.id = $2
     RETURNING users.balance`,
    [code, req.user.id]
  );

  if (rows.length === 0) {
    return res.status(400).json({ error: 'invalid or already-used coupon' });
  }

  res.json({ balance: rows[0].balance });
});
```

Assumes `coupons` has `amount` and `used_at` columns, and `users` has `balance`. Adjust column names if yours differ.
