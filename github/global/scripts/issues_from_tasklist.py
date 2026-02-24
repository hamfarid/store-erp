#!/usr/bin/env python3
# FILE: scripts/issues_from_tasklist.py | PURPOSE: Convert docs/Task_List.md to GitHub Issues | OWNER: DevOps | RELATED: docs/Task_List.md, .github/workflows/issues.yml | LAST-AUDITED: 2025-10-21

import os
import sys
import re
import requests
from typing import List, Tuple

TOKEN = os.getenv('GH_TOKEN')
REPO = os.getenv('GH_REPO')
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'

if not TOKEN or not REPO:
    print('ERROR: GH_TOKEN and GH_REPO environment variables are required', file=sys.stderr)
    sys.exit(1)

API = f'https://api.github.com/repos/{REPO}/issues'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def parse_tasks(path: str) -> List[Tuple[str, str, List[str]]]:
    """
    Parse tasks from Task_List.md
    
    Expected format:
    - [P0][FE] Task title @owner (estimate)
    - [P1][BE] Another task
    
    Returns list of (title, body, labels)
    """
    tasks = []
    
    if not os.path.exists(path):
        print(f'WARNING: {path} not found', file=sys.stderr)
        return tasks
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Match pattern: - [P0-P3][Area] Title @owner (estimate)
            m = re.match(r'^\s*-\s*\[(P[0-3])\]\[(\w+)\]\s*(.+)$', line.strip())
            if m:
                prio, area, rest = m.groups()
                
                # Extract title (before @owner or (estimate))
                title = re.split(r'\s+@|\s+\(', rest)[0].strip()
                
                # Extract owner if present
                owner_match = re.search(r'@(\w+)', rest)
                owner = owner_match.group(1) if owner_match else None
                
                # Extract estimate if present
                estimate_match = re.search(r'\(([^)]+)\)', rest)
                estimate = estimate_match.group(1) if estimate_match else None
                
                # Build body
                body_parts = [
                    f'**Priority**: {prio}',
                    f'**Area**: {area}',
                ]
                if owner:
                    body_parts.append(f'**Owner**: @{owner}')
                if estimate:
                    body_parts.append(f'**Estimate**: {estimate}')
                body_parts.append(f'\n**Source**: `docs/Task_List.md` (line {line_num})')
                
                body = '\n'.join(body_parts)
                
                # Build labels
                labels = [prio, f'area:{area.lower()}']
                
                tasks.append((title, body, labels))
    
    return tasks

def issue_exists(title: str) -> bool:
    """Check if issue with this title already exists"""
    try:
        params = {'state': 'all', 'per_page': 100}
        r = requests.get(API, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 200:
            issues = r.json()
            return any(issue['title'] == title for issue in issues)
    except Exception as e:
        print(f'WARNING: Could not check existing issues: {e}', file=sys.stderr)
    return False

def create_issue(title: str, body: str, labels: List[str]):
    """Create a GitHub issue"""
    if DRY_RUN:
        print(f'[DRY RUN] Would create issue:')
        print(f'  Title: {title}')
        print(f'  Labels: {", ".join(labels)}')
        return
    
    # Check if issue already exists
    if issue_exists(title):
        print(f'SKIP: Issue already exists: {title}')
        return
    
    try:
        payload = {
            'title': title,
            'body': body,
            'labels': labels
        }
        r = requests.post(API, headers=HEADERS, json=payload, timeout=30)
        
        if r.status_code >= 300:
            print(f'ERROR: Failed to create issue: {r.status_code} {r.text}', file=sys.stderr)
        else:
            issue_url = r.json().get('html_url')
            print(f'✅ Created: {issue_url}')
    except Exception as e:
        print(f'ERROR: Exception creating issue: {e}', file=sys.stderr)

def main():
    md_path = sys.argv[1] if len(sys.argv) > 1 else 'docs/Task_List.md'
    
    print(f'Parsing tasks from: {md_path}')
    tasks = parse_tasks(md_path)
    
    if not tasks:
        print('No tasks found in Task_List.md')
        return
    
    print(f'Found {len(tasks)} tasks')
    
    if DRY_RUN:
        print('\n🔍 DRY RUN MODE - No issues will be created\n')
    
    for title, body, labels in tasks:
        create_issue(title, body, labels)
    
    print(f'\n✅ Done. Processed {len(tasks)} tasks.')
    if not DRY_RUN:
        print(f'View issues: https://github.com/{REPO}/issues')

if __name__ == '__main__':
    main()

