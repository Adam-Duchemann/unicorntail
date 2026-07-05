```javascript
const rateLimit = (() => {
  const requests = new Map();
  const LIMIT = 10;
  const WINDOW_MS = 60 * 1000;

  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const timestamps = requests.get(ip) || [];
    const recent = timestamps.filter(t => now - t < WINDOW_MS);

    if (recent.length >= LIMIT) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    recent.push(now);
    requests.set(ip, recent);
    next();
  };
})();

// Apply to route:
app.post('/api/messages', rateLimit, (req, res) => {
  // handler
});
```

Skipped: `express-rate-limit` dependency — add when you scale to multiple processes or need features like response headers or skip conditions.
