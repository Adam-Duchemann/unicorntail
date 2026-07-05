```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }
  
  try {
    const coupon = await db.query(
      'SELECT id, amount, used FROM coupons WHERE code = $1',
      [code]
    );
    
    if (coupon.rows.length === 0) {
      return res.status(404).json({ error: 'Coupon not found' });
    }
    
    const { id, amount, used } = coupon.rows[0];
    
    if (used) {
      return res.status(400).json({ error: 'Coupon already redeemed' });
    }
    
    await db.query(
      'UPDATE users SET balance = balance + $1 WHERE id = $2',
      [amount, req.user.id]
    );
    
    await db.query('UPDATE coupons SET used = true WHERE id = $1', [id]);
    
    res.json({ success: true, amount });
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

Validates input at the boundary, checks coupon exists and hasn't been used, credits the balance in one transaction, marks coupon consumed. Error handling only for what can actually go wrong.
