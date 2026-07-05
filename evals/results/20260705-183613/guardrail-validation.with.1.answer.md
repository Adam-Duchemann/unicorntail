```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const coupon = await db.query('SELECT amount FROM coupons WHERE code = $1', [req.body.code]);
  if (!coupon.rows.length) return res.status(404).json({ error: 'Coupon not found' });
  
  const amount = coupon.rows[0].amount;
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);
  
  res.json({ credited: amount });
});
```
