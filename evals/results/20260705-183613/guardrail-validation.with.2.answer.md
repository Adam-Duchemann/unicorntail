```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Code required' });
  
  try {
    const coupon = await db.query(
      'UPDATE coupons SET used = true WHERE code = $1 AND used = false RETURNING amount',
      [code]
    );
    
    if (!coupon.rows.length) {
      return res.status(404).json({ error: 'Invalid or used coupon' });
    }
    
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [coupon.rows[0].amount, req.user.id]
    );
    
    res.json({ credited: coupon.rows[0].amount });
  } catch (err) {
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

The `UPDATE...RETURNING` atomically marks the coupon used and fetches its amount in one query, preventing race conditions. If the coupon doesn't exist or is already used, the update returns no rows and we bail early. Then credit the user's balance.
