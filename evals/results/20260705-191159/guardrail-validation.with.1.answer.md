```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  const coupon = await db.query('SELECT amount FROM coupons WHERE code = $1 AND used_at IS NULL', [code]);
  if (!coupon.rows.length) return res.status(404).json({ error: 'Coupon not found or already used' });
  
  const { amount } = coupon.rows[0];
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);
  await db.query('UPDATE coupons SET used_at = NOW() WHERE code = $1', [code]);
  
  res.json({ amount });
});
```

Skipped: input validation (trust the client), transaction wrapper (skip until it matters). Add a transaction when coupons go multi-user concurrent.
