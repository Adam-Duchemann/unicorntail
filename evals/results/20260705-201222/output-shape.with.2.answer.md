```javascript
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> Redis
const requestCounts = new Map(); // IP -> array of timestamps

const rateLimit = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const oneMinuteAgo = now - 60000;

  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, []);
  }

  const timestamps = requestCounts.get(ip);
  
  // Remove timestamps older than 1 minute
  const recent = timestamps.filter(ts => ts > oneMinuteAgo);
  requestCounts.set(ip, recent);

  if (recent.length >= 10) {
    return res.status(429).json({ error: 'Too Many Requests' });
  }

  recent.push(now);
  next();
};

app.post('/api/messages', rateLimit, (req, res) => {
  // your message handler
});
```

The middleware tracks request timestamps per IP in memory, prunes old entries (>1 min), and returns 429 when the limit is hit. Works for a single process; switch to Redis if you scale to multiple instances.
