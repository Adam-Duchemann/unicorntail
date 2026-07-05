```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  try {
    const { code } = req.body;
    if (!code) return res.status(400).json({ error: 'Coupon code required' });

    const coupon = await db.query(
      'SELECT amount FROM coupons WHERE code = $1 AND used = false',
      [code]
    );
    if (!coupon.rows.length) {
      return res.status(404).json({ error: 'Invalid or used coupon' });
    }

    const amount = coupon.rows[0].amount;
    await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, req.user.id]);
    await db.query('UPDATE coupons SET used = true WHERE code = $1', [code]);

    res.json({ success: true, amount });
  } catch (err) {
    res.status(500).json({ error: 'Failed to redeem coupon' });
  }
});
```

Assumes coupons table has `code`, `amount`, and `used` columns; users table has `balance`. Validates code exists, isn't already used, credits the amount, marks it consumed.
