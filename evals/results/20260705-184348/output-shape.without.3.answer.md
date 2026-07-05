```javascript
const express = require('express');
const app = express();

// Simple in-memory rate limiter
const requestCounts = new Map();

function rateLimit(maxRequests, windowMs) {
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    
    if (!requestCounts.has(ip)) {
      requestCounts.set(ip, []);
    }
    
    const requests = requestCounts.get(ip);
    const recentRequests = requests.filter(time => now - time < windowMs);
    
    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    recentRequests.push(now);
    requestCounts.set(ip, recentRequests);
    next();
  };
}

// Cleanup old entries every 5 minutes to prevent memory leak
setInterval(() => {
  const now = Date.now();
  const windowMs = 60000; // 1 minute
  
  for (const [ip, requests] of requestCounts.entries()) {
    const active = requests.filter(time => now - time < windowMs);
    if (active.length === 0) {
      requestCounts.delete(ip);
    } else {
      requestCounts.set(ip, active);
    }
  }
}, 300000);

app.post('/api/messages', rateLimit(10, 60000), (req, res) => {
  // Your handler
  res.json({ success: true });
});

app.listen(3000);
```

The middleware tracks request timestamps per IP in memory. Each request checks if there are ≥10 requests within the 60-second window—if so, returns 429. A cleanup interval runs every 5 minutes to prune expired entries and prevent unbounded memory growth.

For production at scale, switch to `express-rate-limit` or Redis-backed solutions.
