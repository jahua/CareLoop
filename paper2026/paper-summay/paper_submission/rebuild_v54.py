# Read V5.4 header with corrected Related Work
with open('V5.4_Healthcare_Submission_FINAL.md', 'r') as f:
    v54_content = f.read()

# Find where we placed the placeholder
split_point = v54_content.find('# Materials and Methods\n\n[Rest of manuscript continues as V5.3...]')

if split_point > 0:
    # Get everything before the placeholder
    header_part = v54_content[:split_point]
    
    # Read the rest from V5.1 (from Materials and Methods onwards)
    with open('V5.1_Healthcare_Submission_ENHANCED.md', 'r') as f:
        v51_lines = f.readlines()
    
    # Find Materials and Methods in V5.1
    materials_start = None
    for i, line in enumerate(v51_lines):
        if line.startswith('# Materials and Methods'):
            materials_start = i
            break
    
    if materials_start:
        # Get everything from Materials and Methods onwards
        rest_part = ''.join(v51_lines[materials_start:])
        
        # Combine
        complete_v54 = header_part.rstrip() + '\n\n' + rest_part
        
        # Write complete V5.4
        with open('V5.4_Healthcare_Submission_FINAL.md', 'w') as f:
            f.write(complete_v54)
        
        print("✅ V5.4 FINAL completed!")
        print(f"   Total lines: {len(complete_v54.splitlines())}")
    else:
        print("❌ Could not find Materials and Methods in V5.1")
else:
    print("❌ Could not find placeholder in V5.4")
