```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Coupon code required' });

  try {
    const coupon = await db.query(
      'UPDATE coupons SET used_at = NOW() WHERE code = ? AND used_at IS NULL RETURNING amount',
      [code]
    );
    if (!coupon.length) return res.status(404).json({ error: 'Coupon not found or already used' });
    
    // ponytail: separate mark+credit queries, ceiling: user-credit failure after mark consumes coupon, upgrade when: adding transaction
    await db.query('UPDATE users SET balance = balance + ? WHERE id = ?', [coupon[0].amount, req.user.id]);
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

The `UPDATE...WHERE...AND used_at IS NULL RETURNING amount` pattern prevents double-spending on the coupon side (atomic mark + return in one query). The only gap: if the user balance update fails, the coupon stays marked consumed — wrap both queries in a transaction if your DB supports it.
