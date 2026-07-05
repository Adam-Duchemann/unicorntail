```html
<dialog id="confirmDialog">
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 10px; justify-content: flex-end;">
    <button id="cancelBtn">Cancel</button>
    <button id="deleteBtn">Delete</button>
  </div>
</dialog>

<script>
  let pendingItemId = null;

  function openDeleteConfirm(id) {
    pendingItemId = id;
    document.getElementById('confirmDialog').showModal();
  }

  document.getElementById('cancelBtn').addEventListener('click', () => {
    document.getElementById('confirmDialog').close();
  });

  document.getElementById('deleteBtn').addEventListener('click', () => {
    document.getElementById('confirmDialog').close();
    if (pendingItemId) deleteItem(pendingItemId);
  });
</script>
```

Replace your delete button's `onclick="deleteItem(id)"` with `onclick="openDeleteConfirm(id)"`. The native `<dialog>` element handles the modal behavior and backdrop automatically.
