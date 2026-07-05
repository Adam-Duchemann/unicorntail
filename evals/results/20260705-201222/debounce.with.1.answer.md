```js
const searchInput = document.querySelector('#search');
let timeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

Each keystroke clears the previous timer and starts a new 300ms countdown. The API call only fires if the user stops typing for that duration.
