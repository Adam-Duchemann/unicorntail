```js
const searchInput = document.querySelector('#search');
let debounceTimer;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  
  debounceTimer = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300); // adjust delay (ms) as needed
});
```

Or as a reusable debounce function:

```js
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.querySelector('#search');

const handleSearch = debounce((e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', handleSearch);
```

The first approach is simpler for a single use case. The second is better if you need debounce elsewhere. Both delay the API call by 300ms (adjust as needed) and cancel the previous timer if the user types again before it fires.
