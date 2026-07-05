```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  try {
    // ponytail: sync transaction; upgrade when: async queue needed for scale
    await db.query('BEGIN');
    
    const coupon = await db.query(
      'UPDATE coupons SET redeemed_at = NOW() WHERE code = $1 AND redeemed_at IS NULL RETURNING amount',
      [code]
    );
    
    if (!coupon.rows[0]) {
      await db.query('ROLLBACK');
      return res.status(400).json({ error: 'Invalid coupon' });
    }
    
    const { amount } = coupon.rows[0];
    
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );
    
    await db.query('COMMIT');
    res.json({ amount });
  } catch (err) {
    await db.query('ROLLBACK').catch(() => {});
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

The UPDATE with `WHERE code = $1 AND redeemed_at IS NULL` ensures only one redemption succeeds concurrently. Both operations complete in a single transaction so balance and coupon state stay consistent.
