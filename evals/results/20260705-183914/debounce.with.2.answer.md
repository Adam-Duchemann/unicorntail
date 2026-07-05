```js
const searchInput = document.querySelector('#search');
let searchTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

Each keystroke clears the pending timeout and starts a new one. The API call fires only after 300ms of inactivity. Adjust the delay as needed for your use case.
