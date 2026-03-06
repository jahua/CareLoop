# Table Style Options for DOCX Conversion

## Current Approach (Markdown pipes with dashes)
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |
```
✅ **Pros:** Simple, widely supported  
❌ **Cons:** Dashes in separator row

---

## Option A: Solid Lines via Post-Processing ✅ **RECOMMENDED**

**How:** Modify `thesis_md2docx.py` to remove dashes from table borders and use solid lines in python-docx

**Change in `_set_table_borders()` method:**
```python
# Current: border.set(qn('w:val'), 'single')  # Single line
# Enhanced: Add custom style to remove dashes

# Result: Professional solid-line tables like in your PDF image
```

**Implementation:**
- Modify the `_set_table_borders()` function
- Use `w:val="single"` with proper cell shading
- Remove all background colors (already done)
- Add row height optimization

---

## Option B: Use Pandoc Grid Tables

**Markdown format:**
```
+----------+----------+
| Header 1 | Header 2 |
+==========+==========+
| Data 1   | Data 2   |
+----------+----------+
```

✅ Renders with solid borders in DOCX  
⚠️ More complex markdown syntax

---

## Option C: Use Pandoc Fancy Tables

```
┌──────────┬──────────┐
│ Header 1 │ Header 2 │
├══════════╪══════════┤
│ Data 1   │ Data 2   │
└──────────┴──────────┘
```

Similar to Grid but with Unicode characters

---

## My Recommendation: **Option A (Modify Converter)**

Current state: Tables have dashes in separator row (markdown artifact)

**Solution:**
1. The converter already removes dashes visually
2. We can make tables RENDER with solid lines by:
   - Keeping current markdown format
   - Enhancing `python-docx` post-processing
   - Setting proper border styles in DOCX XML

**Time to implement:** 20 minutes

Would you like me to implement this?

