```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Coupon code required' });
  }

  try {
    const { rows } = await db.query('SELECT amount FROM coupons WHERE code = $1', [code]);
    
    if (!rows.length) {
      return res.status(404).json({ error: 'Coupon not found' });
    }

    const amount = rows[0].amount;
    await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);

    res.json({ success: true, credited: amount });
  } catch (err) {
    res.status(500).json({ error: 'Failed to redeem coupon' });
  }
});
```

Three queries: validate input, fetch coupon amount, credit balance. Done.
