```javascript
const express = require('express');
const app = express();

// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store (Redis)
const createRateLimiter = () => {
  const store = new Map();

  return (req, res, next) => {
    const ip = req.ip;
    const minuteBucket = Math.floor(Date.now() / 60000);
    const key = `${ip}:${minuteBucket}`;

    const count = (store.get(key) || 0) + 1;
    store.set(key, count);

    // Cleanup old buckets to prevent memory leaks
    for (const [k] of store) {
      const bucket = parseInt(k.split(':')[1]);
      if (bucket < minuteBucket - 1) store.delete(k);
    }

    if (count > 10) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    next();
  };
};

app.post('/api/messages', createRateLimiter(), (req, res) => {
  res.json({ message: 'ok' });
});
```

The middleware divides time into 60-second buckets, tracks requests per IP per bucket, and rejects with 429 once you hit 10. Old buckets are cleaned up automatically. When you scale to multiple processes, swap the Map for Redis.
