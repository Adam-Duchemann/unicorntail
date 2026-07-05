```html
<dialog id="confirm-dialog">
  <p>This action cannot be undone.</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
```

```html
<script>
  const confirmDialog = document.getElementById('confirm-dialog');
  let pendingDeleteId = null;

  function confirmDelete(id) {
    pendingDeleteId = id;
    confirmDialog.showModal();
  }

  confirmDialog.addEventListener('close', () => {
    if (confirmDialog.returnValue === 'delete') {
      deleteItem(pendingDeleteId);
    }
    pendingDeleteId = null;
  });
</script>
```

Change your delete button from `onclick="deleteItem(id)"` to `onclick="confirmDelete(id)"`.

Uses the native `<dialog>` element (`showModal()`, `method="dialog"` buttons) — no library needed, and it gets focus trapping, Esc-to-cancel, and backdrop for free.
