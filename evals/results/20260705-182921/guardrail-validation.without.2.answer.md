```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }

  try {
    const coupon = await db.query('SELECT amount FROM coupons WHERE code = $1', [code]);
    
    if (coupon.rows.length === 0) {
      return res.status(404).json({ error: 'Coupon not found' });
    }

    const { amount } = coupon.rows[0];
    
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );

    res.json({ success: true, amount });
  } catch (err) {
    res.status(500).json({ error: 'Failed to redeem coupon' });
  }
});
```

Validates the code, looks it up, credits the amount, returns the result. No fluff.
