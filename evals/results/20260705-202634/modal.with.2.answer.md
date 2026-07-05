Using the native `<dialog>` element (no custom modal component needed):

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

function requestDelete(id) {
  pendingDeleteId = id;
  confirmDeleteDialog.showModal();
}

confirmDeleteDialog.addEventListener('close', () => {
  if (confirmDeleteDialog.returnValue === 'delete' && pendingDeleteId != null) {
    deleteItem(pendingDeleteId);
  }
  pendingDeleteId = null;
});
```

Change your delete button's `onclick="deleteItem(id)"` to `onclick="requestDelete(id)"`. The dialog handles Cancel, Delete, click-outside, and Escape automatically via the native `close` event and `returnValue`.
