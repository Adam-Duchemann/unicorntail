```javascript
const express = require('express');
const app = express();

// Rate limiter state
const requests = new Map(); // IP -> { count, resetTime }
const RATE_LIMIT = 10;
const WINDOW_MS = 60 * 1000; // 1 minute

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const record = requests.get(ip);
  
  if (!record || now > record.resetTime) {
    requests.set(ip, { count: 1, resetTime: now + WINDOW_MS });
    return next();
  }
  
  if (record.count >= RATE_LIMIT) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  record.count++;
  next();
}

// Cleanup expired entries every minute to prevent memory leak
setInterval(() => {
  const now = Date.now();
  for (const [ip, record] of requests.entries()) {
    if (now > record.resetTime) {
      requests.delete(ip);
    }
  }
}, 60 * 1000);

// Apply rate limiter to the endpoint
app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler here
  res.json({ message: 'Received' });
});
```

The middleware tracks request count per IP within a rolling 60-second window. Requests beyond 10 return 429 (Too Many Requests). The cleanup loop prevents old entries from accumulating indefinitely.
