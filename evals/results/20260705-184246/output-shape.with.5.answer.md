```javascript
const rateLimit = {};

const createRateLimiter = (maxRequests = 10, windowMs = 60000) => {
  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    if (!rateLimit[ip]) {
      rateLimit[ip] = [];
    }
    
    // Remove timestamps older than the window
    rateLimit[ip] = rateLimit[ip].filter(time => now - time < windowMs);
    
    if (rateLimit[ip].length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    rateLimit[ip].push(now);
    res.set('X-RateLimit-Limit', maxRequests);
    res.set('X-RateLimit-Remaining', maxRequests - rateLimit[ip].length);
    
    next();
  };
};

// Apply to the route:
const limiter = createRateLimiter(10, 60000); // 10 requests per 60 seconds
app.post('/api/messages', limiter, (req, res) => {
  // Your handler
});
```

This stores request timestamps in memory keyed by IP, removes old entries on each request, and blocks with 429 when the limit is exceeded. Sets standard rate-limit headers on each response.
