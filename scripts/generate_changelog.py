#!/usr/bin/env python3
"""
Generate change history log from Git commits.

Tracks all changes to structures and relationships over time.

Usage:
    python scripts/generate_changelog.py --output docs/Change-History.md
    python scripts/generate_changelog.py --days 30  # Last 30 days
"""

import sys
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Optional, Tuple

import yaml


# ============================================================================
# Git Operations
# ============================================================================

def run_git_command(args: List[str]) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return ""


def get_git_log(since_days: Optional[int] = None, max_commits: int = 100) -> List[Dict]:
    """Get git commit history."""
    args = [
        'log',
        '--pretty=format:%H|%an|%ae|%at|%s',
        f'-{max_commits}',
        '--',
        'structures/',
        'relationships/'
    ]
    
    if since_days:
        since_date = (datetime.now() - timedelta(days=since_days)).strftime('%Y-%m-%d')
        args.insert(1, f'--since={since_date}')
    
    output = run_git_command(args)
    
    commits = []
    for line in output.split('\n'):
        if not line:
            continue
        
        parts = line.split('|')
        if len(parts) >= 5:
            commits.append({
                'hash': parts[0],
                'author': parts[1],
                'email': parts[2],
                'timestamp': int(parts[3]),
                'message': '|'.join(parts[4:])  # Rejoin in case message had |
            })
    
    return commits


def get_commit_changes(commit_hash: str) -> Dict[str, List[str]]:
    """Get files changed in a commit."""
    output = run_git_command(['diff-tree', '--no-commit-id', '--name-status', '-r', commit_hash])
    
    changes = {
        'added': [],
        'modified': [],
        'deleted': []
    }
    
    for line in output.split('\n'):
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        
        status = parts[0]
        file_path = parts[1]
        
        # Only track structure/relationship files
        if not (file_path.startswith('structures/') or file_path.startswith('relationships/')):
            continue
        
        if status == 'A':
            changes['added'].append(file_path)
        elif status == 'M':
            changes['modified'].append(file_path)
        elif status == 'D':
            changes['deleted'].append(file_path)
    
    return changes


def get_file_diff(commit_hash: str, file_path: str) -> Tuple[List[str], List[str]]:
    """Get added and removed lines from a file in a commit."""
    output = run_git_command(['show', f'{commit_hash}:{file_path}'])
    
    # Try to parse as YAML to extract structure/relationship info
    added_items = []
    removed_items = []
    
    try:
        # Get the diff
        diff_output = run_git_command(['show', commit_hash, '--', file_path])
        
        # Parse diff for added/removed structures
        for line in diff_output.split('\n'):
            if line.startswith('+  - id:') or line.startswith('+  - name:'):
                match = re.search(r'(id|name):\s*(.+)', line)
                if match:
                    added_items.append(match.group(2).strip())
            elif line.startswith('-  - id:') or line.startswith('-  - name:'):
                match = re.search(r'(id|name):\s*(.+)', line)
                if match:
                    removed_items.append(match.group(2).strip())
    except Exception as e:
        print(f"Error parsing diff: {e}")
    
    return added_items, removed_items


# ============================================================================
# Change Analysis
# ============================================================================

def analyze_commit(commit: Dict) -> Dict:
    """Analyze a commit to extract meaningful changes."""
    changes = get_commit_changes(commit['hash'])
    
    analysis = {
        'commit': commit,
        'summary': {
            'files_added': len(changes['added']),
            'files_modified': len(changes['modified']),
            'files_deleted': len(changes['deleted']),
        },
        'details': changes,
        'type': 'other'
    }
    
    # Classify commit type
    msg_lower = commit['message'].lower()
    if 'structure' in msg_lower or 'add' in msg_lower:
        analysis['type'] = 'structure'
    elif 'relationship' in msg_lower or 'innervation' in msg_lower or 'supply' in msg_lower:
        analysis['type'] = 'relationship'
    elif 'fix' in msg_lower or 'correct' in msg_lower:
        analysis['type'] = 'fix'
    elif 'update' in msg_lower or 'modify' in msg_lower:
        analysis['type'] = 'update'
    elif 'remove' in msg_lower or 'delete' in msg_lower:
        analysis['type'] = 'removal'
    
    return analysis


