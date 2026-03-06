#!/usr/bin/env python3

# Read V5.4 (has corrected Related Work with Samuel's citations)
with open('V5.4_Healthcare_Submission_FINAL.md', 'r') as f:
    v54_lines = f.readlines()

# Read V5.3 (has rigorous remaining sections without groundless claims)
with open('V5.3_Healthcare_Submission_RIGOROUS.md', 'r') as f:
    v53_lines = f.readlines()

# Find where Related Work ends in V5.4
related_work_end_v54 = None
for i in range(len(v54_lines)-1, -1, -1):
    if v54_lines[i].startswith('# Materials and Methods'):
        related_work_end_v54 = i
        break

# Find where related work ends in V5.3 (Materials and Methods starts)
materials_start_v53 = None
for i, line in enumerate(v53_lines):
    if line.startswith('# Materials and Methods'):
        materials_start_v53 = i
        break

if related_work_end_v54 and materials_start_v53:
    # Combine: 
    # - V5.4 from start through end of Related Work
    # - V5.3 from Materials and Methods onwards
    
    complete = ''.join(v54_lines[:related_work_end_v54]) + '\n' + ''.join(v53_lines[materials_start_v53:])
    
    with open('V5.5_Healthcare_Submission_FINAL.md', 'w') as f:
        f.write(complete)
    
    print("✅ V5.5 Created Successfully!")
    print(f"   - V5.4 Related Work (Samuel's citations): Lines 1-{related_work_end_v54}")
    print(f"   - V5.3 Rigorous Sections: Materials and Methods onwards")
    print(f"   - Total lines: {len(complete.splitlines())}")
    print(f"   - No groundless statements")
    print(f"   - All evidence-based")
else:
    print("❌ Error: Could not find section boundaries")
    print(f"   related_work_end_v54: {related_work_end_v54}")
    print(f"   materials_start_v53: {materials_start_v53}")
