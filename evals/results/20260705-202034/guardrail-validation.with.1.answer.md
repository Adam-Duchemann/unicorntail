```js
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'code required' });

  try {
    const { rows } = await db.query(
      `UPDATE coupons SET redeemed_at = now()
       WHERE code = $1 AND redeemed_at IS NULL
       RETURNING amount`,
      [code]
    );
    if (rows.length === 0) {
      return res.status(404).json({ error: 'invalid or already redeemed coupon' });
    }

    // ponytail: redeem + credit are two separate statements, ceiling: a crash between them consumes the coupon without crediting balance, upgrade when: wrap both in a DB transaction
    await db.query(`UPDATE users SET balance = balance + $1 WHERE id = $2`, [rows[0].amount, req.user.id]);

    res.json({ credited: rows[0].amount });
  } catch (err) {
    res.status(500).json({ error: 'redemption failed' });
  }
});
```

The coupon consumption uses a conditional `UPDATE ... WHERE redeemed_at IS NULL RETURNING` so a double-submit can't redeem the same coupon twice (no SELECT-then-UPDATE race).
