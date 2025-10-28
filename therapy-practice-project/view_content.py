#!/usr/bin/env python3
"""
Content Library Viewer

Interactive viewer for browsing and previewing content in the library.
View content, metadata, and performance metrics in a user-friendly format.

Usage:
    python view_content.py
    python view_content.py --file "2025-10-27_instagram-feed_grounding-technique"
    python view_content.py --recent 10
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys


class ContentViewer:
    """Interactive content library viewer."""

    def __init__(self, library_path: Path = None):
        """Initialize the content viewer."""
        if library_path is None:
            library_path = Path(__file__).parent / "social-media-content"

        self.library_path = library_path

        if not self.library_path.exists():
            raise FileNotFoundError(
                f"Content library not found at {library_path}. "
                "Run initialize_content_library.py first."
            )

    def find_content_by_name(self, filename: str) -> Optional[Dict]:
        """Find content file by partial name match."""

        all_meta_files = list(self.library_path.rglob("*_meta.json"))

        matches = []
        for meta_file in all_meta_files:
            if filename.lower() in meta_file.name.lower():
                matches.append(meta_file)

        if not matches:
            return None

        if len(matches) > 1:
            print(f"\n⚠️  Multiple matches found:")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match.relative_to(self.library_path)}")
            print(f"\nPlease be more specific.")
            return None

        # Load content and metadata
        meta_file = matches[0]
        content_file = meta_file.parent / meta_file.name.replace("_meta.json", ".md")

        with open(meta_file, 'r') as f:
            metadata = json.load(f)

        content = None
        if content_file.exists():
            with open(content_file, 'r') as f:
                content = f.read()

        return {
            "metadata": metadata,
            "content": content,
            "metadata_file": str(meta_file),
            "content_file": str(content_file) if content_file.exists() else None
        }

    def get_recent_content(self, count: int = 10) -> List[Dict]:
        """Get most recently created content."""

        all_meta_files = list(self.library_path.rglob("*_meta.json"))

        # Sort by creation date
        content_items = []
        for meta_file in all_meta_files:
            try:
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)

                created_date = metadata.get("created_date", "")
                content_file = meta_file.parent / meta_file.name.replace("_meta.json", ".md")

                content_items.append({
                    "metadata": metadata,
                    "metadata_file": str(meta_file),
                    "content_file": str(content_file) if content_file.exists() else None,
                    "created_date": created_date
                })
            except Exception as e:
                print(f"Warning: Could not load {meta_file}: {e}")

        # Sort by date descending
        content_items.sort(key=lambda x: x["created_date"], reverse=True)

        return content_items[:count]

    def display_content(self, item: Dict, show_full_content: bool = True):
        """Display content with metadata in formatted view."""

        metadata = item["metadata"]

        print("\n" + "=" * 80)
        print("CONTENT DETAILS")
        print("=" * 80)

        # Header
        print(f"\n📄 {metadata.get('title', 'Untitled')}")
        print(f"ID: {metadata.get('content_id', 'N/A')}")
        print(f"Status: {metadata.get('status', 'Unknown').upper()}")

        # Content details
        print(f"\n{'─' * 80}")
        print("CONTENT INFORMATION")
        print(f"{'─' * 80}")

        content_details = metadata.get("content_details", {})
        print(f"Platform:       {content_details.get('platform', 'Unknown')}")
        print(f"Content Type:   {metadata.get('content_type', 'Unknown')}")
        print(f"Word Count:     {content_details.get('word_count', 0)}")
        print(f"Reading Time:   ~{content_details.get('reading_time_minutes', 0)} minutes")
        print(f"Target Audience: {content_details.get('target_audience', 'Not specified')}")

        # Scheduling
        scheduling = metadata.get("scheduling", {})
        if scheduling.get("scheduled_date"):
            print(f"\n{'─' * 80}")
            print("SCHEDULING")
            print(f"{'─' * 80}")

            try:
                scheduled_dt = datetime.fromisoformat(
                    scheduling["scheduled_date"].replace("Z", "+00:00")
                )
                print(f"Date:           {scheduled_dt.strftime('%A, %B %d, %Y')}")
                print(f"Time:           {scheduling.get('scheduled_time_local', 'Not specified')}")
                print(f"Timezone:       {scheduling.get('timezone', 'Not specified')}")
            except:
                print(f"Date:           {scheduling.get('scheduled_date', 'Not specified')}")

        # Social media details
        if metadata.get("social_media"):
            social = metadata["social_media"]
            print(f"\n{'─' * 80}")
            print("SOCIAL MEDIA")
            print(f"{'─' * 80}")

            hashtags = social.get("hashtags", [])
            if hashtags:
                print(f"Hashtags:       {' '.join(hashtags[:5])}")
                if len(hashtags) > 5:
                    print(f"                {' '.join(hashtags[5:])}")

            print(f"Has CTA:        {'Yes' if social.get('has_cta') else 'No'}")
            print(f"Visual Needed:  {social.get('visual_content_needed', 'Not specified')}")

        # SEO (for blogs)
        if metadata.get("seo"):
            seo = metadata["seo"]
            print(f"\n{'─' * 80}")
            print("SEO INFORMATION")
            print(f"{'─' * 80}")

            print(f"Primary Keyword:    {seo.get('primary_keyword', 'Not specified')}")

            secondary = seo.get("secondary_keywords", [])
            if secondary:
                print(f"Secondary Keywords: {', '.join(secondary[:3])}")

            if seo.get("meta_description"):
                print(f"Meta Description:   {seo['meta_description'][:80]}...")

        # Business context
        business = metadata.get("business_context", {})
        print(f"\n{'─' * 80}")
        print("BUSINESS CONTEXT")
        print(f"{'─' * 80}")

        print(f"Business Goal:  {business.get('business_goal', 'Not specified')}")
        print(f"Service:        {business.get('service_promoted', 'Not specified')}")
        print(f"Campaign:       {business.get('campaign', 'None')}")

        # Performance (if published)
        performance = metadata.get("performance", {})
        if performance.get("published_date"):
            print(f"\n{'─' * 80}")
            print("PERFORMANCE METRICS")
            print(f"{'─' * 80}")

            try:
                pub_dt = datetime.fromisoformat(
                    performance["published_date"].replace("Z", "+00:00")
                )
                print(f"Published:      {pub_dt.strftime('%Y-%m-%d %H:%M')}")
            except:
                print(f"Published:      {performance.get('published_date', 'Unknown')}")

            print(f"Views:          {performance.get('views', 0):,}")

            engagement = performance.get("engagement", {})
            total_engagement = sum([
                engagement.get("likes", 0),
                engagement.get("comments", 0),
                engagement.get("shares", 0),
                engagement.get("saves", 0)
            ])
            print(f"Total Engagement: {total_engagement:,}")

            if total_engagement > 0:
                print(f"  Likes:        {engagement.get('likes', 0):,}")
                print(f"  Comments:     {engagement.get('comments', 0):,}")
                print(f"  Shares:       {engagement.get('shares', 0):,}")
                print(f"  Saves:        {engagement.get('saves', 0):,}")

            conversions = performance.get("conversions", {})
            inquiries = conversions.get("inquiries_generated", 0)
            if inquiries > 0:
                print(f"\nConversions:")
                print(f"  Website Clicks: {conversions.get('website_clicks', 0)}")
                print(f"  Inquiries:      {inquiries}")
                print(f"  Bookings:       {conversions.get('bookings_attributed', 0)}")

        # Compliance
        compliance = metadata.get("compliance", {})
        print(f"\n{'─' * 80}")
        print("COMPLIANCE")
        print(f"{'─' * 80}")

        print(f"HIPAA Compliant:  {'✓' if compliance.get('hipaa_compliant') else '✗'}")
        print(f"PHI Check:        {compliance.get('phi_check', 'Not checked')}")
        print(f"Ethical Review:   {compliance.get('ethical_review', 'Pending')}")

        # Timestamps
        print(f"\n{'─' * 80}")
        print("TIMESTAMPS")
        print(f"{'─' * 80}")

        try:
            created_dt = datetime.fromisoformat(
                metadata["created_date"].replace("Z", "+00:00")
            )
            print(f"Created:        {created_dt.strftime('%Y-%m-%d %H:%M')}")
        except:
            print(f"Created:        {metadata.get('created_date', 'Unknown')}")

        print(f"Created By:     {metadata.get('created_by_agent', 'Unknown')}")

        # Files
        print(f"\n{'─' * 80}")
        print("FILES")
        print(f"{'─' * 80}")

        if item.get("content_file"):
            content_path = Path(item["content_file"])
            print(f"Content:        {content_path.relative_to(self.library_path)}")

        meta_path = Path(item["metadata_file"])
        print(f"Metadata:       {meta_path.relative_to(self.library_path)}")

        # Content preview/full
        if show_full_content and item.get("content"):
            print(f"\n{'=' * 80}")
            print("CONTENT")
            print(f"{'=' * 80}\n")
            print(item["content"])
        elif item.get("content"):
            # Show preview (first 300 characters)
            preview = item["content"][:300]
            print(f"\n{'─' * 80}")
            print("CONTENT PREVIEW")
            print(f"{'─' * 80}\n")
            print(preview)
            if len(item["content"]) > 300:
                print("\n... (use --full to see complete content)")

        print("\n" + "=" * 80 + "\n")

    def display_recent_list(self, items: List[Dict]):
        """Display list of recent content items."""

        print("\n" + "=" * 80)
        print(f"RECENT CONTENT ({len(items)} items)")
        print("=" * 80)

        for i, item in enumerate(items, 1):
            metadata = item["metadata"]

            title = metadata.get("title", "Untitled")
            status = metadata.get("status", "Unknown")
            platform = metadata.get("content_details", {}).get("platform", "Unknown")

            # Parse created date
            try:
                created_dt = datetime.fromisoformat(
                    metadata["created_date"].replace("Z", "+00:00")
                )
                created_str = created_dt.strftime("%Y-%m-%d %H:%M")
            except:
                created_str = "Unknown"

            # Status icon
            status_icons = {
                "draft": "📝",
                "scheduled": "📅",
                "published": "✅",
                "archived": "📦"
            }
            icon = status_icons.get(status, "📄")

            print(f"\n{i}. {icon} {title}")
            print(f"   Platform: {platform:10} | Status: {status:10} | Created: {created_str}")

            # Show filename for reference
            if item.get("content_file"):
                content_path = Path(item["content_file"])
                print(f"   File: {content_path.name}")

        print("\n" + "=" * 80)
        print(f"\nTo view details: python view_content.py --file <filename>")
        print("=" * 80 + "\n")


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="View and browse content library"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="View specific content file (partial name match)"
    )

    parser.add_argument(
        "--recent",
        type=int,
        default=10,
        help="Show N most recent content items (default: 10)"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Show full content (not just preview)"
    )

    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Show list without opening specific file"
    )

    args = parser.parse_args()

    # Initialize viewer
    try:
        viewer = ContentViewer()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Execute commands
    if args.file:
        # View specific file
        item = viewer.find_content_by_name(args.file)

        if item:
            viewer.display_content(item, show_full_content=args.full)
        else:
            print(f"\n❌ Content not found: {args.file}")
            print("\nTip: Try a partial filename like '2025-10-27_instagram' or just 'anxiety'")

    elif args.list_only or not args.file:
        # Show recent content list
        items = viewer.get_recent_content(count=args.recent)

        if items:
            viewer.display_recent_list(items)
        else:
            print("\n❌ No content found in library")
            print("\nCreate content with: python request_social_post.py --use-api")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
