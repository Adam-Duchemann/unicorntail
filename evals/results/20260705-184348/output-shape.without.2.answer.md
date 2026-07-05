```javascript
// Rate limiter middleware
const createRateLimiter = (maxRequests = 10, windowMs = 60 * 1000) => {
  const requests = new Map(); // { ip: [timestamp1, timestamp2, ...] }

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    if (!requests.has(ip)) {
      requests.set(ip, []);
    }

    let timestamps = requests.get(ip);
    
    // Remove timestamps outside the window
    timestamps = timestamps.filter(t => now - t < windowMs);
    
    if (timestamps.length >= maxRequests) {
      return res.status(429).json({ 
        error: 'Too many requests, please try again later' 
      });
    }

    timestamps.push(now);
    requests.set(ip, timestamps);
    
    next();
  };
};

// Apply to your route
const messageLimiter = createRateLimiter(10, 60 * 1000);

app.post('/api/messages', messageLimiter, (req, res) => {
  // Your handler
});
```

This stores request timestamps per IP in memory. Old timestamps are filtered out on each request, so memory stays bounded. When the limit is hit within the window, it returns a 429 status.
