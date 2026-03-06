# 🧪 **Testing Manual Trigger - Complete Guide**

## ⚠️ **Current Issue**

The error shows:
```sql
VALUES ('', 1, false, 'active')
        ^^
        Empty session_id
```

This means the `session_id` from "Edit Fields" isn't reaching the "Save Session" node.

## 🔧 **What I Fixed**

1. Added `"turn_index": 1` to the Edit Fields input data
2. The Edit Fields node already has the correct session_id: `"550e8400-e29b-41d4-a716-446655440002"`

## 📋 **Re-import and Test Steps**

### 1. Delete Old Workflow
1. Go to N8N: http://localhost:5678
2. Find and delete "phase1-2-postgres" workflow

### 2. Import Fixed Workflow
1. Click "Import from File"
2. Select: `Phase-1/workflows/phase1-2-postgres-manual.json`
3. Import

### 3. Verify the Manual Trigger Setup
After importing, check the "Edit Fields" node:
- Click on "Edit Fields" node
- Verify it shows:
  ```json
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "turn_index": 1,
    "evaluation_mode": true,
    "baseline_comparison": true,
    "messages": [...]
  }
  ```

### 4. Test with Debug
Before running the full workflow, test each node individually:

#### Step 1: Test "Edit Fields" Node
1. Click on "Edit Fields" node
2. Click "Test step" or "Execute node"
3. Check output - should show the session_id

#### Step 2: Test "Enhanced Ingest" Node
1. After Edit Fields works, click "Enhanced Ingest"
2. Click "Test step"
3. Check output - should show `session_id: "550e8400-e29b-41d4-a716-446655440002"`

### 5. Run Full Workflow
1. Click "Test workflow" (top right)
2. Monitor each node execution
3. Check for errors

## 🔍 **If Session ID is Still Empty**

The issue might be how the "Enhanced Ingest" node reads the data. Let me check what it's receiving:

### Debug in N8N:
1. Click on "Enhanced Ingest (Zurich)" node
2. Look at the INPUT data (not output)
3. It should show:
   ```json
   {
     "session_id": "550e8400-e29b-41d4-a716-446655440002",
     "turn_index": 1,
     ...
   }
   ```

If the INPUT is empty or doesn't have session_id, then the connection between "Edit Fields" and "Enhanced Ingest" is broken.

## 🎯 **Alternative: Use Webhook Instead**

If the manual trigger keeps having issues, test via webhook instead:

### 1. Activate the Workflow
Toggle it to "Active"

### 2. Test via Curl
```bash
curl -X POST http://localhost:5678/webhook/personality-chat-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "turn_index": 1,
    "message": "I feel overwhelmed and anxious about work deadlines"
  }' | jq .
```

This bypasses the manual trigger setup and tests the webhook directly.

## ✅ **Expected Successful Result**

When it works, you should see:
1. ✅ Edit Fields: Outputs session_id
2. ✅ Enhanced Ingest: Receives and processes session_id
3. ✅ Load Previous State: Uses session_id in SQL query
4. ✅ Save Session: Inserts with valid UUID (not empty string)
5. ✅ Final output: Complete JSON with personality data

## 🐛 **Troubleshooting**

### If session_id is still ''
Check the Enhanced Ingest node code line:
```javascript
const inputData = $json.body || $json || {};
```

It should fall back to `$json` which contains the Edit Fields output.

### Manual Trigger Alternative
If Edit Fields isn't working, try switching to a simple "Set" node with explicit mapping:
1. Delete "Edit Fields" node
2. Add new "Set" node (n8n-nodes-base.set)
3. Use "Manual" mode with explicit fields:
   - session_id = "550e8400-e29b-41d4-a716-446655440002"
   - turn_index = 1
   - messages = [array]

---

**Next Action**: Re-import the workflow and check if Edit Fields → Enhanced Ingest connection works! 🚀









































