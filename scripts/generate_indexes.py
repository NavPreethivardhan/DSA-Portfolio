#!/usr/bin/env python3
"""
scripts/generate_indexes.py
Scans all Python files in ../solutions/, extracts metadata headers,
generates ../by_topic.md, ../by_difficulty.md, updates ../README.md with progress tracking,
and creates/updates daily logs.
"""
import os
import re
import json
from collections import defaultdict
from datetime import datetime, timedelta

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOLUTIONS_DIR = os.path.join(ROOT, "solutions")
BY_TOPIC_PATH = os.path.join(ROOT, "by_topic.md")
BY_DIFF_PATH = os.path.join(ROOT, "by_difficulty.md")
README_PATH = os.path.join(ROOT, "README.md")
PROGRESS_DIR = os.path.join(ROOT, "progress")
DAILY_LOGS_DIR = os.path.join(PROGRESS_DIR, "daily_logs")
STREAK_DATA_PATH = os.path.join(ROOT, "scripts", "streak_data.json")

# Ensure directories exist
os.makedirs(DAILY_LOGS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(STREAK_DATA_PATH), exist_ok=True)

# Regex patterns for metadata
META_PATTERN = re.compile(r"^Topic:\s*(.+)$", re.MULTILINE)
DIFF_PATTERN = re.compile(r"^Difficulty:\s*(.+)$", re.MULTILINE)
TIME_PATTERN = re.compile(r"^Time:\s*(.+)$", re.MULTILINE)
NOTES_PATTERN = re.compile(r"^Notes:\s*(.+)$", re.MULTILINE)
APPROACH_PATTERN = re.compile(r"^Approach:\s*(.+)$", re.MULTILINE)

FILE_LINK_TEMPLATE = "- [{name}]({path})"


def load_streak_data():
    """Load streak tracking data from JSON file."""
    if os.path.exists(STREAK_DATA_PATH):
        with open(STREAK_DATA_PATH, 'r') as f:
            return json.load(f)
    return {
        "current_streak": 0,
        "last_solution_date": None,
        "solution_dates": []
    }


