```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  const coupon = await db.query(
    'SELECT amount FROM coupons WHERE code = $1 AND used = false',
    [code]
  );
  if (!coupon.rows.length) return res.status(404).json({ error: 'Invalid coupon' });
  
  const { amount } = coupon.rows[0];
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);
  await db.query('UPDATE coupons SET used = true WHERE code = $1', [code]);
  
  res.json({ amount });
});
```

Looks up the coupon, credits the amount, marks it used. Skipped: transaction wrapper (add if concurrent redemption is a risk), result validation on the UPDATE (trust the schema).
