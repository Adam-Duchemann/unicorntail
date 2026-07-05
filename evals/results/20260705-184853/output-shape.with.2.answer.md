No prior context found for this. Here's an in-memory rate limiter middleware:

```js
const RATE_LIMIT = 10; // max requests
const WINDOW_MS = 60 * 1000; // per 1 minute

// ponytail: in-memory Map, ceiling: single process (state lost on restart, not shared across instances), upgrade when: running multiple Node processes/instances -> move to Redis (e.g. INCR + EXPIRE)
const hits = new Map(); // ip -> { count, resetAt }

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const entry = hits.get(ip);

  if (!entry || now > entry.resetAt) {
    hits.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return next();
  }

  if (entry.count >= RATE_LIMIT) {
    res.set('Retry-After', Math.ceil((entry.resetAt - now) / 1000));
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  entry.count++;
  next();
}

// periodic cleanup so the map doesn't grow unbounded with stale IPs
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of hits) {
    if (now > entry.resetAt) hits.delete(ip);
  }
}, WINDOW_MS).unref();

app.post('/api/messages', rateLimiter, (req, res) => {
  // existing handler
});
```

skipped: distributed/shared store across processes — add when you scale past a single Node process.

Note: `req.ip` requires `app.set('trust proxy', ...)` configured correctly if you're behind a proxy/load balancer, otherwise all requests may appear to come from the proxy's IP.
