```javascript
const rateLimit = {};

const rateLimiterMiddleware = (req, res, next) => {
  // Get client IP (handles proxies like reverse proxy/load balancer)
  const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.ip;
  const now = Date.now();
  const windowMs = 60 * 1000; // 1 minute
  const maxRequests = 10;

  if (!rateLimit[ip]) {
    rateLimit[ip] = [];
  }

  // Remove requests older than the window
  rateLimit[ip] = rateLimit[ip].filter(timestamp => now - timestamp < windowMs);

  if (rateLimit[ip].length >= maxRequests) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  rateLimit[ip].push(now);
  next();
};

app.post('/api/messages', rateLimiterMiddleware, (req, res) => {
  // Your endpoint logic
  res.json({ success: true });
});
```

Tracks request timestamps per IP in memory. On each request, it purges timestamps older than 60 seconds, then either rejects (429) if the limit is hit or records the request and continues. Handles `X-Forwarded-For` for proxy scenarios.
