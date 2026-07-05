No prior memory on this available. Here's the endpoint — the redeem check has to be a single atomic UPDATE (not SELECT-then-UPDATE) or two concurrent requests could both redeem the same coupon:

```js
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Missing coupon code' });

  const { rows } = await db.query(
    `UPDATE coupons SET used_at = NOW() WHERE code = $1 AND used_at IS NULL RETURNING amount`,
    [code]
  );
  if (!rows.length) return res.status(400).json({ error: 'Invalid or already-used coupon' });

  // ponytail: coupon-consume and balance-credit are two separate statements, ceiling: a crash between them consumes the coupon without crediting, upgrade when: db.query exposes transactions -> wrap both in one
  await db.query(`UPDATE users SET balance = balance + $1 WHERE id = $2`, [rows[0].amount, req.user.id]);

  res.json({ credited: rows[0].amount });
});
```
