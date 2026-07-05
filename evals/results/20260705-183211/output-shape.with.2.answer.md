Here's a simple in-memory rate limiter for a single Node process:

```javascript
const rateLimit = (() => {
  const store = new Map(); // { ip: { count, resetTime } }
  const MAX_REQUESTS = 10;
  const WINDOW_MS = 60 * 1000; // 1 minute

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    let record = store.get(ip);

    if (!record || now > record.resetTime) {
      store.set(ip, { count: 1, resetTime: now + WINDOW_MS });
      return next();
    }

    if (record.count >= MAX_REQUESTS) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    record.count++;
    next();
  };
})();

// Use it on your route:
app.post('/api/messages', rateLimit, (req, res) => {
  // Your handler here
});
```

**How it works:**
- Tracks `count` and `resetTime` per IP in a Map
- Resets the counter each minute
- Returns 429 when limit is hit
- `req.ip` handles proxied requests; falls back to raw connection address

**Note:** This uses IIFE to create a private closure for the store. If you need to clear old entries to prevent memory leaks in very long-running processes, add periodic cleanup (e.g., delete entries older than 5 minutes).
