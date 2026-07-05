```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  const userId = req.user.id;

  const result = await db.query(
    'UPDATE coupons SET redeemed_by = $1, redeemed_at = NOW() WHERE code = $2 AND redeemed_by IS NULL RETURNING amount',
    [userId, code]
  );

  if (!result.rows.length) {
    return res.status(404).json({ error: 'Coupon not found or already redeemed' });
  }

  const amount = result.rows[0].amount;
  await db.query('UPDATE users SET balance = balance + $1 WHERE id = $2', [amount, userId]);

  res.json({ success: true });
});
```

The atomic `UPDATE … RETURNING` in a single statement prevents concurrent requests from redeeming the same coupon twice — if it's already marked (`redeemed_by IS NOT NULL`), the second request gets zero rows back.
