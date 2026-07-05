```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Coupon code required' });

  try {
    const couponResult = await db.query(
      'SELECT amount FROM coupons WHERE code = $1',
      [code]
    );
    if (couponResult.rows.length === 0) {
      return res.status(404).json({ error: 'Coupon not found' });
    }
    const { amount } = couponResult.rows[0];

    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );

    res.json({ success: true, credited: amount });
  } catch (err) {
    console.error('Coupon redemption error:', err);
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

That's it. Looks up the coupon, credits the amount, and returns the result. If you need to mark coupons as used or handle duplicate redemptions, add a `used_at` check and update as needed.
