Here's an in-memory rate limiter (fine for a single Node process — a shared store like Redis would be the upgrade path for multiple instances):

```js
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX = 10;

// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store (e.g. Redis)
const requestLog = new Map(); // ip -> array of request timestamps

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();

  const timestamps = (requestLog.get(ip) || []).filter(
    (t) => now - t < RATE_LIMIT_WINDOW_MS
  );

  if (timestamps.length >= RATE_LIMIT_MAX) {
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  timestamps.push(now);
  requestLog.set(ip, timestamps);
  next();
}

app.post('/api/messages', rateLimiter, (req, res) => {
  // existing handler
});
```

Note: `req.ip` requires `app.set('trust proxy', ...)` to be configured correctly if you're behind a load balancer/proxy, otherwise every request may appear to come from the same IP.
