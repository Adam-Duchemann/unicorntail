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

Wraps the fetch in a 300ms timeout. Each keystroke clears the previous timeout and starts a new one, so the API call only fires after the user stops typing for 300ms.
