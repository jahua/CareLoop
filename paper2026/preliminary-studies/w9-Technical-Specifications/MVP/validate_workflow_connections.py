#!/usr/bin/env python3
import json
import sys

def validate_workflow_connections(workflow_file):
    """Validate that all nodes in the workflow are properly connected"""
    
    try:
        with open(workflow_file, 'r') as f:
            workflow = json.load(f)
    except Exception as e:
        print(f"❌ Error reading workflow: {e}")
        return False
    
    print(f"🔍 Validating workflow: {workflow.get('name', 'Unknown')}")
    print("=" * 60)
    
    # Extract nodes and connections
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    # Create a mapping of node names to their details
    node_map = {}
    for node in nodes:
        node_name = node.get('name', '')
        node_type = node.get('type', '')
        node_map[node_name] = {
            'id': node.get('id', ''),
            'type': node_type,
            'position': node.get('position', [])
        }
    
    print(f"📊 Found {len(nodes)} nodes:")
    for i, (name, details) in enumerate(node_map.items(), 1):
        print(f"   {i}. {name} ({details['type']})")
    
    print(f"\n🔗 Checking {len(connections)} connections:")
    
    # Validate each connection
    all_connected = True
    connection_count = 0
    
    for source_node, targets in connections.items():
        if source_node not in node_map:
            print(f"❌ Source node not found: {source_node}")
            all_connected = False
            continue
            
        print(f"   📤 {source_node} ->")
        
        if 'main' in targets:
            for target_list in targets['main']:
                for target in target_list:
                    target_node = target.get('node', '')
                    if target_node not in node_map:
                        print(f"      ❌ Target node not found: {target_node}")
                        all_connected = False
                    else:
                        print(f"      ✅ {target_node}")
                        connection_count += 1
    
    print(f"\n📈 Connection Summary:")
    print(f"   Total nodes: {len(nodes)}")
    print(f"   Total connections: {connection_count}")
    print(f"   Expected connections: {len(nodes) - 1} (for linear workflow)")
    
    # Check for expected workflow structure
    expected_flow = [
        "When clicking 'Execute workflow'",
        "Edit Fields", 
        "Ingest (Per-turn, no smoothing)",
        "Detect OCEAN (Discrete, Gemini 2.0 Direct)",
        "Parse Detection JSON",
        "Build Regulation Directives (Zurich Model)",
        "Generate Response (Gemini 2.0 Direct)",
        "Format Output"
    ]
    
    print(f"\n🔄 Expected Workflow Flow:")
    missing_nodes = []
    for i, expected_node in enumerate(expected_flow):
        if expected_node in node_map:
            print(f"   {i+1}. ✅ {expected_node}")
        else:
            print(f"   {i+1}. ❌ {expected_node} (MISSING)")
            missing_nodes.append(expected_node)
    
    # Validate specific critical connections
    print(f"\n🔍 Critical Connection Validation:")
    critical_connections = [
        ("When clicking 'Execute workflow'", "Edit Fields"),
        ("Edit Fields", "Ingest (Per-turn, no smoothing)"),
        ("Ingest (Per-turn, no smoothing)", "Detect OCEAN (Discrete, Gemini 2.0 Direct)"),
        ("Detect OCEAN (Discrete, Gemini 2.0 Direct)", "Parse Detection JSON"),
        ("Parse Detection JSON", "Build Regulation Directives (Zurich Model)"),
        ("Build Regulation Directives (Zurich Model)", "Generate Response (Gemini 2.0 Direct)"),
        ("Generate Response (Gemini 2.0 Direct)", "Format Output")
    ]
    
    critical_ok = True
    for source, target in critical_connections:
        if source in connections:
            connected = False
            for target_list in connections[source].get('main', []):
                for conn in target_list:
                    if conn.get('node') == target:
                        connected = True
                        break
            
            if connected:
                print(f"   ✅ {source} → {target}")
            else:
                print(f"   ❌ {source} → {target} (BROKEN)")
                critical_ok = False
        else:
            print(f"   ❌ {source} has no connections")
            critical_ok = False
    
    # Final status
    print(f"\n{'='*60}")
    if all_connected and critical_ok and not missing_nodes:
        print("🎉 ALL CONNECTIONS VALIDATED - WORKFLOW IS READY!")
        return True
    else:
        print("❌ WORKFLOW HAS ISSUES:")
        if missing_nodes:
            print(f"   Missing nodes: {', '.join(missing_nodes)}")
        if not all_connected:
            print("   Some connections reference non-existent nodes")
        if not critical_ok:
            print("   Critical workflow connections are broken")
        return False

if __name__ == "__main__":
    workflow_file = sys.argv[1] if len(sys.argv) > 1 else "Discrete_workflow_gemini_only.json"
    success = validate_workflow_connections(workflow_file)
    sys.exit(0 if success else 1)



















































