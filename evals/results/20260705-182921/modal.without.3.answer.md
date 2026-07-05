```html
<!-- Modal HTML (add to your page) -->
<div id="deleteModal" class="modal" style="display: none;">
  <div class="modal-content">
    <p>This action cannot be undone</p>
    <div class="modal-buttons">
      <button id="cancelBtn" class="btn-cancel">Cancel</button>
      <button id="deleteBtn" class="btn-delete">Delete</button>
    </div>
  </div>
</div>

<style>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 24px;
    border-radius: 8px;
    min-width: 300px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .modal-content p {
    margin: 0 0 20px 0;
    color: #333;
  }
  
  .modal-buttons {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }
  
  .btn-cancel, .btn-delete {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .btn-cancel {
    background: #e5e7eb;
    color: #374151;
  }
  
  .btn-cancel:hover {
    background: #d1d5db;
  }
  
  .btn-delete {
    background: #dc2626;
    color: white;
  }
  
  .btn-delete:hover {
    background: #b91c1c;
  }
</style>

<script>
  let pendingDeleteId = null;
  
  function confirmDelete(id) {
    pendingDeleteId = id;
    document.getElementById('deleteModal').style.display = 'flex';
  }
  
  document.getElementById('cancelBtn').addEventListener('click', () => {
    document.getElementById('deleteModal').style.display = 'none';
    pendingDeleteId = null;
  });
  
  document.getElementById('deleteBtn').addEventListener('click', () => {
    if (pendingDeleteId !== null) {
      deleteItem(pendingDeleteId);
      document.getElementById('deleteModal').style.display = 'none';
      pendingDeleteId = null;
    }
  });
</script>
```

**Update your delete button:**
```html
<!-- Instead of: onclick="deleteItem(123)" -->
<button onclick="confirmDelete(123)">Delete</button>
```

The modal shows on `confirmDelete(id)`, stores the ID, and only calls `deleteItem()` if the user clicks Delete.
