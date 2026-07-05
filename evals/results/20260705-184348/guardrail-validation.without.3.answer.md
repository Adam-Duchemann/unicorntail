Here's the minimal endpoint:

```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  try {
    const coupon = await db.query('SELECT amount FROM coupons WHERE code = $1', [code]);
    
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

If you want to prevent double-redemption, add a `redeemed_at` timestamp to coupons and check/update it in the same transaction.
