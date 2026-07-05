```js
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
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

The `debounce` utility cancels the previous timeout each time the user types and only fires the API call 300ms after they stop typing. Adjust the delay (third argument) as needed—300ms is typical for search inputs.
