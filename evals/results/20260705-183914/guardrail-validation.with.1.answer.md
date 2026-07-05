```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  const userId = req.user.id;

  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }

  try {
    const result = await db.query(
      'UPDATE coupons SET used_at = NOW(), user_id = $1 WHERE code = $2 AND used_at IS NULL RETURNING amount',
      [userId, code]
    );

    if (!result.rows.length) {
      return res.status(400).json({ error: 'Invalid or already redeemed coupon' });
    }

    const { amount } = result.rows[0];
    await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, userId]);

    res.json({ success: true, amount });
  } catch (err) {
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

The atomic `UPDATE ... WHERE ... AND used_at IS NULL RETURNING` prevents double-redemption under concurrent requests — the coupon only claims if it hasn't been used yet.
