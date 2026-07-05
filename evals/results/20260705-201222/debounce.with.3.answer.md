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

The timeout clears and resets on each keystroke, so the fetch only fires 300ms after the user stops typing. Adjust the delay as needed.
