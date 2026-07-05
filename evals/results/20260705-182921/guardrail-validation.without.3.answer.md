```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  const coupon = await db.query(
    'SELECT id, amount FROM coupons WHERE code = $1',
    [code]
  );
  
  if (!coupon.rows.length) {
    return res.status(404).json({ error: 'Coupon not found' });
  }
  
  const { id: couponId, amount } = coupon.rows[0];
  
  await db.query(
    'UPDATE users SET balance = balance + $1 WHERE id = $2',
    [amount, req.user.id]
  );
  
  await db.query(
    'INSERT INTO coupon_redemptions (user_id, coupon_id) VALUES ($1, $2)',
    [req.user.id, couponId]
  );
  
  res.json({ success: true, amount });
});
```

This looks up the coupon, credits the user's balance, and tracks the redemption in a join table. If you want to prevent double-redemption, add a check for `coupon_redemptions` before the update, or add a unique constraint to the table.
