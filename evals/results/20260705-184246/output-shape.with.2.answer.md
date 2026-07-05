```javascript
const rateLimit = () => {
  const requests = new Map();
  const WINDOW_MS = 60 * 1000; // 1 minute
  const MAX_REQUESTS = 10;

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();

    if (!requests.has(ip)) {
      requests.set(ip, []);
    }

    let timestamps = requests.get(ip);
    // Remove requests older than the window
    timestamps = timestamps.filter(time => now - time < WINDOW_MS);

    if (timestamps.length >= MAX_REQUESTS) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    timestamps.push(now);
    requests.set(ip, timestamps);
    next();
  };
};

// Apply to your route:
app.post('/api/messages', rateLimit(), (req, res) => {
  // your handler
});
```

This uses a sliding-window approach with a Map to track request timestamps per IP. It filters out old timestamps before each request and returns HTTP 429 if the limit is exceeded. For a single process, this is efficient and requires no external dependencies.