def save_streak_data(data):
    """Save streak tracking data to JSON file."""
    with open(STREAK_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def extract_metadata(filepath):
    """Read file and extract metadata fields."""
    metadata = {
        'topic': None,
        'difficulty': None,
        'time': None,
        'notes': None,
        'approach': None
    }
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read(2048)  # Read first 2KB for headers

    patterns = {
        'topic': META_PATTERN,
        'difficulty': DIFF_PATTERN,
        'time': TIME_PATTERN,
        'notes': NOTES_PATTERN,
        'approach': APPROACH_PATTERN
    }
    for key, pattern in patterns.items():
        match = pattern.search(content)
        if match:
            metadata[key] = match.group(1).strip()
    return metadata


def split_topics(topic_field):
    """Split a Topic field into a list."""
    if not topic_field:
        return []
    parts = [t.strip() for t in topic_field.split(",")]
    return [t for t in parts if t]


def get_file_creation_date(filepath):
    """Get file creation date as YYYY-MM-DD."""
    return datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d')


def scan_solutions():
    """Scan solutions directory and gather all relevant data."""
    topic_map = defaultdict(list)
    diff_map = defaultdict(list)
    solutions_by_date = defaultdict(list)

    for root, _, files in os.walk(SOLUTIONS_DIR):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            rel_dir = os.path.relpath(root, ROOT)
            rel_path = os.path.join(rel_dir, fname).replace("\\", "/")
            filepath = os.path.join(root, fname)

            metadata = extract_metadata(filepath)
            display_name = fname
            file_date = get_file_creation_date(filepath)

            solution_info = {
                'name': display_name,
                'path': rel_path,
                'date': file_date,
                'metadata': metadata
            }
            solutions_by_date[file_date].append(solution_info)

            for topic in split_topics(metadata['topic']):
                topic_map[topic].append((display_name, rel_path))
            if metadata['difficulty']:
                diff_map[metadata['difficulty']].append((display_name, rel_path))

    return topic_map, diff_map, solutions_by_date


def calculate_progress_stats(solutions_by_date, streak_data):
    """Calculate progress statistics for the current month."""
    today = datetime.now()
    current_month = today.strftime('%Y-%m')

    total_solved = sum(len(sols) for sols in solutions_by_date.values())

    month_solved = sum(
        len(sols)
        for date_str, sols in solutions_by_date.items()
        if date_str.startswith(current_month)
    )

    monthly_target = 75
    prev_month_date = (today.replace(day=1) - timedelta(days=1))
    prev_month = prev_month_date.strftime('%Y-%m')
    prev_month_solved = sum(
        len(sols)
        for date_str, sols in solutions_by_date.items()
        if date_str.startswith(prev_month)
    )
    carry_over = max(0, monthly_target - prev_month_solved)
    adjusted_target = monthly_target + carry_over

    success_rate = (month_solved / adjusted_target * 100) if adjusted_target > 0 else 0

    today_str = today.strftime('%Y-%m-%d')
    if today_str in solutions_by_date and streak_data.get('last_solution_date') != today_str:
        yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        if streak_data.get('last_solution_date') == yesterday or streak_data['current_streak'] == 0:
            streak_data['current_streak'] += 1
        else:
            streak_data['current_streak'] = 1
        streak_data['last_solution_date'] = today_str
        if today_str not in streak_data['solution_dates']:
            streak_data['solution_dates'].append(today_str)

    return {
        'total_solved': total_solved,
        'month_solved': month_solved,
        'monthly_target': adjusted_target,
        'success_rate': success_rate,
        'current_month': today.strftime('%B %Y')
    }


def generate_progress_bar(percentage):
    """Generate a GitHub-style progress bar badge."""
    pct = min(100, max(0, int(percentage)))
    return f"![Progress](https://geps.dev/progress/{pct})"


def generate_streak_display(streak_data, solutions_by_date=None):
    """
    Render a GitHub-like 4-week heatmap:
    - Columns: Mon..Sun
    - Rows: 4 recent weeks, oldest on top
    - Cell intensity from solutions per day:
        0 -> ▢ (none)
        1 -> 🟩
        2 -> 🟨
        3 -> 🟧
        4+ -> 🟥
    """
    from datetime import datetime, timedelta

    # Build counts per YYYY-MM-DD
    day_counts = {}
    if solutions_by_date:
        for d, sols in solutions_by_date.items():
            day_counts[d] = len(sols)
    else:
        for d in streak_data.get("solution_dates", []):
            day_counts[d] = max(1, day_counts.get(d, 0))

    # Helper: map count -> emoji
    def cell(c):
        if c <= 0:
            return "▢"
        if c == 1:
            return "🟩"
        if c == 2:
            return "🟨"
        if c == 3:
            return "🟧"
        return "🟥"

    # Determine the last Sunday to align columns Mon..Sun visually
    today = datetime.now().date()
    # Weekday(): Mon=0..Sun=6. We want the grid to end on Sunday to show a full last row.
    days_since_sunday = (today.weekday() - 6) % 7
    last_sunday = today - timedelta(days=days_since_sunday)

    # Build a 4-week window ending at last_sunday
    # Weeks: oldest -> newest (top to bottom)
    weeks = []
    start_of_oldest_week = last_sunday - timedelta(days=7*3 + 6)  # 4 weeks total, each 7 days, aligned Mon start
    # Align the start to Monday for consistent columns
    start_of_oldest_week -= timedelta(days=(start_of_oldest_week.weekday() % 7))  # push back to Monday

    for w in range(4):
        week_start = start_of_oldest_week + timedelta(days=7*w)
        days = []
        for i in range(7):
            d = week_start + timedelta(days=i)
            ds = d.strftime("%Y-%m-%d")
            days.append(cell(day_counts.get(ds, 0)))
        weeks.append(days)

    # Header: weekdays
    header = "M T W T F S S"

    # Join rows with spaces between cells
    grid = [header] + [" ".join(row) for row in weeks]
    grid_str = "\n".join(grid)

    legend = "Legend: ▢ None  🟩 1  🟨 2  🟧 3  🟥 4+"
    direction = "Oldest → Newest"

    current_streak = streak_data.get("current_streak", 0)

    return (
        "## 🔥 Streak & Activity\n"
        f"**Current Streak:** {current_streak} days\n\n"
        f"{grid_str}\n"
        f"{direction}\n\n"
        f"{legend}"
    )



def update_readme(progress_stats, streak_data, solutions_by_date=None):
    """Update README.md with the latest progress and streak info."""
    if not os.path.exists(README_PATH):
        return
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    progress_bar = generate_progress_bar(progress_stats['success_rate'])
    new_table = (
        "| Period               | Solved | Target | Rate (%) | Progress |\n"
        "|----------------------|-------:|-------:|---------:|----------|\n"
        f"| {progress_stats['current_month']:<20} | {progress_stats['month_solved']:>6} | "
        f"{progress_stats['monthly_target']:>6} | {progress_stats['success_rate']:>7.1f}% | {progress_bar} |\n"
        "| **Total**            | "
        f"{progress_stats['total_solved']:>6} | {progress_stats['monthly_target']:>6} | "
        f"{progress_stats['success_rate']:>7.1f}% | {progress_bar} |"
    )

    table_pattern = re.compile(r"\| Period.*?\| \*\*Total\*\*.*?\|[^\n]*", re.DOTALL)
    if table_pattern.search(content):
        content = table_pattern.sub(new_table, content)

    streak_section = generate_streak_display(streak_data, solutions_by_date=solutions_by_date)
    streak_pattern = re.compile(r"## 🔥 Streak & Activity.*?(?=## |$)", re.DOTALL)
    if streak_pattern.search(content):
        content = streak_pattern.sub(streak_section + "\n\n", content)
    else:
        content = re.sub(
            r"(## 📞 Contact)",
            streak_section + "\n\n---\n\n\\1",
            content,
            flags=re.MULTILINE
        )

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


def create_or_update_daily_log(solutions_by_date):
    """Create or update today's log in progress/daily_logs."""
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = os.path.join(DAILY_LOGS_DIR, f"{today}.md")
    todays_solutions = solutions_by_date.get(today, [])

    if not todays_solutions and os.path.exists(log_path):
        return

    content = (
        f"# Daily Log - {today}\n\n"
        f"**Date:** {datetime.now():%A, %B %d, %Y}  \n"
        f"**Problems Solved:** {len(todays_solutions)}\n\n"
        "## Solutions Added Today\n\n"
    )
    if todays_solutions:
        for sol in todays_solutions:
            md = sol['metadata']
            content += (
                f"### [{sol['name']}]({sol['path']})\n"
                f"- **Topic:** {md['topic'] or 'Not specified'}\n"
                f"- **Difficulty:** {md['difficulty'] or 'Not specified'}\n"
            )
            if md['time']:
                content += f"- **Time Spent:** {md['time']}\n"
            if md['approach']:
                content += f"- **Approach:** {md['approach']}\n"
            if md['notes']:
                content += f"- **Notes:** {md['notes']}\n"
            content += "\n"
    else:
        content += "*No solutions added today.*\n\n"

    content += (
        "## Topics Covered\n\n"
        f"{', '.join({sol['metadata']['topic'] for sol in todays_solutions if sol['metadata']['topic']}) or 'None'}\n\n"
        "## Reflections\n\n"
        "*Add your thoughts about today's practice session...*\n\n"
        "## Tomorrow's Goals\n\n"
        "*Plan for tomorrow...*\n"
    )

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_index(path, title, mapping):
    """Write a markdown index file given a mapping."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("Generated by `scripts/generate_indexes.py`\n\n")
        for key in sorted(mapping):
            f.write(f"## {key}\n")
            for name, rel_path in sorted(mapping[key]):
                f.write(f"{FILE_LINK_TEMPLATE.format(name=name, path=rel_path)}\n")
            f.write("\n")


def main():
    streak_data = load_streak_data()
    topic_map, diff_map, solutions_by_date = scan_solutions()
    progress_stats = calculate_progress_stats(solutions_by_date, streak_data)

    write_index(BY_TOPIC_PATH, "Solutions by Topic", topic_map)
    write_index(BY_DIFF_PATH, "Solutions by Difficulty", diff_map)

    update_readme(progress_stats, streak_data, solutions_by_date)
    create_or_update_daily_log(solutions_by_date)
    save_streak_data(streak_data)

    print(f"✅ Generated {BY_TOPIC_PATH} and {BY_DIFF_PATH}")
    print(f"✅ Updated {README_PATH} with progress tracking")
    print(f"✅ Updated daily log for {datetime.now():%Y-%m-%d}")
    print(
        f"📊 Progress: {progress_stats['month_solved']}/"
        f"{progress_stats['monthly_target']} "
        f"({progress_stats['success_rate']:.1f}%)"
    )
    print(f"🔥 Current streak: {streak_data['current_streak']} days")


if __name__ == "__main__":
    main()
