Here's a simple in-memory rate limiter for your Express API:

```javascript
const express = require('express');
const app = express();

// Simple in-memory rate limiter
const requestCounts = new Map();
const LIMIT = 10;              // max requests
const WINDOW = 60 * 1000;      // 1 minute in ms

const rateLimiter = (req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  const now = Date.now();
  
  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, []);
  }
  
  const timestamps = requestCounts.get(ip);
  const recentRequests = timestamps.filter(t => now - t < WINDOW);
  
  if (recentRequests.length >= LIMIT) {
    return res.status(429).json({ error: 'Too many requests, try again later' });
  }
  
  recentRequests.push(now);
  requestCounts.set(ip, recentRequests);
  next();
};

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your message handling logic here
  res.json({ success: true });
});

app.listen(3000);
```

**How it works:**
- Tracks request timestamps per IP in a Map
- Filters out timestamps older than 60 seconds
- Rejects with 429 if 10+ recent requests exist
- Stores the new request timestamp and calls `next()`

For production with multiple processes, you'd swap this for Redis-backed rate limiting, but this handles single-process workloads well.
