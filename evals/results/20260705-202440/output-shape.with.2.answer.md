```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> Redis/shared store
const rateLimit = () => {
  const store = new Map();
  const LIMIT = 10;
  const WINDOW_MS = 60 * 1000;

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    let data = store.get(ip);

    if (!data || now > data.resetTime) {
      data = { count: 0, resetTime: now + WINDOW_MS };
      store.set(ip, data);
    }

    data.count++;
    res.set('X-RateLimit-Limit', LIMIT);
    res.set('X-RateLimit-Remaining', Math.max(0, LIMIT - data.count));
    res.set('X-RateLimit-Reset', new Date(data.resetTime).toISOString());

    if (data.count > LIMIT) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    next();
  };
};

app.post('/api/messages', rateLimit(), (req, res) => {
  // your handler
});
```

Each IP gets a fresh 10-request window every minute. Returns 429 when exceeded, and sets standard `X-RateLimit-*` headers so clients know their quota.
