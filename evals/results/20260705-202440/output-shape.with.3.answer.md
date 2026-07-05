```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> Redis/Memcached
const rateLimiter = (() => {
  const requests = new Map(); // IP -> { count, resetAt }

  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const minute = 60000;

    if (requests.has(ip)) {
      const record = requests.get(ip);
      if (now < record.resetAt) {
        if (record.count >= 10) {
          return res.status(429).json({ error: 'Too many requests' });
        }
        record.count++;
      } else {
        record.count = 1;
        record.resetAt = now + minute;
      }
    } else {
      requests.set(ip, { count: 1, resetAt: now + minute });
    }

    next();
  };
})();

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler here
});
```

The middleware tracks requests by IP in a `Map`. Each IP gets a rolling 60-second window—once the window passes, the counter resets. Returns `429 Too Many Requests` when the limit is hit. The closure keeps the state private.

If you need to trust proxy headers (running behind a load balancer), add `app.set('trust proxy', 1)` before mounting the middleware.
