```javascript
const express = require('express');
const app = express();

// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store (Redis)
const requestCounts = new Map();

const rateLimit = (maxRequests, windowMs) => {
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const windowStart = now - windowMs;

    if (!requestCounts.has(ip)) {
      requestCounts.set(ip, []);
    }

    const timestamps = requestCounts.get(ip);
    const recentRequests = timestamps.filter(ts => ts > windowStart);

    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    recentRequests.push(now);
    requestCounts.set(ip, recentRequests);
    next();
  };
};

// Apply to your endpoint: 10 requests per 60 seconds
app.post('/api/messages', rateLimit(10, 60000), (req, res) => {
  // your handler
  res.json({ ok: true });
});
```

Tracks request timestamps per IP in memory. Rejects with 429 when limit hit. When you scale to multiple processes, swap the `Map` for Redis.
