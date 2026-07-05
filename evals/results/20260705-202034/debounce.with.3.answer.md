```js
const searchInput = document.querySelector('#search');

function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const debouncedSearch = debounce((value) => {
  fetch(`/api/search?q=${encodeURIComponent(value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', (e) => debouncedSearch(e.target.value));
```

300ms is a reasonable default delay; adjust to taste.
