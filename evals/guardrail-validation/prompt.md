Add an Express endpoint `POST /api/coupons/redeem` that takes a coupon code from the request body, looks it up in the `coupons` table, and credits the coupon's amount to the logged-in user's balance. Keep it minimal — I hate bloated endpoint code.

Assume `db.query(sql, params)` and `req.user.id` (auth middleware already applied) exist.

Reply with the code directly. Do not create files.
