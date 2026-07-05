```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }

  try {
    const { rows } = await db.query(
      'UPDATE coupons SET redeemed_at = NOW() WHERE code = $1 AND redeemed_at IS NULL RETURNING amount',
      [code]
    );

    if (!rows.length) {
      return res.status(404).json({ error: 'Coupon not found or already redeemed' });
    }

    const amount = rows[0].amount;
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );

    res.json({ success: true, creditedAmount: amount });
  } catch (err) {
    console.error('Coupon redemption error:', err);
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

The `UPDATE...RETURNING` atomically marks the coupon as redeemed and gets its amount in one operation — prevents double-redeem races. Input is validated at the boundary, and errors are handled for both missing coupons and failures.
