```html
<dialog id="deleteConfirmDialog">
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end;">
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn" style="background-color: #dc2626; color: white;">Delete</button>
  </div>
</dialog>

<script>
  let pendingDeleteId = null;
  const dialog = document.getElementById('deleteConfirmDialog');

  function showDeleteConfirm(id) {
    pendingDeleteId = id;
    dialog.showModal();
  }

  document.getElementById('cancelBtn').addEventListener('click', () => {
    dialog.close();
    pendingDeleteId = null;
  });

  document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
    dialog.close();
    deleteItem(pendingDeleteId);
    pendingDeleteId = null;
  });
</script>

<style>
  dialog::backdrop {
    background-color: rgba(0, 0, 0, 0.5);
  }
  dialog {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }
  dialog p {
    margin: 0 0 16px 0;
  }
  dialog button {
    padding: 8px 16px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    background-color: white;
    cursor: pointer;
  }
  dialog button:hover {
    background-color: #f3f4f6;
  }
  dialog #confirmDeleteBtn:hover {
    background-color: #b91c1c;
  }
</style>
```

Change your delete button's `onclick` from `deleteItem(id)` to `showDeleteConfirm(id)`. The dialog will open, and only calls `deleteItem()` if the user clicks Delete.
