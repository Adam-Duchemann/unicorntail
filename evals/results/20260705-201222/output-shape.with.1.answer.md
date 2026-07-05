Here's a simple in-memory rate limiter for your Express API:

```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> Redis or shared store
const requestCounts = {}; // { ip: { count, resetTime } }
const WINDOW_MS = 60 * 1000; // 1 minute
const MAX_REQUESTS = 10;

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  
  if (!requestCounts[ip]) {
    requestCounts[ip] = { count: 1, resetTime: now + WINDOW_MS };
    return next();
  }
  
  if (now > requestCounts[ip].resetTime) {
    requestCounts[ip] = { count: 1, resetTime: now + WINDOW_MS };
    return next();
  }
  
  requestCounts[ip].count++;
  if (requestCounts[ip].count > MAX_REQUESTS) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  next();
}

// Apply to your route
app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler
});
```

Tracks requests per IP in memory, resets the window every minute, returns 429 (Too Many Requests) when limit is exceeded. Works for a single process; swap for Redis if you scale to multiple instances later.
