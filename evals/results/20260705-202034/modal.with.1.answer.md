```html
<dialog id="confirmDeleteDialog">
  <p>This action cannot be undone.</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="delete" id="confirmDeleteBtn">Delete</button>
  </form>
</dialog>
```

```js
const confirmDeleteDialog = document.getElementById('confirmDeleteDialog');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
let pendingDeleteId = null;

function confirmDelete(id) {
  pendingDeleteId = id;
  confirmDeleteDialog.showModal();
}

confirmDeleteDialog.addEventListener('close', () => {
  if (confirmDeleteDialog.returnValue === 'delete' && pendingDeleteId !== null) {
    deleteItem(pendingDeleteId);
  }
  pendingDeleteId = null;
});
```

Replace the delete button's `onclick="deleteItem(id)"` with `onclick="confirmDelete(id)"`. Uses the native `<dialog>` element (built into every modern browser) instead of a custom modal — no CSS/JS modal library needed.
