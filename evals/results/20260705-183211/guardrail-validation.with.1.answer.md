```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }

  try {
    const coupon = await db.query(
      'SELECT amount FROM coupons WHERE code = $1',
      [code]
    );

    if (!coupon.rows.length) {
      return res.status(404).json({ error: 'Coupon not found' });
    }

    const { amount } = coupon.rows[0];

    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );

    res.json({ success: true, credited: amount });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

Fetches the coupon, validates it exists, credits the amount to the user's balance, done. No transaction wrapper since you said minimal — add one if coupons need "used" tracking or concurrency guards.
