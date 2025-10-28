#!/usr/bin/env python3
"""
Create Optimized Content

Uses your performance learnings to create content that's more likely to perform well.

Usage:
    python create_optimized_content.py --topic "Your topic"
    python create_optimized_content.py --auto-suggest
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys


class OptimizedContentCreator:
    """Create content optimized based on performance learnings."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.profile_path = self.project_root / "performance_profile.json"

    def load_profile(self) -> dict:
        """Load performance profile."""
        if not self.profile_path.exists():
            print("⚠️  No performance profile found yet.")
            print("   Run weekly check-ins to build performance insights!")
            return None

        with open(self.profile_path, 'r') as f:
            return json.load(f)

    def show_recommendations(self, profile: dict):
        """Display content recommendations."""

        print("\n" + "=" * 70)
        print("🎯 CONTENT RECOMMENDATIONS (Based on Your Performance)")
        print("=" * 70)

        learnings = profile.get("learnings", {})
        total_checkins = profile.get("total_checkins", 0)

        if total_checkins == 0:
            print("\n⚠️  No check-ins completed yet.")
            print("   Complete weekly check-ins to get personalized recommendations!")
            return

        print(f"\n📊 Based on {total_checkins} week(s) of data:\n")

        # Top topics
        topics = learnings.get("topics", {})
        if topics:
            print("📝 TOPICS THAT WORK:")
            sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
            for topic, count in sorted_topics[:3]:
                confidence = "🔥" if count >= 3 else "💡"
                print(f"   {confidence} {topic} (performed well {count}x)")

        # Best platforms
        platforms = learnings.get("platforms", {})
        if platforms:
            print("\n📱 BEST PLATFORMS:")
            sorted_platforms = sorted(platforms.items(), key=lambda x: x[1], reverse=True)
            for platform, count in sorted_platforms:
                confidence = "🔥" if count >= 3 else "💡"
                print(f"   {confidence} {platform} (top performer {count}x)")

        # Content styles
        styles = learnings.get("content_styles", {})
        if styles:
            print("\n✨ CONTENT STYLES THAT WORK:")
            sorted_styles = sorted(styles.items(), key=lambda x: x[1], reverse=True)
            style_descriptions = {
                "educational": "Educational/How-to (actionable tips)",
                "personal": "Personal/Relatable (stories)",
                "inspirational": "Inspirational/Motivational",
                "informational": "Informational (research-based)"
            }
            for style, count in sorted_styles:
                confidence = "🔥" if count >= 2 else "💡"
                desc = style_descriptions.get(style, style)
                print(f"   {confidence} {desc} (worked {count}x)")

        # Timing patterns
        timing = learnings.get("timing", {})
        if timing:
            print("\n⏰ BEST POSTING TIMES:")
            sorted_timing = sorted(timing.items(), key=lambda x: x[1], reverse=True)
            timing_descriptions = {
                "mid_week": "Tuesday-Thursday",
                "early_week": "Monday-Tuesday",
                "weekend": "Saturday-Sunday"
            }
            for time_pattern, count in sorted_timing[:1]:
                desc = timing_descriptions.get(time_pattern, time_pattern)
                print(f"   🔥 {desc} (performed best)")

        # Inquiry-generating topics
        inquiry_topics = learnings.get("inquiry_generating_topics", [])
        if inquiry_topics:
            print("\n💼 TOPICS THAT GENERATE INQUIRIES:")
            unique_topics = list(set(inquiry_topics))[:3]
            for topic in unique_topics:
                print(f"   💰 {topic}")

        print("\n" + "=" * 70)

    def suggest_topics(self, profile: dict) -> list:
        """Suggest topic ideas based on learnings."""

        learnings = profile.get("learnings", {})
        topics = learnings.get("topics", {})

        if not topics:
            return [
                "Anxiety coping strategies",
                "ADHD in adults",
                "Understanding autism in adults",
                "Couples communication tips",
                "Self-care practices"
            ]

        # Get top performing topics
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)

        suggestions = []
        for topic, count in sorted_topics[:3]:
            # Suggest variations
            suggestions.append(f"{topic} (proven topic)")
            suggestions.append(f"Advanced {topic}")
            suggestions.append(f"Common myths about {topic}")

        return suggestions[:5]

    def get_optimal_settings(self, profile: dict) -> dict:
        """Get optimal platform, timing, and style based on learnings."""

        learnings = profile.get("learnings", {})

        # Best platform
        platforms = learnings.get("platforms", {})
        best_platform = "Instagram"  # Default
        if platforms:
            best_platform = max(platforms.items(), key=lambda x: x[1])[0]

        # Best timing
        timing = learnings.get("timing", {})
        timing_map = {
            "mid_week": ("Tuesday", "11:00"),
            "early_week": ("Monday", "09:00"),
            "weekend": ("Saturday", "10:00")
        }
        best_day, best_time = ("Tuesday", "11:00")  # Default
        if timing:
            best_timing = max(timing.items(), key=lambda x: x[1])[0]
            best_day, best_time = timing_map.get(best_timing, ("Tuesday", "11:00"))

        # Best style
        styles = learnings.get("content_styles", {})
        best_style = "educational"  # Default
        if styles:
            best_style = max(styles.items(), key=lambda x: x[1])[0]

        return {
            "platform": best_platform,
            "day": best_day,
            "time": best_time,
            "style": best_style
        }

    def create_content(self, topic: str, use_api: bool = False, scheduled_date: str = None):
        """Create optimized content."""

        profile = self.load_profile()

        if profile:
            optimal = self.get_optimal_settings(profile)

            print("\n" + "=" * 70)
            print("🎯 CREATING OPTIMIZED CONTENT")
            print("=" * 70)
            print(f"\nUsing your proven success patterns:")
            print(f"  Platform: {optimal['platform']}")
            print(f"  Style: {optimal['style']}")
            if scheduled_date:
                print(f"  Scheduled: {scheduled_date}")
            print()

            # Build command
            cmd = [
                "python", "request_social_post.py",
                "--topic", topic,
                "--platform", optimal["platform"],
                "--type", optimal["style"]
            ]

            if scheduled_date:
                cmd.extend(["--scheduled-date", scheduled_date])
                cmd.extend(["--scheduled-time", optimal["time"]])

            if use_api:
                cmd.append("--use-api")

            # Run content creation
            result = subprocess.run(cmd, cwd=self.project_root)

            if result.returncode == 0:
                print("\n✅ Content created using your optimal settings!")
            else:
                print("\n❌ Content creation failed")

        else:
            # No profile yet - use standard creation
            print("\n⚠️  No performance data yet - using standard settings")
            print("   Complete weekly check-ins to enable optimization!\n")

            cmd = [
                "python", "request_social_post.py",
                "--topic", topic,
                "--platform", "Instagram"
            ]

            if scheduled_date:
                cmd.extend(["--scheduled-date", scheduled_date])
                cmd.extend(["--scheduled-time", "11:00"])

            if use_api:
                cmd.append("--use-api")

            subprocess.run(cmd, cwd=self.project_root)


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="Create content optimized by your performance learnings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Show what works best for you
  python create_optimized_content.py --show-recommendations

  # Get topic suggestions based on your performance
  python create_optimized_content.py --suggest-topics

  # Create optimized content
  python create_optimized_content.py --topic "ADHD time management tips" --use-api

  # Create and schedule optimized content
  python create_optimized_content.py --topic "Anxiety grounding" --use-api --schedule "2025-11-12"
        """
    )

    parser.add_argument(
        "--show-recommendations",
        action="store_true",
        help="Show content recommendations based on your performance"
    )

    parser.add_argument(
        "--suggest-topics",
        action="store_true",
        help="Get topic suggestions based on what works"
    )

    parser.add_argument(
        "--topic",
        type=str,
        help="Topic for the content"
    )

    parser.add_argument(
        "--use-api",
        action="store_true",
        help="Generate content with Claude API"
    )

    parser.add_argument(
        "--schedule",
        type=str,
        help="Schedule for date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    creator = OptimizedContentCreator()
    profile = creator.load_profile()

    if args.show_recommendations:
        if profile:
            creator.show_recommendations(profile)
        else:
            print("\n⚠️  No performance profile yet.")
            print("   Run: python weekly_checkin.py")
            print("   to start building your performance insights!\n")

    elif args.suggest_topics:
        if profile:
            print("\n" + "=" * 70)
            print("💡 SUGGESTED TOPICS (Based on Your Performance)")
            print("=" * 70 + "\n")

            suggestions = creator.suggest_topics(profile)
            for i, topic in enumerate(suggestions, 1):
                print(f"{i}. {topic}")

            print("\n" + "=" * 70)
        else:
            print("\n⚠️  No performance data yet.")
            print("   Complete weekly check-ins to get personalized suggestions!\n")

    elif args.topic:
        creator.create_content(
            topic=args.topic,
            use_api=args.use_api,
            scheduled_date=args.schedule
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
