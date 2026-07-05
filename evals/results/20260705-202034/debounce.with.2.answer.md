```js
const searchInput = document.querySelector('#search');
let debounceTimer;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  const value = e.target.value;
  debounceTimer = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```