def group_commits_by_date(commits: List[Dict]) -> Dict[str, List[Dict]]:
    """Group commits by date."""
    by_date = defaultdict(list)
    
    for commit in commits:
        dt = datetime.fromtimestamp(commit['timestamp'])
        date_str = dt.strftime('%Y-%m-%d')
        by_date[date_str].append(commit)
    
    return dict(by_date)


# ============================================================================
# Markdown Generation
# ============================================================================

def generate_changelog_markdown(commits: List[Dict], since_days: Optional[int] = None) -> str:
    """Generate markdown changelog."""
    
    if not commits:
        return "# Change History\n\nNo changes recorded.\n"
    
    # Analyze all commits
    analyses = [analyze_commit(c) for c in commits]
    
    # Group by date
    by_date = group_commits_by_date(commits)
    
    # Calculate stats
    total_commits = len(commits)
    by_type = defaultdict(int)
    by_author = defaultdict(int)
    
    for analysis in analyses:
        by_type[analysis['type']] += 1
        by_author[analysis['commit']['author']] += 1
    
    # Generate markdown
    md = f"""# Change History

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

"""
    
    if since_days:
        md += f"**Period:** Last {since_days} days\n\n"
    else:
        md += f"**Period:** Last {total_commits} commits\n\n"
    
    md += f"""## Summary

| Metric | Count |
|--------|-------|
| **Total Commits** | {total_commits} |
| **Active Contributors** | {len(by_author)} |
"""
    
    # Stats by type
    for change_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        type_name = change_type.replace('_', ' ').title()
        md += f"| {type_name} Changes | {count} |\n"
    
    md += "\n## Contributors\n\n"
    
    for author, count in sorted(by_author.items(), key=lambda x: x[1], reverse=True):
        md += f"- **{author}**: {count} commit(s)\n"
    
    md += "\n## Recent Changes\n\n"
    
    # Show changes by date (most recent first)
    for date in sorted(by_date.keys(), reverse=True):
        date_commits = by_date[date]
        
        md += f"\n### {date} ({len(date_commits)} commits)\n\n"
        
        for commit in date_commits:
            analysis = next(a for a in analyses if a['commit']['hash'] == commit['hash'])
            
            # Format commit
            short_hash = commit['hash'][:7]
            timestamp = datetime.fromtimestamp(commit['timestamp']).strftime('%H:%M')
            author = commit['author']
            message = commit['message']
            
            # Emoji by type
            emoji = {
                'structure': '📦',
                'relationship': '🔗',
                'fix': '🐛',
                'update': '♻️',
                'removal': '🗑️',
                'other': '📝'
            }.get(analysis['type'], '📝')
            
            md += f"#### {emoji} {message}\n\n"
            md += f"*By {author} at {timestamp} · [`{short_hash}`](../../commit/{commit['hash']})*\n\n"
            
            # Show file changes
            if analysis['summary']['files_added'] > 0:
                md += f"- ➕ Added {analysis['summary']['files_added']} file(s)\n"
            if analysis['summary']['files_modified'] > 0:
                md += f"- ✏️ Modified {analysis['summary']['files_modified']} file(s)\n"
            if analysis['summary']['files_deleted'] > 0:
                md += f"- ❌ Deleted {analysis['summary']['files_deleted']} file(s)\n"
            
            # List affected files
            all_files = (analysis['details']['added'] + 
                        analysis['details']['modified'] + 
                        analysis['details']['deleted'])
            
            if all_files:
                md += "\n**Files changed:**\n"
                for file in all_files[:5]:  # Limit to 5 files
                    md += f"- `{file}`\n"
                if len(all_files) > 5:
                    md += f"- *...and {len(all_files) - 5} more*\n"
            
            md += "\n"
    
    md += "\n---\n*Auto-generated change history*\n"
    
    return md


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate change history from git log")
    parser.add_argument("--output", "-o", type=str, default="docs/Change-History.md", 
                       help="Output file path")
    parser.add_argument("--days", type=int, help="Number of days to look back")
    parser.add_argument("--max-commits", type=int, default=100, 
                       help="Maximum number of commits to analyze")
    args = parser.parse_args()
    
    print("📜 Analyzing git history...")
    
    commits = get_git_log(since_days=args.days, max_commits=args.max_commits)
    
    if not commits:
        print("⚠️  No commits found")
        return 1
    
    print(f"  ✓ Found {len(commits)} commits")
    
    print("📝 Generating changelog...")
    markdown = generate_changelog_markdown(commits, since_days=args.days)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"✅ Changelog saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
