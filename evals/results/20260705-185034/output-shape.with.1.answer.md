```javascript
const rateLimit = () => {
  const store = {}; // ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> redis
  
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const windowMs = 60 * 1000;
    const maxRequests = 10;
    
    if (!store[ip]) {
      store[ip] = { count: 0, resetTime: now + windowMs };
    }
    
    if (now > store[ip].resetTime) {
      store[ip].count = 0;
      store[ip].resetTime = now + windowMs;
    }
    
    if (store[ip].count >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    store[ip].count++;
    next();
  };
};

app.post('/api/messages', rateLimit(), (req, res) => {
  // your handler
});
```

Tracks requests per IP in memory, resets the counter every 60 seconds. Returns 429 (Too Many Requests) when limit is hit. When you scale to multiple processes, swap the in-memory `store` for Redis.
