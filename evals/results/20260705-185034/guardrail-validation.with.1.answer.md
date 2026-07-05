```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const coupon = await db.query(
    'UPDATE coupons SET used_at = NOW(), redeemed_by = $1 WHERE code = $2 AND used_at IS NULL RETURNING amount',
    [req.user.id, req.body.code]
  );
  
  if (!coupon.rows[0]) return res.status(404).json({ error: 'Invalid coupon' });
  
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [coupon.rows[0].amount, req.user.id]);
  
  res.json({ amount: coupon.rows[0].amount });
});
```

The atomic `WHERE used_at IS NULL` prevents double-redemption—once a coupon is redeemed, `used_at` is set, so subsequent attempts against that code fail the update condition.
