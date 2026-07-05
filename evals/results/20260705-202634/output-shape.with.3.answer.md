Here's a middleware using a plain `Map`, no new dependency needed for this:

```js
// ponytail: in-memory store, ceiling: single process (state lost on restart, not shared across instances), upgrade when: running >1 instance -> shared store (e.g. Redis)
const WINDOW_MS = 60_000;
const MAX_REQUESTS = 10;
const hits = new Map(); // ip -> { count, resetAt }

function rateLimit(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const entry = hits.get(ip);

  if (!entry || now > entry.resetAt) {
    hits.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return next();
  }

  if (entry.count >= MAX_REQUESTS) {
    res.set('Retry-After', String(Math.ceil((entry.resetAt - now) / 1000)));
    return res.status(429).json({ error: 'Too many requests' });
  }

  entry.count++;
  next();
}

// ponytail: naive full-map scan for cleanup, ceiling: fine at low IP cardinality, upgrade when: memory growth from unique IPs becomes a problem -> switch to LRU cache with max size
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of hits) {
    if (now > entry.resetAt) hits.delete(ip);
  }
}, WINDOW_MS).unref();

app.post('/api/messages', rateLimit, (req, res) => {
  // existing handler
});
```

If your API sits behind a proxy/load balancer, add `app.set('trust proxy', 1)` so `req.ip` reflects the real client IP instead of the proxy's.
