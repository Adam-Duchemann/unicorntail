```js
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'code is required' });

  const { rows } = await db.query(
    `UPDATE coupons SET redeemed_at = NOW() WHERE code = $1 AND redeemed_at IS NULL RETURNING amount`,
    [code]
  );
  if (rows.length === 0) {
    return res.status(404).json({ error: 'invalid or already redeemed coupon' });
  }

  await db.query(`UPDATE users SET balance = balance + $1 WHERE id = $2`, [rows[0].amount, req.user.id]);
  res.json({ credited: rows[0].amount });
});
```

Redemption is a single conditional `UPDATE ... WHERE redeemed_at IS NULL RETURNING`, so a coupon can't be double-redeemed under concurrent requests — no separate lookup step to race.
