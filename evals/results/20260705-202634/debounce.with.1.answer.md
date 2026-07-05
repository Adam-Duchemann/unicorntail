```js
const searchInput = document.querySelector('#search');
let debounceTimer;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  const query = e.target.value;
  debounceTimer = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```
