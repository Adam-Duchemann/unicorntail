Using the native `<dialog>` element — no library needed for a confirm prompt:

```html
<dialog id="confirm-dialog">
  <p>This action cannot be undone.</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
```

```js
const confirmDialog = document.getElementById('confirm-dialog');
let pendingId = null;

function confirmDelete(id) {
  pendingId = id;
  confirmDialog.showModal();
}

confirmDialog.addEventListener('close', () => {
  if (confirmDialog.returnValue === 'delete') {
    deleteItem(pendingId);
  }
  pendingId = null;
});
```

Change your delete button's handler from `deleteItem(id)` to `confirmDelete(id)`. The `method="dialog"` form auto-closes the dialog and sets `returnValue` to whichever button's `value` was clicked, so no extra click listeners are needed.

Basic centering/backdrop styling (optional):

```css
dialog::backdrop { background: rgba(0, 0, 0, 0.5); }
dialog { border: none; border-radius: 8px; padding: 1.5rem; }
```
