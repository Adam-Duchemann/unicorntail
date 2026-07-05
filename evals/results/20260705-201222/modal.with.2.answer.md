```html
<!-- Add this to your HTML -->
<dialog id="deleteConfirmDialog">
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px;">
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn" style="background-color: #dc2626; color: white;">Delete</button>
  </div>
</dialog>

<!-- Update your delete button to call showDeleteConfirm instead -->
<button onclick="showDeleteConfirm(itemId)">Delete</button>

<script>
let pendingDeleteId = null;

function showDeleteConfirm(id) {
  pendingDeleteId = id;
  document.getElementById('deleteConfirmDialog').showModal();
}

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('deleteConfirmDialog').close();
  pendingDeleteId = null;
});

document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
  if (pendingDeleteId !== null) {
    deleteItem(pendingDeleteId);
    document.getElementById('deleteConfirmDialog').close();
    pendingDeleteId = null;
  }
});
</script>

<style>
dialog {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 16px;
  max-width: 400px;
}

dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
```

The `<dialog>` element handles backdrop, focus trapping, and escape-key closing natively. Just swap `itemId` for your actual ID variable.
