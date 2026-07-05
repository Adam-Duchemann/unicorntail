```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  try {
    const coupon = await db.query(
      'UPDATE coupons SET used_at = NOW() WHERE code = $1 AND used_at IS NULL RETURNING amount',
      [code]
    );
    
    if (coupon.rows.length === 0) {
      return res.status(404).json({ error: 'Invalid or already used coupon' });
    }
    
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [coupon.rows[0].amount, req.user.id]
    );
    
    res.json({ success: true, amount: coupon.rows[0].amount });
  } catch (error) {
    res.status(500).json({ error: 'Failed to redeem coupon' });
  }
});
```

The atomic coupon update (mark used + get amount in one statement) prevents double-redemption. If the coupon doesn't exist or is already used, the query returns zero rows.
