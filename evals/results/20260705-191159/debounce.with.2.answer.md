```js
const debounce = (fn, delay) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
};

const searchInput = document.querySelector('#search');
const handleSearch = debounce((e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', handleSearch);
```

The debounce function cancels pending calls and queues a new one each keystroke; only the final call within 300ms fires. Adjust the delay as needed.
