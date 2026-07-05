No prior memory on this. Here's a single-process, in-memory rate limiter middleware:

```js
const RATE_LIMIT = 10;
const WINDOW_MS = 60_000;

// ponytail: in-memory store, ceiling: single process (resets on restart, not shared across instances), upgrade when: multiple instances -> shared store (e.g. Redis)
const hits = new Map(); // ip -> { count, resetAt }

function rateLimit(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const entry = hits.get(ip);

  if (!entry || now >= entry.resetAt) {
    hits.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return next();
  }

  if (entry.count >= RATE_LIMIT) {
    res.set('Retry-After', Math.ceil((entry.resetAt - now) / 1000));
    return res.status(429).json({ error: 'Too many requests' });
  }

  entry.count++;
  next();
}

app.post('/api/messages', rateLimit, (req, res) => {
  // existing handler
});
```

skipped: cleanup of stale IP entries — add a `setInterval` sweep (or switch to an LRU cache) when memory growth from abandoned IPs becomes a real concern.

Note: `req.ip` needs `app.set('trust proxy', ...)` configured correctly if you're behind a reverse proxy/load balancer, otherwise every request may resolve to the proxy's IP.
