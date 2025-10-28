#!/usr/bin/env python3
"""
Update Performance Data for Posts

Simple script to update post performance metrics after publishing.

Usage:
    python update_performance.py --file "adhd" --views 1250 --likes 87 --comments 12
    python update_performance.py --search "anxiety" --views 950 --likes 65
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import sys


def find_content_metadata(search_term: str, library_path: Path) -> Path:
    """Find metadata file by search term."""

    # Search for metadata files
    meta_files = list(library_path.rglob("*_meta.json"))

    matches = []
    for meta_file in meta_files:
        if search_term.lower() in meta_file.name.lower():
            matches.append(meta_file)

    if not matches:
        print(f"❌ No content found matching: {search_term}")
        return None

    if len(matches) > 1:
        print(f"❌ Multiple matches found:")
        for i, match in enumerate(matches, 1):
            print(f"  {i}. {match.relative_to(library_path)}")
        print("\nPlease be more specific.")
        return None

    return matches[0]


def update_performance(
    meta_file: Path,
    views: int = None,
    likes: int = None,
    comments: int = None,
    shares: int = None,
    saves: int = None,
    website_clicks: int = None,
    inquiries: int = None,
    bookings: int = None,
    published_url: str = None,
    mark_published: bool = False
) -> bool:
    """Update performance metrics in metadata file."""

    try:
        # Load existing metadata
        with open(meta_file, 'r') as f:
            metadata = json.load(f)

        # Update performance section
        performance = metadata.get("performance", {})

        if mark_published and not performance.get("published_date"):
            performance["published_date"] = datetime.now().isoformat() + "Z"
            metadata["status"] = "published"

        if published_url:
            performance["published_url"] = published_url

        if views is not None:
            performance["views"] = views

        engagement = performance.get("engagement", {})
        if likes is not None:
            engagement["likes"] = likes
        if comments is not None:
            engagement["comments"] = comments
        if shares is not None:
            engagement["shares"] = shares
        if saves is not None:
            engagement["saves"] = saves

        performance["engagement"] = engagement

        conversions = performance.get("conversions", {})
        if website_clicks is not None:
            conversions["website_clicks"] = website_clicks
        if inquiries is not None:
            conversions["inquiries_generated"] = inquiries
        if bookings is not None:
            conversions["bookings_attributed"] = bookings

        performance["conversions"] = conversions

        metadata["performance"] = performance

        # Add to version history
        if "version_history" not in metadata:
            metadata["version_history"] = []

        metadata["version_history"].append({
            "version": len(metadata["version_history"]) + 1,
            "date": datetime.now().isoformat(),
            "changes": "Updated performance metrics",
            "modified_by": "manual-update"
        })

        # Save updated metadata
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        return True

    except Exception as e:
        print(f"❌ Error updating metadata: {e}")
        return False


def display_performance(meta_file: Path):
    """Display current performance metrics."""

    with open(meta_file, 'r') as f:
        metadata = json.load(f)

    print("\n" + "=" * 70)
    print("CURRENT PERFORMANCE METRICS")
    print("=" * 70)

    print(f"\n📄 {metadata.get('title', 'Untitled')}")
    print(f"Platform: {metadata.get('content_details', {}).get('platform', 'Unknown')}")
    print(f"Status: {metadata.get('status', 'Unknown').upper()}")

    performance = metadata.get("performance", {})

    # Published info
    pub_date = performance.get("published_date")
    if pub_date:
        try:
            dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            print(f"Published: {dt.strftime('%Y-%m-%d %H:%M')}")
        except:
            print(f"Published: {pub_date}")
    else:
        print("Published: Not yet published")

    pub_url = performance.get("published_url")
    if pub_url:
        print(f"URL: {pub_url}")

    # Engagement metrics
    print(f"\n📊 Engagement:")
    print(f"  Views:    {performance.get('views', 0):,}")

    engagement = performance.get("engagement", {})
    print(f"  Likes:    {engagement.get('likes', 0):,}")
    print(f"  Comments: {engagement.get('comments', 0):,}")
    print(f"  Shares:   {engagement.get('shares', 0):,}")
    print(f"  Saves:    {engagement.get('saves', 0):,}")

    total_engagement = sum([
        engagement.get('likes', 0),
        engagement.get('comments', 0),
        engagement.get('shares', 0),
        engagement.get('saves', 0)
    ])
    print(f"  TOTAL:    {total_engagement:,}")

    # Engagement rate
    views = performance.get('views', 0)
    if views > 0:
        engagement_rate = (total_engagement / views) * 100
        print(f"  Rate:     {engagement_rate:.2f}%")

    # Conversions
    conversions = performance.get("conversions", {})
    clicks = conversions.get("website_clicks", 0)
    inquiries = conversions.get("inquiries_generated", 0)
    bookings = conversions.get("bookings_attributed", 0)

    if clicks > 0 or inquiries > 0 or bookings > 0:
        print(f"\n💼 Conversions:")
        print(f"  Website Clicks: {clicks}")
        print(f"  Inquiries:      {inquiries}")
        print(f"  Bookings:       {bookings}")

    print("\n" + "=" * 70 + "\n")


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="Update post performance metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Update basic engagement
  python update_performance.py --file "adhd" --views 1250 --likes 87 --comments 12

  # Update all metrics including conversions
  python update_performance.py --file "anxiety" \\
    --views 950 --likes 65 --comments 8 --shares 3 --saves 22 \\
    --website-clicks 15 --inquiries 2 --bookings 1

  # Mark as published with URL
  python update_performance.py --file "adhd" \\
    --mark-published \\
    --url "https://instagram.com/p/abc123"

  # View current performance
  python update_performance.py --file "adhd" --show
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Content file to update (partial name match)"
    )

    parser.add_argument(
        "--views",
        type=int,
        help="Total views/reach"
    )

    parser.add_argument(
        "--likes",
        type=int,
        help="Number of likes"
    )

    parser.add_argument(
        "--comments",
        type=int,
        help="Number of comments"
    )

    parser.add_argument(
        "--shares",
        type=int,
        help="Number of shares"
    )

    parser.add_argument(
        "--saves",
        type=int,
        help="Number of saves/bookmarks"
    )

    parser.add_argument(
        "--website-clicks",
        type=int,
        help="Clicks to website/profile"
    )

    parser.add_argument(
        "--inquiries",
        type=int,
        help="Inquiries/DMs generated"
    )

    parser.add_argument(
        "--bookings",
        type=int,
        help="Therapy bookings attributed to this post"
    )

    parser.add_argument(
        "--url",
        type=str,
        help="Published post URL"
    )

    parser.add_argument(
        "--mark-published",
        action="store_true",
        help="Mark content as published with current timestamp"
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current performance without updating"
    )

    args = parser.parse_args()

    # Find content
    library_path = Path(__file__).parent / "social-media-content"
    meta_file = find_content_metadata(args.file, library_path)

    if not meta_file:
        sys.exit(1)

    print(f"\n✓ Found: {meta_file.relative_to(Path(__file__).parent)}")

    # Show current performance if requested
    if args.show:
        display_performance(meta_file)
        sys.exit(0)

    # Update performance
    success = update_performance(
        meta_file=meta_file,
        views=args.views,
        likes=args.likes,
        comments=args.comments,
        shares=args.shares,
        saves=args.saves,
        website_clicks=args.website_clicks,
        inquiries=args.inquiries,
        bookings=args.bookings,
        published_url=args.url,
        mark_published=args.mark_published
    )

    if success:
        print("\n✅ Performance data updated successfully!\n")
        display_performance(meta_file)
    else:
        print("\n❌ Failed to update performance data\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
