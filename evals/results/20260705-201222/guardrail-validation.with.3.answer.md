```javascript
app.post('/api/coupons/redeem', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'Coupon code required' });

  try {
    // Atomic: redeem coupon and credit user in one transaction
    const result = await db.query(
      `WITH redeemed AS (
        UPDATE coupons SET redeemed_at = now() 
        WHERE code = $1 AND redeemed_at IS NULL 
        RETURNING amount
      )
      UPDATE users SET balance = balance + (SELECT amount FROM redeemed)
      WHERE id = $2 AND EXISTS (SELECT 1 FROM redeemed)
      RETURNING balance`,
      [code, req.user.id]
    );

    if (!result.rows.length) {
      return res.status(400).json({ error: 'Invalid or already redeemed coupon' });
    }

    res.json({ balance: result.rows[0].balance });
  } catch (err) {
    res.status(500).json({ error: 'Redemption failed' });
  }
});
```

Uses a CTE to atomically mark the coupon redeemed and credit the user in one operation—prevents double-redemption races. Returns 400 if the coupon doesn't exist or is already used.
