```javascript
const rateLimit = (() => {
  const store = new Map(); // IP -> array of request timestamps
  const limit = 10;
  const window = 60 * 1000; // 1 minute in ms

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    if (!store.has(ip)) {
      store.set(ip, []);
    }
    
    const timestamps = store.get(ip);
    
    // Remove timestamps outside the window
    while (timestamps.length > 0 && timestamps[0] < now - window) {
      timestamps.shift();
    }
    
    // Check if limit exceeded
    if (timestamps.length >= limit) {
      return res.status(429).json({ 
        error: 'Too many requests',
        retryAfter: Math.ceil((timestamps[0] + window - now) / 1000)
      });
    }
    
    // Record this request
    timestamps.push(now);
    res.set('X-RateLimit-Limit', limit);
    res.set('X-RateLimit-Remaining', limit - timestamps.length);
    
    next();
  };
})();

// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> Redis/shared store

// Apply to the route
app.post('/api/messages', rateLimit, (req, res) => {
  // your handler
});
```

The middleware tracks request timestamps per IP in memory, cleaning up entries older than 1 minute. Returns 429 with a `retryAfter` hint when the limit is hit. Sets response headers so clients know their quota.
