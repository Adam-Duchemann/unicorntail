```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  const coupon = await db.query(
    `UPDATE coupons 
     SET used_by = $1, used_at = NOW() 
     WHERE code = $2 AND used_by IS NULL 
     RETURNING amount`,
    [req.user.id, code]
  );
  
  if (!coupon.rows.length) {
    return res.status(404).json({ error: 'Coupon not found or already used' });
  }
  
  const { amount } = coupon.rows[0];
  
  await db.query(
    'UPDATE users SET balance = balance + $1 WHERE id = $2',
    [amount, req.user.id]
  );
  
  res.json({ success: true, amount });
});
```

The UPDATE with `used_by IS NULL` check prevents double-redeem atomically—only one request can mark a coupon as used. Then it credits the balance. Done.
