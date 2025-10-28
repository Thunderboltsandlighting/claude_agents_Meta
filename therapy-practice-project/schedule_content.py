#!/usr/bin/env python3
"""
Content Scheduling Manager

Schedule social media posts for optimal posting times based on platform best practices.
Automatically organize content into scheduled folders with proper metadata.

Usage:
    python schedule_content.py --week 2025-11-04
    python schedule_content.py --calendar
    python schedule_content.py --optimize-times
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys


class ContentScheduler:
    """Manages content scheduling and optimization."""

    def __init__(self, library_path: Path = None):
        """Initialize the content scheduler."""
        if library_path is None:
            library_path = Path(__file__).parent / "social-media-content"

        self.library_path = library_path
        self.config_path = library_path / "library_config.json"

        if not self.library_path.exists():
            raise FileNotFoundError(
                f"Content library not found at {library_path}. "
                "Run initialize_content_library.py first."
            )

        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def get_optimal_posting_times(self, platform: str, day_of_week: int) -> List[str]:
        """
        Get optimal posting times for a platform and day of week.

        Args:
            platform: Platform name (Instagram, Facebook, LinkedIn)
            day_of_week: 0=Monday, 6=Sunday

        Returns:
            List of optimal posting times in HH:MM format
        """
        optimal_times = self.config.get("optimal_posting_times", {})

        # Determine if weekday or weekend
        is_weekend = day_of_week in [5, 6]  # Saturday, Sunday
        time_key = "weekend" if is_weekend else "weekday"

        platform_times = optimal_times.get(platform, {})
        times = platform_times.get(time_key, ["09:00"])

        return times

    def create_weekly_schedule(
        self,
        week_start: str,
        themes: Dict[str, str] = None
    ) -> Dict:
        """
        Create a weekly posting schedule with optimal times.

        Args:
            week_start: Start date of week (YYYY-MM-DD)
            themes: Optional themes for each day {day: theme}

        Returns:
            Weekly schedule dictionary
        """
        start_date = datetime.fromisoformat(week_start)

        schedule = {
            "week_of": week_start,
            "created_date": datetime.now().isoformat(),
            "days": {}
        }

        # Define default posting pattern (customize as needed)
        default_pattern = {
            0: {"Instagram": 1, "LinkedIn": 1},  # Monday
            1: {"Facebook": 1, "Instagram": 1},   # Tuesday
            2: {"Instagram": 1},                  # Wednesday
            3: {"LinkedIn": 1, "Facebook": 1},    # Thursday
            4: {"Instagram": 1},                  # Friday
            5: {"Instagram": 1},                  # Saturday (optional)
            6: {}                                  # Sunday (rest day)
        }

        for day_offset in range(7):
            current_date = start_date + timedelta(days=day_offset)
            day_name = current_date.strftime("%A")
            date_str = current_date.strftime("%Y-%m-%d")

            day_schedule = {
                "date": date_str,
                "day_name": day_name,
                "theme": themes.get(day_name, None) if themes else None,
                "posts": []
            }

            # Get platforms for this day
            platforms_today = default_pattern.get(day_offset, {})

            for platform, count in platforms_today.items():
                optimal_times = self.get_optimal_posting_times(platform, day_offset)

                for i in range(count):
                    time_slot = optimal_times[i % len(optimal_times)]

                    day_schedule["posts"].append({
                        "platform": platform,
                        "time": time_slot,
                        "status": "planning",
                        "content_needed": True,
                        "content_file": None
                    })

            schedule["days"][date_str] = day_schedule

        return schedule

    def save_weekly_schedule(self, schedule: Dict) -> Path:
        """Save weekly schedule to weekly-batches folder."""

        week_start = schedule["week_of"]
        week_dt = datetime.fromisoformat(week_start)
        week_number = week_dt.isocalendar()[1]
        year = week_dt.year

        # Create weekly batch folder
        batch_folder = self.library_path / "weekly-batches" / f"{year}-week-{week_number:02d}"
        batch_folder.mkdir(parents=True, exist_ok=True)

        # Save schedule
        schedule_file = batch_folder / "weekly_schedule.json"
        with open(schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)

        # Create markdown version for easy viewing
        md_file = batch_folder / "weekly_plan.md"
        with open(md_file, 'w') as f:
            f.write(f"# Content Schedule for Week of {week_start}\n\n")
            f.write(f"**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("---\n\n")

            for date_str, day_data in sorted(schedule["days"].items()):
                f.write(f"## {day_data['day_name']} - {date_str}\n\n")

                if day_data["theme"]:
                    f.write(f"**Theme**: {day_data['theme']}\n\n")

                if day_data["posts"]:
                    f.write("**Scheduled Posts:**\n\n")
                    for post in day_data["posts"]:
                        f.write(f"- {post['time']} - {post['platform']}\n")
                        if post["content_file"]:
                            f.write(f"  - File: `{post['content_file']}`\n")
                        else:
                            f.write(f"  - Status: Content needed\n")
                    f.write("\n")
                else:
                    f.write("*No posts scheduled*\n\n")

                f.write("---\n\n")

        return schedule_file

    def display_weekly_schedule(self, schedule: Dict):
        """Display weekly schedule in readable format."""

        print("\n" + "=" * 80)
        print(f"CONTENT SCHEDULE - Week of {schedule['week_of']}")
        print("=" * 80)

        total_posts = 0

        for date_str, day_data in sorted(schedule["days"].items()):
            print(f"\n{day_data['day_name']:10} {date_str}")

            if day_data["theme"]:
                print(f"Theme: {day_data['theme']}")

            print("-" * 80)

            if day_data["posts"]:
                for post in day_data["posts"]:
                    status_icon = "✓" if post.get("content_file") else "○"
                    print(f"  {status_icon} {post['time']} | {post['platform']:10} | ", end="")

                    if post.get("content_file"):
                        print(f"{Path(post['content_file']).name}")
                    else:
                        print("Content needed")

                    total_posts += 1
            else:
                print("  (No posts scheduled)")

        print("\n" + "=" * 80)
        print(f"Total posts scheduled: {total_posts}")
        print("=" * 80 + "\n")

    def get_next_available_slot(
        self,
        platform: str,
        after_date: str = None
    ) -> Optional[Dict]:
        """
        Find next available time slot for a platform.

        Args:
            platform: Platform name
            after_date: Find slots after this date (YYYY-MM-DD)

        Returns:
            Dict with date and time, or None if no slots found
        """
        if after_date is None:
            after_date = datetime.now().strftime("%Y-%m-%d")

        after_dt = datetime.fromisoformat(after_date)

        # Look ahead 14 days
        for day_offset in range(14):
            check_date = after_dt + timedelta(days=day_offset)
            day_of_week = check_date.weekday()
            date_str = check_date.strftime("%Y-%m-%d")

            # Get optimal times for this platform/day
            optimal_times = self.get_optimal_posting_times(platform, day_of_week)

            # Check if any times are available (not already scheduled)
            # For now, just return the first optimal time
            # In production, would check against existing scheduled content
            if optimal_times:
                return {
                    "date": date_str,
                    "time": optimal_times[0],
                    "day_name": check_date.strftime("%A"),
                    "is_optimal": True
                }

        return None

    def optimize_schedule(self, schedule: Dict) -> Dict:
        """
        Optimize posting schedule based on platform best practices.

        Args:
            schedule: Existing schedule

        Returns:
            Optimized schedule
        """
        print("\nOptimizing schedule based on platform best practices...")

        optimized = schedule.copy()

        # Ensure optimal posting times
        for date_str, day_data in optimized["days"].items():
            date_dt = datetime.fromisoformat(date_str)
            day_of_week = date_dt.weekday()

            for post in day_data["posts"]:
                platform = post["platform"]
                optimal_times = self.get_optimal_posting_times(platform, day_of_week)

                # If current time is not optimal, suggest optimization
                if post["time"] not in optimal_times:
                    post["original_time"] = post["time"]
                    post["time"] = optimal_times[0]
                    post["optimized"] = True

        print("✓ Schedule optimized")

        return optimized


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="Manage content scheduling for therapy practice"
    )

    parser.add_argument(
        "--week",
        type=str,
        help="Create schedule for week starting on this date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--calendar",
        action="store_true",
        help="View upcoming scheduled content"
    )

    parser.add_argument(
        "--optimize-times",
        action="store_true",
        help="Optimize posting times for existing scheduled content"
    )

    parser.add_argument(
        "--next-slot",
        type=str,
        choices=["Instagram", "Facebook", "LinkedIn"],
        help="Find next available posting slot for platform"
    )

    parser.add_argument(
        "--theme",
        type=str,
        action="append",
        help="Add theme for specific day (format: Day:Theme, e.g., Monday:Anxiety Awareness)"
    )

    args = parser.parse_args()

    # Initialize scheduler
    try:
        scheduler = ContentScheduler()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Parse themes if provided
    themes = {}
    if args.theme:
        for theme_str in args.theme:
            if ":" in theme_str:
                day, theme = theme_str.split(":", 1)
                themes[day.strip()] = theme.strip()

    # Execute commands
    if args.week:
        # Create weekly schedule
        schedule = scheduler.create_weekly_schedule(
            week_start=args.week,
            themes=themes if themes else None
        )

        # Display schedule
        scheduler.display_weekly_schedule(schedule)

        # Save schedule
        schedule_file = scheduler.save_weekly_schedule(schedule)
        print(f"\n✓ Schedule saved to: {schedule_file.relative_to(Path.cwd())}")

    elif args.next_slot:
        # Find next available slot
        slot = scheduler.get_next_available_slot(
            platform=args.next_slot
        )

        if slot:
            print(f"\n📅 Next available {args.next_slot} slot:")
            print(f"   Date: {slot['day_name']}, {slot['date']}")
            print(f"   Time: {slot['time']}")
            if slot["is_optimal"]:
                print(f"   ✓ Optimal posting time")
        else:
            print(f"\n❌ No available slots found for {args.next_slot}")

    elif args.calendar:
        # View existing scheduled content
        print("\nViewing scheduled content calendar...")
        print("(Use manage_content_library.py --calendar for detailed view)")

    else:
        parser.print_help()
        print("\n" + "="*80)
        print("QUICK START")
        print("="*80)
        print("\nCreate a schedule for next week:")
        next_monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7)
        print(f"  python schedule_content.py --week {next_monday.strftime('%Y-%m-%d')}")
        print("\nCreate schedule with themes:")
        print(f"  python schedule_content.py --week {next_monday.strftime('%Y-%m-%d')} \\")
        print(f"    --theme 'Monday:Anxiety Awareness' \\")
        print(f"    --theme 'Wednesday:Couples Therapy Tips'")
        print("\nFind next available Instagram slot:")
        print(f"  python schedule_content.py --next-slot Instagram")
        print()


if __name__ == "__main__":
    main()
