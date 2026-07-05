```typescript
import express, { Request, Response, NextFunction } from 'express';

// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> redis or similar
const requestCounts = new Map<string, { count: number; resetTime: number }>();
const WINDOW_MS = 60 * 1000; // 1 minute
const LIMIT = 10;

function rateLimiter(req: Request, res: Response, next: NextFunction) {
  const ip = req.ip || 'unknown';
  const now = Date.now();
  
  const record = requestCounts.get(ip);
  
  if (!record || now > record.resetTime) {
    // New window or first request
    requestCounts.set(ip, { count: 1, resetTime: now + WINDOW_MS });
    return next();
  }
  
  if (record.count >= LIMIT) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  record.count++;
  next();
}

const app = express();
app.post('/api/messages', rateLimiter, (req: Request, res: Response) => {
  // Your message handling logic
  res.json({ message: 'Message received' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

The middleware tracks requests by IP in memory. Each IP gets a 1-minute window; once it exceeds 10 requests in that window, subsequent requests get a 429 response. The window resets automatically when the timestamp passes.
