```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  const coupon = await db.query(
    'SELECT amount FROM coupons WHERE code = $1',
    [code]
  );

  if (!coupon.rows.length) {
    return res.status(404).json({ error: 'Coupon not found' });
  }

  const { amount } = coupon.rows[0];
  await db.query(
    'UPDATE users SET balance = balance + $1 WHERE id = $2',
    [amount, req.user.id]
  );

  res.json({ amount });
});
```

Two queries: fetch the coupon, then credit the user. Returns 404 if the code doesn't exist, 200 with the credited amount on success.
