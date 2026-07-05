Here's a simple in-memory rate limiter middleware (no extra dependencies needed, single-process is fine for this):

```js
const rateLimitBuckets = new Map(); // ip -> { count, resetAt }

function rateLimit({ windowMs = 60_000, max = 10 } = {}) {
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const bucket = rateLimitBuckets.get(ip);

    if (!bucket || now >= bucket.resetAt) {
      rateLimitBuckets.set(ip, { count: 1, resetAt: now + windowMs });
      return next();
    }

    if (bucket.count >= max) {
      const retryAfterSec = Math.ceil((bucket.resetAt - now) / 1000);
      res.set('Retry-After', String(retryAfterSec));
      return res.status(429).json({ error: 'Too many requests, please try again later.' });
    }

    bucket.count += 1;
    next();
  };
}

// periodically clear stale buckets so the Map doesn't grow forever
setInterval(() => {
  const now = Date.now();
  for (const [ip, bucket] of rateLimitBuckets) {
    if (now >= bucket.resetAt) rateLimitBuckets.delete(ip);
  }
}, 60_000).unref();

app.post('/api/messages', rateLimit({ windowMs: 60_000, max: 10 }), (req, res) => {
  // your existing handler
});
```

Notes:
- If your app sits behind a proxy/load balancer, make sure `app.set('trust proxy', ...)` is configured correctly so `req.ip` reflects the real client IP.
- This resets per-IP counts on a fixed window (not sliding), which is simplest and fine for "max 10/min" semantics. If you later need sliding-window precision or multi-process/horizontal scaling, swap the `Map` for Redis (e.g. via `rate-limiter-flexible` or `express-rate-limit` with a Redis store) — but for a single process this is sufficient.
