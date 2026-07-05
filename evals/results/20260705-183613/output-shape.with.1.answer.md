```javascript
const express = require('express');
const app = express();

// In-memory rate limiter: IP → array of request timestamps
const requestTimestamps = new Map();

const rateLimiter = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const oneMinuteAgo = now - 60_000;
  
  if (!requestTimestamps.has(ip)) {
    requestTimestamps.set(ip, []);
  }
  
  const timestamps = requestTimestamps.get(ip);
  const recent = timestamps.filter(t => t > oneMinuteAgo);
  
  if (recent.length >= 10) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  
  recent.push(now);
  requestTimestamps.set(ip, recent);
  next();
};

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler
  res.json({ success: true });
});
```

**How it works:**
- Each IP gets a list of request timestamps in a Map
- On each request, filter timestamps to only the past 60 seconds
- If ≥10 requests in that window, reject with 429
- Otherwise, append the current timestamp and continue

**Optional cleanup** (prevents unbounded Map growth): add this after the filter:
```javascript
if (recent.length === 0) requestTimestamps.delete(ip);
else requestTimestamps.set(ip, recent);
```
