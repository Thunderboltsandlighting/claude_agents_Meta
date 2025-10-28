#!/usr/bin/env python3
"""
Content Library Manager

Manage, search, schedule, and track content in the therapy practice content library.

Usage:
    python manage_content_library.py --list scheduled
    python manage_content_library.py --search "anxiety"
    python manage_content_library.py --calendar --month November
    python manage_content_library.py --publish "2025-10-27_blog_anxiety-strategies"
    python manage_content_library.py --performance-report
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys


class ContentLibraryManager:
    """Manages the social media content library."""

    def __init__(self, library_path: Path = None):
        """
        Initialize the content library manager.

        Args:
            library_path: Path to the social-media-content directory
        """
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

    def list_content(
        self,
        status: str = "all",
        platform: str = "all",
        content_type: str = "all"
    ) -> List[Dict]:
        """
        List content by status, platform, and type.

        Args:
            status: draft, scheduled, published, or all
            platform: blog, instagram, facebook, linkedin, or all
            content_type: feed, reel, post, article, or all

        Returns:
            List of content items with metadata
        """
        content_items = []

        # Define search paths based on filters
        if platform == "all":
            platforms = ["blogs", "instagram", "facebook", "linkedin"]
        else:
            platforms = [platform if platform != "blog" else "blogs"]

        for platform_folder in platforms:
            platform_path = self.library_path / platform_folder

            if not platform_path.exists():
                continue

            # Get all subfolders
            subfolders = [d for d in platform_path.rglob("*") if d.is_dir()]

            for folder in subfolders:
                # Check if this matches the status filter
                if status != "all" and status not in str(folder):
                    continue

                # Find all metadata files
                meta_files = list(folder.glob("*_meta.json"))

                for meta_file in meta_files:
                    try:
                        with open(meta_file, 'r') as f:
                            metadata = json.load(f)

                        # Apply content type filter
                        if content_type != "all":
                            if content_type not in metadata.get("content_type", ""):
                                continue

                        # Get corresponding content file
                        content_file = meta_file.parent / meta_file.name.replace("_meta.json", ".md")

                        content_items.append({
                            "metadata": metadata,
                            "metadata_file": str(meta_file),
                            "content_file": str(content_file) if content_file.exists() else None,
                            "folder": str(folder.relative_to(self.library_path))
                        })

                    except Exception as e:
                        print(f"Warning: Could not load {meta_file}: {e}")

        return content_items

    def search_content(
        self,
        query: str,
        search_fields: List[str] = None
    ) -> List[Dict]:
        """
        Search content by keywords in metadata or content files.

        Args:
            query: Search query
            search_fields: Fields to search in (default: title, topic, keywords)

        Returns:
            List of matching content items
        """
        if search_fields is None:
            search_fields = ["title", "topic", "primary_keyword", "secondary_keywords"]

        all_content = self.list_content()
        matching_content = []

        query_lower = query.lower()

        for item in all_content:
            metadata = item["metadata"]

            # Search in metadata fields
            for field in search_fields:
                if field in metadata:
                    value = metadata[field]

                    # Handle string fields
                    if isinstance(value, str) and query_lower in value.lower():
                        matching_content.append(item)
                        break

                    # Handle list fields (like secondary_keywords)
                    elif isinstance(value, list):
                        if any(query_lower in str(v).lower() for v in value):
                            matching_content.append(item)
                            break

                # Search in nested fields (like seo.primary_keyword)
                elif '.' in field:
                    parts = field.split('.')
                    value = metadata
                    for part in parts:
                        value = value.get(part, {})
                        if isinstance(value, str) and query_lower in value.lower():
                            matching_content.append(item)
                            break

        return matching_content

    def get_calendar(
        self,
        month: str = None,
        year: int = None
    ) -> Dict:
        """
        Get content calendar for a specific month.

        Args:
            month: Month name (e.g., "November")
            year: Year (e.g., 2025)

        Returns:
            Dictionary organized by date with scheduled content
        """
        if month is None:
            month = datetime.now().strftime("%B")
        if year is None:
            year = datetime.now().year

        # Get all scheduled content
        scheduled_content = self.list_content(status="scheduled")

        calendar = {}

        for item in scheduled_content:
            metadata = item["metadata"]
            scheduled_date = metadata.get("scheduling", {}).get("scheduled_date")

            if scheduled_date:
                try:
                    dt = datetime.fromisoformat(scheduled_date.replace("Z", "+00:00"))

                    # Check if it matches the requested month/year
                    if dt.strftime("%B") == month and dt.year == year:
                        date_key = dt.strftime("%Y-%m-%d")

                        if date_key not in calendar:
                            calendar[date_key] = []

                        calendar[date_key].append({
                            "time": dt.strftime("%H:%M"),
                            "title": metadata.get("title", "Untitled"),
                            "platform": metadata.get("content_details", {}).get("platform", "Unknown"),
                            "content_type": metadata.get("content_type", "Unknown"),
                            "file": item["content_file"]
                        })

                except Exception as e:
                    print(f"Warning: Could not parse date for {item['metadata_file']}: {e}")

        return calendar

    def move_content(
        self,
        content_filename: str,
        to_status: str
    ) -> bool:
        """
        Move content from one status folder to another.

        Args:
            content_filename: Name of the content file (without path)
            to_status: Target status (draft, scheduled, published)

        Returns:
            True if successful, False otherwise
        """
        # Find the content
        all_content = self.list_content()

        matching_items = [
            item for item in all_content
            if content_filename in item["content_file"]
        ]

        if not matching_items:
            print(f"Error: Content '{content_filename}' not found")
            return False

        if len(matching_items) > 1:
            print(f"Error: Multiple files match '{content_filename}'. Be more specific.")
            return False

        item = matching_items[0]

        # Determine target folder
        content_file = Path(item["content_file"])
        meta_file = Path(item["metadata_file"])

        # Get platform path
        current_folder = content_file.parent
        platform_base = current_folder

        # Navigate up to find the platform base (blog, instagram/feed, etc.)
        while platform_base.parent != self.library_path:
            platform_base = platform_base.parent

        # Construct target folder
        target_folder = platform_base / to_status

        if not target_folder.exists():
            target_folder.mkdir(parents=True)

        # Move files
        try:
            new_content_path = target_folder / content_file.name
            new_meta_path = target_folder / meta_file.name

            content_file.rename(new_content_path)
            meta_file.rename(new_meta_path)

            # Update metadata status
            with open(new_meta_path, 'r') as f:
                metadata = json.load(f)

            metadata["status"] = to_status

            # If moving to published, update published date
            if to_status == "published":
                metadata["performance"]["published_date"] = datetime.now().isoformat()

            with open(new_meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"✓ Moved '{content_filename}' to {to_status}")
            print(f"  New location: {new_content_path.relative_to(self.library_path)}")

            return True

        except Exception as e:
            print(f"Error moving content: {e}")
            return False

    def get_performance_report(
        self,
        date_range: str = None
    ) -> Dict:
        """
        Generate performance report for published content.

        Args:
            date_range: Date range in format "YYYY-MM-DD:YYYY-MM-DD"

        Returns:
            Performance metrics dictionary
        """
        published_content = self.list_content(status="published")

        if date_range:
            start_date, end_date = date_range.split(":")
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)

            # Filter by date range
            filtered_content = []
            for item in published_content:
                pub_date = item["metadata"].get("performance", {}).get("published_date")
                if pub_date:
                    pub_dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                    if start_dt <= pub_dt <= end_dt:
                        filtered_content.append(item)

            published_content = filtered_content

        # Calculate aggregate metrics
        total_posts = len(published_content)
        total_views = 0
        total_engagement = 0
        total_conversions = 0

        platform_breakdown = {}
        content_type_breakdown = {}

        for item in published_content:
            metadata = item["metadata"]
            performance = metadata.get("performance", {})

            # Aggregate views
            total_views += performance.get("views", 0)

            # Aggregate engagement
            engagement = performance.get("engagement", {})
            post_engagement = sum([
                engagement.get("likes", 0),
                engagement.get("comments", 0),
                engagement.get("shares", 0),
                engagement.get("saves", 0)
            ])
            total_engagement += post_engagement

            # Aggregate conversions
            conversions = performance.get("conversions", {})
            total_conversions += conversions.get("inquiries_generated", 0)

            # Platform breakdown
            platform = metadata.get("content_details", {}).get("platform", "Unknown")
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    "posts": 0,
                    "views": 0,
                    "engagement": 0
                }

            platform_breakdown[platform]["posts"] += 1
            platform_breakdown[platform]["views"] += performance.get("views", 0)
            platform_breakdown[platform]["engagement"] += post_engagement

            # Content type breakdown
            content_type = metadata.get("content_type", "Unknown")
            if content_type not in content_type_breakdown:
                content_type_breakdown[content_type] = {
                    "posts": 0,
                    "views": 0,
                    "engagement": 0
                }

            content_type_breakdown[content_type]["posts"] += 1
            content_type_breakdown[content_type]["views"] += performance.get("views", 0)
            content_type_breakdown[content_type]["engagement"] += post_engagement

        # Calculate averages
        avg_views = total_views / total_posts if total_posts > 0 else 0
        avg_engagement = total_engagement / total_posts if total_posts > 0 else 0
        engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0

        report = {
            "period": date_range if date_range else "all_time",
            "summary": {
                "total_posts": total_posts,
                "total_views": total_views,
                "total_engagement": total_engagement,
                "total_conversions": total_conversions,
                "avg_views_per_post": round(avg_views, 2),
                "avg_engagement_per_post": round(avg_engagement, 2),
                "engagement_rate": round(engagement_rate, 2)
            },
            "by_platform": platform_breakdown,
            "by_content_type": content_type_breakdown
        }

        return report

    def display_calendar(self, calendar: Dict):
        """Display calendar in a readable format."""

        print("\n" + "=" * 70)
        print("CONTENT CALENDAR")
        print("=" * 70)

        if not calendar:
            print("\nNo scheduled content found for this month.")
            return

        for date in sorted(calendar.keys()):
            dt = datetime.fromisoformat(date)
            day_name = dt.strftime("%A")

            print(f"\n{date} ({day_name})")
            print("-" * 70)

            for post in calendar[date]:
                print(f"  {post['time']} | {post['platform']:10} | {post['title']}")

        print("\n" + "=" * 70)

    def display_content_list(self, content_items: List[Dict], title: str = "Content"):
        """Display list of content items."""

        print("\n" + "=" * 80)
        print(f"{title.upper()} ({len(content_items)} items)")
        print("=" * 80)

        if not content_items:
            print("\nNo content found.")
            return

        for item in content_items:
            metadata = item["metadata"]

            title = metadata.get("title", "Untitled")
            content_type = metadata.get("content_type", "Unknown")
            status = metadata.get("status", "Unknown")
            created = metadata.get("created_date", "Unknown")

            # Parse created date
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created_str = created_dt.strftime("%Y-%m-%d")
            except:
                created_str = created[:10] if len(created) >= 10 else "Unknown"

            print(f"\n📄 {title}")
            print(f"   Type: {content_type} | Status: {status} | Created: {created_str}")
            print(f"   File: {Path(item['content_file']).name if item['content_file'] else 'N/A'}")

            # Show scheduled date if available
            scheduled = metadata.get("scheduling", {}).get("scheduled_date")
            if scheduled:
                try:
                    scheduled_dt = datetime.fromisoformat(scheduled.replace("Z", "+00:00"))
                    scheduled_str = scheduled_dt.strftime("%Y-%m-%d %H:%M")
                    print(f"   Scheduled: {scheduled_str}")
                except:
                    pass

        print("\n" + "=" * 80)

    def display_performance_report(self, report: Dict):
        """Display performance report."""

        print("\n" + "=" * 80)
        print("PERFORMANCE REPORT")
        print("=" * 80)

        summary = report["summary"]

        print(f"\nPeriod: {report['period']}")
        print(f"\nTotal Posts: {summary['total_posts']}")
        print(f"Total Views: {summary['total_views']:,}")
        print(f"Total Engagement: {summary['total_engagement']:,}")
        print(f"Total Conversions: {summary['total_conversions']}")
        print(f"\nAverage Views per Post: {summary['avg_views_per_post']:.2f}")
        print(f"Average Engagement per Post: {summary['avg_engagement_per_post']:.2f}")
        print(f"Engagement Rate: {summary['engagement_rate']:.2f}%")

        print("\n" + "-" * 80)
        print("BY PLATFORM")
        print("-" * 80)

        for platform, metrics in report["by_platform"].items():
            print(f"\n{platform}:")
            print(f"  Posts: {metrics['posts']}")
            print(f"  Views: {metrics['views']:,}")
            print(f"  Engagement: {metrics['engagement']:,}")

        print("\n" + "-" * 80)
        print("BY CONTENT TYPE")
        print("-" * 80)

        for content_type, metrics in report["by_content_type"].items():
            print(f"\n{content_type}:")
            print(f"  Posts: {metrics['posts']}")
            print(f"  Views: {metrics['views']:,}")
            print(f"  Engagement: {metrics['engagement']:,}")

        print("\n" + "=" * 80)


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="Manage therapy practice content library"
    )

    # List content
    parser.add_argument(
        "--list",
        choices=["all", "draft", "scheduled", "published"],
        help="List content by status"
    )

    parser.add_argument(
        "--platform",
        choices=["all", "blog", "instagram", "facebook", "linkedin"],
        default="all",
        help="Filter by platform"
    )

    # Search content
    parser.add_argument(
        "--search",
        type=str,
        help="Search content by keyword"
    )

    # Calendar view
    parser.add_argument(
        "--calendar",
        action="store_true",
        help="Show content calendar"
    )

    parser.add_argument(
        "--month",
        type=str,
        help="Month for calendar (e.g., 'November')"
    )

    parser.add_argument(
        "--year",
        type=int,
        help="Year for calendar (e.g., 2025)"
    )

    # Move content
    parser.add_argument(
        "--publish",
        type=str,
        help="Move content to published (provide filename)"
    )

    parser.add_argument(
        "--schedule",
        type=str,
        help="Move content to scheduled (provide filename)"
    )

    # Performance report
    parser.add_argument(
        "--performance-report",
        action="store_true",
        help="Generate performance report"
    )

    parser.add_argument(
        "--date-range",
        type=str,
        help="Date range for report (YYYY-MM-DD:YYYY-MM-DD)"
    )

    args = parser.parse_args()

    # Initialize manager
    try:
        manager = ContentLibraryManager()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Execute commands
    if args.list:
        content = manager.list_content(status=args.list, platform=args.platform)
        manager.display_content_list(content, title=f"{args.list} content")

    elif args.search:
        content = manager.search_content(args.search)
        manager.display_content_list(content, title=f"Search results for '{args.search}'")

    elif args.calendar:
        calendar = manager.get_calendar(month=args.month, year=args.year)
        manager.display_calendar(calendar)

    elif args.publish:
        manager.move_content(args.publish, "published")

    elif args.schedule:
        manager.move_content(args.schedule, "scheduled")

    elif args.performance_report:
        report = manager.get_performance_report(date_range=args.date_range)
        manager.display_performance_report(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
