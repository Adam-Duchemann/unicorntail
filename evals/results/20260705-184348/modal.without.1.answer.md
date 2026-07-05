```html
<!-- Add this modal HTML to your page -->
<div id="confirmDialog" class="modal" style="display: none;">
  <div class="modal-content">
    <p>This action cannot be undone</p>
    <div class="modal-buttons">
      <button id="cancelBtn" class="btn-cancel">Cancel</button>
      <button id="confirmBtn" class="btn-delete">Delete</button>
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 300px;
}

.modal-content p {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: #333;
}

.modal-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel,
.btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn-cancel {
  background: #e5e7eb;
  color: #374151;
}

.btn-cancel:hover {
  background: #d1d5db;
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
}
</style>

<script>
let pendingDeleteId = null;

function showDeleteConfirmation(id) {
  pendingDeleteId = id;
  document.getElementById('confirmDialog').style.display = 'flex';
}

document.getElementById('cancelBtn').addEventListener('click', function() {
  document.getElementById('confirmDialog').style.display = 'none';
  pendingDeleteId = null;
});

document.getElementById('confirmBtn').addEventListener('click', function() {
  if (pendingDeleteId !== null) {
    deleteItem(pendingDeleteId);
    document.getElementById('confirmDialog').style.display = 'none';
    pendingDeleteId = null;
  }
});
</script>
```

Change your delete button from `onclick="deleteItem(id)"` to `onclick="showDeleteConfirmation(id)"`.
