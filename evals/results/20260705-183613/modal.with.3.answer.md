```html
<!-- Dialog -->
<dialog id="deleteConfirmDialog">
  <div>
    <p>This action cannot be undone</p>
    <div>
      <button id="cancelBtn">Cancel</button>
      <button id="confirmDeleteBtn">Delete</button>
    </div>
  </div>
</dialog>

<!-- Delete button (example) -->
<button onclick="showDeleteConfirm(123)">Delete Item</button>

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
    document.getElementById('deleteConfirmDialog').close();
    deleteItem(pendingDeleteId);
    pendingDeleteId = null;
  });

  function deleteItem(id) {
    // your delete logic here
    console.log('Deleting item:', id);
  }
</script>

<style>
  dialog {
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 24px;
  }

  dialog p {
    margin: 0 0 20px 0;
    font-size: 16px;
  }

  dialog div:last-child {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }

  dialog button {
    padding: 8px 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    font-size: 14px;
  }

  dialog button:hover {
    background: #f5f5f5;
  }

  #confirmDeleteBtn {
    background: #dc2626;
    color: white;
    border-color: #dc2626;
  }

  #confirmDeleteBtn:hover {
    background: #b91c1c;
    border-color: #b91c1c;
  }
</style>
```

Change your delete button from `onclick="deleteItem(id)"` to `onclick="showDeleteConfirm(id)"`. The dialog handles the confirmation flow—if the user clicks Delete, it calls `deleteItem()`, otherwise it just closes.
