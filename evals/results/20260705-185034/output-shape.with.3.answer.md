Here's a simple in-memory rate limiter for your Express API:

```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store
const requestCounts = new Map();

function rateLimit(windowMs = 60000, maxRequests = 10) {
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    
    if (!requestCounts.has(ip)) {
      requestCounts.set(ip, []);
    }
    
    const timestamps = requestCounts.get(ip);
    const validTimestamps = timestamps.filter(ts => now - ts < windowMs);
    
    if (validTimestamps.length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    validTimestamps.push(now);
    requestCounts.set(ip, validTimestamps);
    next();
  };
}

// Apply to your endpoint
app.post('/api/messages', rateLimit(60000, 10), (req, res) => {
  // Your handler
});
```

This tracks request timestamps per IP in memory, cleans up old entries outside the 1-minute window, and rejects with 429 when the limit is exceeded. Works fine for a single process; when you scale to multiple processes, swap the `Map` for Redis or similar.
