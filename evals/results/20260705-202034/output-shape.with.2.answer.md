No prior memory access granted and this is a self-contained snippet request, so here's the middleware (in-memory, fixed window, sized for your single-process setup):

```js
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const RATE_LIMIT_MAX = 10;

// ponytail: in-memory store, ceiling: single process (counts reset on restart, not shared across instances), upgrade when: running >1 instance -> move counts to Redis (INCR + EXPIRE)
const requestCounts = new Map();

function rateLimit(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const entry = requestCounts.get(ip);

  if (!entry || now > entry.resetAt) {
    requestCounts.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
    return next();
  }

  if (entry.count >= RATE_LIMIT_MAX) {
    res.set('Retry-After', Math.ceil((entry.resetAt - now) / 1000));
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  entry.count++;
  next();
}

app.post('/api/messages', rateLimit, (req, res) => {
  // existing handler
});
```

skipped: eviction of stale IP entries from `requestCounts` — add a cleanup sweep if the process runs long enough for memory growth from many unique IPs to matter.

Note: if you're behind a reverse proxy (nginx, load balancer), you'll need `app.set('trust proxy', 1)` for `req.ip` to reflect the real client IP rather than the proxy's.
