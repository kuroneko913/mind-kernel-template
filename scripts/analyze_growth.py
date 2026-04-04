import argparse
import subprocess
import json
import os
from typing import Dict, List, Any, Optional, Tuple

def run_git_command(command: List[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_json_at_commit(commit_hash: str, file_path: str) -> Dict[str, Any]:
    try:
        content = run_git_command(["git", "show", f"{commit_hash}:{file_path}"])
        data = json.loads(content)
        return data.get("body", data) if isinstance(data, dict) else data
    except subprocess.CalledProcessError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_local_json(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("body", data) if isinstance(data, dict) else data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def extract_rich_context(data: Any) -> str:
    """
    Extracts a human-readable summary from a dictionary (description, name, values).
    Returns a string representation.
    """
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return ", ".join([str(x) for x in data])
    if isinstance(data, dict):
        context = []
        if "name" in data:
            context.append(f"Name: {data['name']}")
        if "description" in data:
            context.append(f"Description: {data['description']}")
        if "definitions" in data:
             context.append(f"Definition: {data['definitions']}")
        if "values" in data:
            context.append(f"Values: {', '.join(data['values']) if isinstance(data['values'], list) else data['values']}")
        if "signals" in data:
            signals = data['signals']
            if isinstance(signals, list):
                context.append(f"Signals: {', '.join(signals)}")
            else:
                context.append(f"Signals: {signals}")
        
        # If no specific semantic keys found, dump the whole thing if it's small, else just keys
        if not context:
            return json.dumps(data, ensure_ascii=False, indent=2)
        
        return " | ".join(context)
    return str(data)


METADATA_KEYS = {"version", "schema", "$schema", "id", "description", "_guidelines"}

def _find_changes_recursive(old: Any, new: Any, path: str, changes: List[Dict[str, Any]]) -> None:
    """
    Helper function to traverse and compare two JSON objects.
    """
    # 1. Handle Leaf Nodes (Non-dict comparisons)
    if not (isinstance(old, dict) and isinstance(new, dict)):
        if old != new:
             changes.append({
                "type": "MODIFIED",
                "key": path,
                "old": old,
                "new": new,
                "context": f"{old} -> {new}"
             })
        return

    # 2. Dictionary Comparison (Recursive)
    all_keys = set(old.keys()) | set(new.keys())
    
    for key in all_keys:
        if key in METADATA_KEYS:
            continue

        new_path = f"{path}.{key}" if path else key

        # Case A: Added
        if key not in old:
            changes.append({
                "type": "ADDED",
                "key": new_path,
                "value": new[key],
                "context": extract_rich_context(new[key])
            })
            continue

        # Case B: Removed (ignored for growth report)
        if key not in new:
            continue
            
        # Case C: Both exist -> Recurse
        _find_changes_recursive(old[key], new[key], new_path, changes)

def detailed_semantic_diff(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Recursively compares two dictionaries to find significant additions and changes.
    Returns a flat list of change events.
    """
    changes = []
    _find_changes_recursive(old_data, new_data, "", changes)
    return changes

def analyze_growth_semantics(since_commit: str):
    print(f"Analyzing semantic growth since commit: {since_commit}")
    
    files_to_analyze = [
        ("kernel/patterns.json", "Capabilities & Skills"),
        ("kernel/identity.json", "Mindset & Values"),
        ("kernel/meta.json", "System & Meta"),
    ]

    report = {}

    for file_path, category_label in files_to_analyze:
        old_json = get_json_at_commit(since_commit, file_path)
        new_json = get_local_json(file_path)
        
        changes = detailed_semantic_diff(old_json, new_json)
        if changes:
             report[category_label] = changes
    
    return report


def _format_added_items(items: List[Dict[str, Any]]) -> str:
    if not items:
        return ""
    
    md = "### 🆕 New Acquisitions\n"
    for item in items:
        # Heuristic: If it's a leaf node addition (value is str/int), it might be a property of an existing item.
        # If it's a dict addition, it's likely a new concept.
        
        key_name = item['key'].split('.')[-1]
        full_key = item['key']
        
        # Indent based on depth or just list
        if isinstance(item['value'], dict):
            md += f"- **{key_name}** (`{full_key}`)\n"
            # Add description/context block
            context = item['context']
            if context:
                # Replace | separator with newlines for better readability
                formatted_context = context.replace(" | ", "\n  - ")
                md += f"  - {formatted_context}\n"
        else:
                md += f"- **{key_name}**: {item['value']}\n"
    return md

def _format_modified_items(items: List[Dict[str, Any]]) -> str:
    if not items:
        return ""
    
    md = "\n### 🔄 Updates & Shifts\n"
    for item in items:
        key_name = item['key'].split('.')[-1]
        # Show semantic changes
        md += f"- **{key_name}**: {item['context']}\n"
    return md

def generate_rich_markdown(report: Dict[str, List[Dict[str, Any]]], duration_label: str):
    md = f"# Mind Kernel Growth Report ({duration_label})\n\n"
    
    for category, changes in report.items():
        if not changes:
            continue
            
        md += f"## {category}\n"
        
        added_items = [c for c in changes if c['type'] == 'ADDED']
        modified_items = [c for c in changes if c['type'] == 'MODIFIED']
        
        md += _format_added_items(added_items)
        md += _format_modified_items(modified_items)
        
        md += "\n"
        
    return md


def resolve_commit_from_date(date_spec: str) -> str:
    """
    Resolves a date specification (e.g. '1 month ago', '2023-01-01') to a commit hash.
    """
    try:
        # git rev-list -n 1 --before="1 month ago" HEAD
        cmd = ["git", "rev-list", "-n", "1", f"--before={date_spec}", "HEAD"]
        return run_git_command(cmd)
    except Exception:
        return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Mind Kernel growth using semantic JSON diffs.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--commit", help="The commit hash to compare against (e.g., 5e20e22)")
    group.add_argument("--since", help="Natural language date to compare against (e.g., '1 week ago', '2025-12-01')")
    
    parser.add_argument("--label", help="Label for the time duration (optional, auto-generated if using --since)")

    args = parser.parse_args()
    
    target_commit = args.commit
    label = args.label
    
    if args.since:
        found_commit = resolve_commit_from_date(args.since)
        if not found_commit:
            print(f"Error: Could not find a commit for date specification '{args.since}'")
            exit(1)
        target_commit = found_commit
        if not label:
            label = f"Since {args.since}"
            
    if not label:
        label = f"Since {target_commit[:7]}"

    try:
        growth_data = analyze_growth_semantics(target_commit)
        report_md = generate_rich_markdown(growth_data, label)
        print(report_md)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
