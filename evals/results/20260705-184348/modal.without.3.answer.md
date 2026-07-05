```html
<!-- Add this HTML somewhere in your page -->
<div id="confirmDialog" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
  <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); min-width: 300px;">
    <p style="margin: 0 0 24px 0; font-size: 16px;">This action cannot be undone</p>
    <div style="display: flex; gap: 12px; justify-content: flex-end;">
      <button id="confirmCancel" style="padding: 8px 16px; border: 1px solid #ccc; background: #f5f5f5; border-radius: 4px; cursor: pointer;">Cancel</button>
      <button id="confirmDelete" style="padding: 8px 16px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer;">Delete</button>
    </div>
  </div>
</div>

<script>
  let pendingDeleteId = null;

  function showDeleteConfirm(id) {
    pendingDeleteId = id;
    document.getElementById('confirmDialog').style.display = 'block';
  }

  document.getElementById('confirmCancel').addEventListener('click', () => {
    document.getElementById('confirmDialog').style.display = 'none';
    pendingDeleteId = null;
  });

  document.getElementById('confirmDelete').addEventListener('click', () => {
    document.getElementById('confirmDialog').style.display = 'none';
    deleteItem(pendingDeleteId);
    pendingDeleteId = null;
  });
</script>
```

**Then change your delete button from:**
```html
<button onclick="deleteItem(id)">Delete</button>
```

**To:**
```html
<button onclick="showDeleteConfirm(id)">Delete</button>
```

The dialog shows when delete is clicked, and only calls `deleteItem()` if the user confirms.
