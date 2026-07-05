```javascript
const express = require('express');
const app = express();

// In-memory store: IP -> [timestamps of requests]
const requestLog = new Map();

const RATE_LIMIT = 10;
const WINDOW = 60 * 1000; // 1 minute

const rateLimiter = (req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  const now = Date.now();

  if (!requestLog.has(ip)) {
    requestLog.set(ip, []);
  }

  const log = requestLog.get(ip);

  // Remove requests outside the window
  const validRequests = log.filter(ts => now - ts < WINDOW);
  requestLog.set(ip, validRequests);

  // Set rate limit headers
  res.set('X-RateLimit-Limit', RATE_LIMIT);
  res.set('X-RateLimit-Remaining', Math.max(0, RATE_LIMIT - validRequests.length));

  if (validRequests.length >= RATE_LIMIT) {
    return res.status(429).json({ error: 'Too many requests, max 10 per minute' });
  }

  validRequests.push(now);
  next();
};

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler here
  res.json({ success: true });
});

// Clean up stale entries every 5 minutes to prevent memory leak
setInterval(() => {
  const now = Date.now();
  for (const [ip, log] of requestLog.entries()) {
    const validRequests = log.filter(ts => now - ts < WINDOW);
    if (validRequests.length === 0) {
      requestLog.delete(ip);
    } else {
      requestLog.set(ip, validRequests);
    }
  }
}, 5 * 60 * 1000);
```

**Key points:**
- Stores timestamps per IP in memory
- Filters out requests older than 60 seconds on each check
- Returns 429 with remaining quota in headers
- Cleanup interval prevents unbounded memory growth
- For `req.ip`: Express/Node will respect `X-Forwarded-For` if you've set `trust proxy` — adjust if behind a load balancer

When you scale to multiple processes, swap the `Map` for Redis.
