```js
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store (e.g. Redis)
const RATE_LIMIT = 10;
const WINDOW_MS = 60 * 1000;
const hits = new Map(); // ip -> { count, resetAt }

function rateLimit(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const entry = hits.get(ip);

  if (!entry || now > entry.resetAt) {
    hits.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return next();
  }

  if (entry.count >= RATE_LIMIT) {
    const retryAfter = Math.ceil((entry.resetAt - now) / 1000);
    res.set('Retry-After', String(retryAfter));
    return res.status(429).json({ error: 'Too many requests' });
  }

  entry.count++;
  next();
}

app.post('/api/messages', rateLimit, (req, res) => {
  // existing handler
});
```

Note: `req.ip` requires `app.set('trust proxy', ...)` configured correctly if you're behind a proxy/load balancer, otherwise all requests may appear to come from the same IP.
