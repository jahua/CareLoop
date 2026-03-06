# 📊 Workflow Version Guide

## ✅ Latest Recommended Workflow

**File**: `Phase1_Enhanced_Workflow_LATEST.json`  
**Version**: 2.0  
**Date**: October 30, 2025  
**Status**: ✅ **Production Ready**

---

## 🆕 What's New in LATEST Version

### **Key Improvements:**

1. ✅ **Database Integration**
   - Queries conversation history from database
   - Retrieves previous personality state
   - Properly persists turns and state snapshots

2. ✅ **Cleaner Node Structure**
   - Better organized node names
   - Clear execution flow
   - Improved error handling

3. ✅ **Correct Webhook Path**
   - Uses `personality-chat-enhanced` (matches API)
   - Compatible with current frontend/API setup

4. ✅ **Complete Pipeline**
   - Database queries → Ingest → Detect → Smooth → Regulate → Generate → Verify → Refine → Persist

---

## 📋 Workflow Comparison

| Feature | Phase1_Enhanced_Workflow_LATEST.json | Phase1_Enhanced_Workflow_Fixed.json |
|---------|--------------------------------------|-------------------------------------|
| **Webhook Path** | ✅ `personality-chat-enhanced` | ✅ `personality-chat-enhanced` |
| **Database Queries** | ✅ Yes (Get Latest State, Get History) | ❌ No |
| **History Retrieval** | ✅ Full conversation history | ❌ Limited |
| **State Persistence** | ✅ Complete | ⚠️ Partial |
| **Node Organization** | ✅ Clean, clear names | ⚠️ Mixed naming |
| **Error Handling** | ✅ Robust | ⚠️ Basic |
| **API Compatibility** | ✅ Full | ✅ Full |
| **Status** | **RECOMMENDED** | Legacy |

---

## 🔄 How to Import & Activate

### **Option 1: Import as New Workflow (Recommended)**

1. **Open N8N**: http://localhost:5678

2. **Import Workflow**:
   - Click "Create Workflow" → "Import from File"
   - Select: `Phase1_Enhanced_Workflow_LATEST.json`
   - Click "Open"

3. **Verify Settings**:
   - Check webhook path: `personality-chat-enhanced` ✅
   - Verify database connection settings
   - Check API key (line 69, 138, 215)

4. **Deactivate Old Workflow**:
   - Go to Workflows list
   - Find "phase1-2" or any other active workflow
   - Toggle OFF
   - Click "Save"

5. **Activate New Workflow**:
   - Open the newly imported workflow
   - Toggle "Active" to ON
   - Click "Save"

6. **Test**:
   ```bash
   cd /path/to/MVP
   ./test_now.sh
   ```

### **Option 2: Replace Existing Workflow**

1. **Export Current Active Workflow** (backup):
   ```bash
   # In N8N UI: Workflows → phase1-2 → ... → Download
   ```

2. **Delete Old Workflow**:
   - In N8N UI: Workflows → phase1-2 → Delete

3. **Import New Workflow**:
   - Follow steps from Option 1

---

## 🧪 Testing the New Workflow

### **1. Test via API Server**:
```bash
cd /Users/huaduojiejia/MyProject/hslu/2026/preliminary-studies/w9-Technical-Specifications/MVP

curl -s -X POST http://localhost:3001/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-latest-'$(date +%s)'",
    "message": "I feel very anxious and stressed"
  }' | jq '.ocean_preview'
```

**Expected Output**:
```json
{
  "O": -0.2,
  "C": 0.1,
  "E": -0.3,
  "A": 0.2,
  "N": 0.8
}
```

### **2. Test via Frontend**:
```
http://localhost:3002
```

Send message: `I feel anxious and worried`

**Expected**: Real OCEAN traits, not zeros!

### **3. Check Database Persistence**:
```bash
docker-compose exec -T postgres psql -U n8n_user -d n8n_personality_ai -c \
  "SELECT session_id, turn_index, role, LEFT(text, 50) FROM turns ORDER BY created_at DESC LIMIT 5;"
```

**Expected**: Recent conversation turns stored

---

## 📊 Workflow Architecture

### **Node Flow**:

