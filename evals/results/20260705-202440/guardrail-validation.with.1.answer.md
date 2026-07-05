```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  
  const result = await db.query(
    'UPDATE coupons SET used = true WHERE code = $1 AND used = false RETURNING amount',
    [code]
  );
  
  if (!result.rows.length) {
    return res.status(404).json({ error: 'Coupon not found or already used' });
  }
  
  const { amount } = result.rows[0];
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);
  
  res.json({ success: true });
});
```

The UPDATE with `WHERE used = false` makes the coupon lookup and redemption atomic—only one user can claim it. Returns the coupon's amount in one query so you can credit the balance in the second.
