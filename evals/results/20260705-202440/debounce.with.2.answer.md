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

The `debounce` function clears the timer on each keystroke and only fires the callback after 300ms of inactivity. Adjust the delay as needed.