```
1. Webhook Trigger (POST)
   ↓
2. Get Latest State (DB Query)
   ↓
3. Get Conversation History (DB Query)
   ↓
4. Ingest & Normalize
   ↓
5. Personality Detection (LLM)
   ↓
6. Smooth Personality (EMA)
   ↓
7. Generate Policy (Regulation)
   ↓
8. Generate Response (LLM)
   ↓
9. Verify Response
   ↓
10. Decision Router
    ├─ Accept → Format Response
    └─ Refine → Refine Response (LLM) → Format Response
       ↓
11. Save User Turn (DB)
12. Save Assistant Turn (DB)
13. Save State Snapshot (DB)
    ↓
14. Return Response (Webhook)
```

### **Key Improvements Over Previous Versions**:

1. **Database-First Approach**:
   - Retrieves previous state before detection
   - Enables true EMA smoothing across sessions
   - Persistent conversation history

2. **Robust Error Handling**:
   - Null checks throughout
   - Fallback values for missing data
   - Markdown fence stripping for LLM JSON

3. **Better State Management**:
   - Tracks turn index
   - Stable flag calculation
   - Confidence-weighted smoothing

---

## 🔧 Configuration Notes

### **API Keys** (Update if needed):

Lines to check:
- Line 69: Personality Detection API key
- Line 138: Response Generation API key  
- Line 215: Refinement API key

**Current**: Uses Juguang API (Gemini 1.5 Flash)

### **Database Connection**:

Uses environment variables from docker-compose:
- `DB_POSTGRESDB_HOST`: postgres
- `DB_POSTGRESDB_DATABASE`: n8n_personality_ai
- `DB_POSTGRESDB_USER`: n8n_user
- `DB_POSTGRESDB_PASSWORD`: n8n_password

### **Webhook Settings**:

- **Method**: POST
- **Path**: `personality-chat-enhanced`
- **Full URL**: `http://localhost:5678/webhook/personality-chat-enhanced`
- **Response Mode**: responseNode (Returns via "Return Response" node)

---

## 🐛 Troubleshooting

### Issue: "Webhook not registered"

**Solution**:
1. Ensure workflow is active (green toggle)
2. Restart N8N: `docker-compose restart n8n`
3. Check webhook path matches API

### Issue: "Missing body.session_id or body.message"

**Solution**:
1. Check API payload includes both fields
2. Verify webhook receives data correctly
3. Check "Ingest & Normalize" node logic

### Issue: "Cannot read properties of undefined"

**Solution**:
1. This version has robust null checks
2. Verify all nodes are connected
3. Check previous node outputs

### Issue: Database queries fail

**Solution**:
1. Ensure Postgres is running: `docker-compose ps postgres`
2. Check database credentials in N8N
3. Verify tables exist:
   ```bash
   docker-compose exec -T postgres psql -U n8n_user -d n8n_personality_ai -c "\dt"
   ```

---

## 📚 File Locations

```
Phase-1/workflows/
├── Phase1_Enhanced_Workflow_LATEST.json      ← USE THIS ONE! ✅
├── Phase1_Enhanced_Workflow_Fixed.json       ← Legacy (still works)
├── Phase1_Enhanced_Workflow_FALLBACK.json    ← Backup
├── Phase1_Enhanced_Workflow.json             ← Original
└── WORKFLOW_VERSION_GUIDE.md                 ← This file
```

---

## ✅ Migration Checklist

- [ ] Backup current active workflow
- [ ] Export database state snapshots (optional)
- [ ] Import `Phase1_Enhanced_Workflow_LATEST.json`
- [ ] Verify webhook path: `personality-chat-enhanced`
- [ ] Check API keys are set
- [ ] Connect all database nodes to Postgres
- [ ] Deactivate old workflow
- [ ] Activate new workflow
- [ ] Test with `./test_now.sh`
- [ ] Test via frontend (http://localhost:3002)
- [ ] Verify database persistence
- [ ] Monitor N8N execution logs

---

## 🎯 Summary

**Use `Phase1_Enhanced_Workflow_LATEST.json` for:**
- ✅ Production deployment
- ✅ Full database integration
- ✅ Persistent conversation state
- ✅ Robust error handling
- ✅ Complete personality pipeline

**Advantages:**
- Database-backed state retrieval
- Better conversation continuity
- Cleaner code structure
- Production-ready error handling

**Status**: ✅ **RECOMMENDED FOR ALL NEW DEPLOYMENTS**









































