```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Code required' });

  try {
    const coupon = await db.query(
      `UPDATE coupons SET used_at = NOW() 
       WHERE code = $1 AND used_at IS NULL 
       RETURNING amount`,
      [code]
    );
    
    if (!coupon.rows.length) {
      return res.status(400).json({ error: 'Invalid or already used coupon' });
    }

    const user = await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2 RETURNING balance',
      [coupon.rows[0].amount, req.user.id]
    );

    res.json({ balance: user.rows[0].balance });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

The first `UPDATE` atomically marks the coupon used and returns its amount in one query (prevents double-redemption). The second credits it to the user and returns the new balance. Clean and minimal.
