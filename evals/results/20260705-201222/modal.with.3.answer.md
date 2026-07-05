```html
<!-- In your HTML -->
<dialog id="confirmDialog">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="deleteBtn" style="background-color: #dc2626; color: white;">Delete</button>
  </div>
</dialog>

<!-- Your delete button -->
<button onclick="showDeleteConfirm('item-id')">Delete</button>

<script>
  function showDeleteConfirm(id) {
    const dialog = document.getElementById('confirmDialog');
    
    // Update delete button to call deleteItem when confirmed
    document.getElementById('deleteBtn').onclick = () => {
      deleteItem(id);
      dialog.close();
    };
    
    document.getElementById('cancelBtn').onclick = () => {
      dialog.close();
    };
    
    dialog.showModal();
  }
  
  function deleteItem(id) {
    // Your existing delete logic
    console.log('Deleting item:', id);
  }
</script>

<style>
  dialog {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
    max-width: 320px;
  }
  
  dialog > div {
    display: flex;
    gap: 12px;
    margin-top: 24px;
    justify-content: flex-end;
  }
  
  button {
    padding: 8px 16px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  button:hover {
    background-color: #f3f4f6;
  }
  
  #deleteBtn:hover {
    background-color: #991b1b;
  }
</style>
```

Replace your current delete button's `onclick="deleteItem(id)"` with `onclick="showDeleteConfirm(id)"`. The dialog uses the native `<dialog>` element and `showModal()` for proper focus management and backdrop handling.
