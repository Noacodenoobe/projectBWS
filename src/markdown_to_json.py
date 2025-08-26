"""
Converts a Markdown report with an 'Action Items' table into a JSON array for further use.
Usage: python src/markdown_to_json.py data/sample_report.md data/sample_tasks.json
"""

import sys
import re
import json

def extract_action_items(md_content):
    # Simple parser for Markdown table (assumes standard format)
    table_regex = r"\| *Zadanie *\| *Kto\? *\| *Kiedy\? *\| *Priorytet *\|([\s\S]+?)\n\n"
    match = re.search(table_regex, md_content)
    if not match:
        return []
    rows = match.group(1).strip().split('\n')
    items = []
    for row in rows:
        cols = [c.strip() for c in row.strip('|').split('|')]
        if len(cols) != 4: continue
        items.append({
            "title": cols[0] if cols[0] else None,
            "assignee": cols[1] if cols[1] else None,
            "due_date": cols[2] if cols[2] else None,
            "priority": cols[3] if cols[3] else None,
        })
    return items

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/markdown_to_json.py <input_md> <output_json>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding='utf-8') as f:
        md_content = f.read()
    items = extract_action_items(md_content)
    with open(sys.argv[2], "w", encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(items)} items to {sys.argv[2]}")