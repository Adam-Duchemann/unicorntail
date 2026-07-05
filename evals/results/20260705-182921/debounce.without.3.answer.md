```js
const searchInput = document.querySelector('#search');
let debounceTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

Or as a reusable utility:

```js
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.querySelector('#search');
const handleSearch = debounce((value) => {
  fetch(`/api/search?q=${encodeURIComponent(value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', (e) => {
  handleSearch(e.target.value);
});
```

The first version is inline and simpler for a single use case. The second is reusable if you need debouncing elsewhere. Adjust the `300` (milliseconds) up or down based on your preference—300ms is a good starting point.
