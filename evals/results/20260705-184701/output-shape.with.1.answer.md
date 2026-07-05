Here's a simple in-memory rate limiter middleware for your single-process setup:

```javascript
// ponytail: in-memory rate limit store, ceiling: single process (resets on restart), grows unbounded per unique IP
// upgrade when: multi-process → Redis, or add periodic cleanup of expired entries
const rateLimit = (() => {
  const store = new Map();
  const WINDOW_MS = 60 * 1000; // 1 minute
  const MAX_REQUESTS = 10;

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();

    if (!store.has(ip)) {
      store.set(ip, { count: 1, resetTime: now + WINDOW_MS });
      return next();
    }

    const record = store.get(ip);

    if (now >= record.resetTime) {
      record.count = 1;
      record.resetTime = now + WINDOW_MS;
      return next();
    }

    if (record.count >= MAX_REQUESTS) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    record.count++;
    next();
  };
})();

// Apply to your endpoint:
app.post('/api/messages', rateLimit, (req, res) => {
  // handler
});
```

The middleware tracks requests per IP in memory, resets the counter every minute, and returns HTTP 429 when the limit is exceeded. For multi-process deployments later, swap to Redis.
