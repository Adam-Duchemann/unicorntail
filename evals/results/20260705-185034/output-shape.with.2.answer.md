Here's a simple in-memory rate limiter for your use case:

```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> use Redis
const requestTimestamps = new Map();
const RATE_LIMIT = 10;
const WINDOW_MS = 60 * 1000; // 1 minute

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  
  if (!requestTimestamps.has(ip)) {
    requestTimestamps.set(ip, []);
  }
  
  const timestamps = requestTimestamps.get(ip);
  const recentTimestamps = timestamps.filter(ts => now - ts < WINDOW_MS);
  
  if (recentTimestamps.length >= RATE_LIMIT) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  recentTimestamps.push(now);
  requestTimestamps.set(ip, recentTimestamps);
  next();
}

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler here
});
```

The middleware tracks timestamps per IP in a sliding window. When a request arrives, it discards timestamps older than 1 minute and checks if the count in that window exceeds 10. If so, it returns a 429 status code. Otherwise, it adds the current timestamp and continues.

Since you're on a single process now, the in-memory Map is fine—the ponytail comment marks when to upgrade to Redis if you scale to multiple processes.
