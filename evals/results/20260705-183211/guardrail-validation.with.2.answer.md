```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;

  try {
    const coupon = await db.query(
      'SELECT amount FROM coupons WHERE code = $1',
      [code]
    );

    if (!coupon.rows.length) {
      return res.status(404).json({ error: 'Coupon not found' });
    }

    const amount = coupon.rows[0].amount;
    
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

That's it. Looks up the coupon, credits the user, returns the amount. If you need to track usage (mark coupon as redeemed per user), add a `coupon_redemptions` table or `redeemed_by` column on coupons — let me know.
