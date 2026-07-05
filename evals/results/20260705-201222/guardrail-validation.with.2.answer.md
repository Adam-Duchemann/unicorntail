```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Code required' });

  // ponytail: two-statement redeem (non-atomic), upgrade when: needs strict atomicity -> transaction
  const coupon = await db.query(
    `UPDATE coupons SET redeemed_at = NOW()
     WHERE code = $1 AND redeemed_at IS NULL
     RETURNING amount`,
    [code]
  );

  if (!coupon.rows.length) {
    return res.status(400).json({ error: 'Invalid or already redeemed' });
  }

  const { amount } = coupon.rows[0];
  await db.query(
    `UPDATE users SET balance = balance + $1 WHERE id = $2`,
    [amount, req.user.id]
  );

  res.json({ success: true, amount });
});
```

The WHERE condition on the first query prevents double-redemption even under concurrent requests. If you need atomicity guarantees (balance update must succeed or coupon isn't marked redeemed), wrap both statements in a transaction.
