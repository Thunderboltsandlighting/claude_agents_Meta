#!/usr/bin/env python3
"""
Weekly Performance Check-In

Simple 5-minute weekly check-in to learn what content works best.
No detailed metrics required - just quick observations.

Usage:
    python weekly_checkin.py
    python weekly_checkin.py --week 2025-11-04
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
import sys


class WeeklyCheckIn:
    """Manage weekly performance check-ins."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.library_path = self.project_root / "social-media-content"
        self.profile_path = self.project_root / "performance_profile.json"
        self.checkins_path = self.project_root / "weekly_checkins"
        self.checkins_path.mkdir(exist_ok=True)

    def get_week_posts(self, week_start: str) -> list:
        """Get posts created/scheduled for a specific week."""

        start_date = datetime.fromisoformat(week_start)
        end_date = start_date + timedelta(days=7)

        posts = []

        # Find all content files from that week
        for meta_file in self.library_path.rglob("*_meta.json"):
            try:
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)

                created = metadata.get("created_date", "")
                if created:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))

                    if start_date <= created_dt < end_date:
                        posts.append({
                            "file": meta_file.name.replace("_meta.json", ""),
                            "title": metadata.get("title", "Untitled"),
                            "platform": metadata.get("content_details", {}).get("platform", "Unknown"),
                            "content_type": metadata.get("content_type", "Unknown"),
                            "created": created_dt,
                            "metadata": metadata
                        })
            except Exception as e:
                continue

        # Sort by created date
        posts.sort(key=lambda x: x["created"])

        return posts

    def run_checkin(self, week_start: str = None):
        """Run interactive weekly check-in."""

        if week_start is None:
            # Default to last Monday
            today = datetime.now()
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_start = last_monday.strftime("%Y-%m-%d")

        print("\n" + "=" * 70)
        print("📊 WEEKLY PERFORMANCE CHECK-IN")
        print("=" * 70)
        print(f"\nWeek of: {week_start}")
        print("\nThis will take about 5 minutes.")
        print("Answer based on general observations - no need for exact numbers!\n")

        # Get posts from this week
        posts = self.get_week_posts(week_start)

        if not posts:
            print(f"\n⚠️  No posts found for week of {week_start}")
            print("Create some content first, then come back for the check-in!\n")
            return

        print(f"You created {len(posts)} post(s) this week:\n")
        for i, post in enumerate(posts, 1):
            day = post["created"].strftime("%A")
            print(f"{i}. {day} - {post['title'][:60]}")
            print(f"   Platform: {post['platform']}")

        print("\n" + "=" * 70)
        print("QUESTIONS")
        print("=" * 70 + "\n")

        responses = {
            "week_start": week_start,
            "checkin_date": datetime.now().isoformat(),
            "posts_count": len(posts),
            "posts": [{"title": p["title"], "platform": p["platform"]} for p in posts]
        }

        # Q1: Best performing post
        print("Q1: Which post got the MOST engagement?")
        print("    (likes, comments, shares, saves)")
        best_idx = self._get_choice_input(f"    Enter number (1-{len(posts)})", 1, len(posts))
        responses["best_performing_post"] = posts[best_idx - 1]["title"]
        responses["best_platform"] = posts[best_idx - 1]["platform"]

        # Q2: How much better?
        print("\nQ2: How much MORE engagement than others?")
        print("    1. A little more (20-30%)")
        print("    2. Noticeably more (50-100%)")
        print("    3. Way more (2x or more)")
        performance_level = self._get_choice_input("    Enter choice", 1, 3)
        performance_map = {1: "slightly_better", 2: "noticeably_better", 3: "significantly_better"}
        responses["performance_level"] = performance_map[performance_level]

        # Q3: Worst performing post
        if len(posts) > 1:
            print("\nQ3: Which post got the LEAST engagement?")
            worst_idx = self._get_choice_input(f"    Enter number (1-{len(posts)})", 1, len(posts))
            responses["worst_performing_post"] = posts[worst_idx - 1]["title"]
            responses["worst_platform"] = posts[worst_idx - 1]["platform"]
        else:
            responses["worst_performing_post"] = None

        # Q4: Inquiries/DMs
        print("\nQ4: Did any posts lead to DMs, inquiries, or consultations?")
        print("    1. Yes - several (3+)")
        print("    2. Yes - a couple (1-2)")
        print("    3. No")
        inquiry_choice = self._get_choice_input("    Enter choice", 1, 3)
        inquiry_map = {1: "high", 2: "moderate", 3: "none"}
        responses["inquiries_generated"] = inquiry_map[inquiry_choice]

        if inquiry_choice < 3:
            print("\n    Which post(s) generated inquiries?")
            inquiry_posts = input("    Enter numbers separated by commas (e.g., 1,3): ").strip()
            responses["inquiry_posts"] = [posts[int(i.strip())-1]["title"] for i in inquiry_posts.split(",") if i.strip().isdigit()]

        # Q5: Topic relevance
        print("\nQ5: Which topic felt MOST relevant to your audience?")
        print("    (What did people seem to connect with?)")
        relevant_topic = input("    Your answer: ").strip()
        responses["most_relevant_topic"] = relevant_topic

        # Q6: Platform performance
        platforms = list(set([p["platform"] for p in posts]))
        if len(platforms) > 1:
            print(f"\nQ6: Which platform performed best?")
            for i, platform in enumerate(platforms, 1):
                print(f"    {i}. {platform}")
            platform_choice = self._get_choice_input("    Enter choice", 1, len(platforms))
            responses["best_platform_overall"] = platforms[platform_choice - 1]
        else:
            responses["best_platform_overall"] = platforms[0]

        # Q7: Content type performance
        print("\nQ7: What content style worked best?")
        print("    1. Educational/How-to (actionable tips)")
        print("    2. Personal/Relatable (stories, experiences)")
        print("    3. Inspirational/Motivational (quotes, encouragement)")
        print("    4. Informational (facts, research, awareness)")
        style_choice = self._get_choice_input("    Enter choice", 1, 4)
        style_map = {1: "educational", 2: "personal", 3: "inspirational", 4: "informational"}
        responses["best_content_style"] = style_map[style_choice]

        # Q8: Timing observations
        print("\nQ8: Did you notice any patterns with posting times?")
        print("    1. Mid-week (Tue-Thu) performed better")
        print("    2. Early week (Mon-Tue) performed better")
        print("    3. Weekend performed better")
        print("    4. No noticeable difference")
        timing_choice = self._get_choice_input("    Enter choice", 1, 4)
        timing_map = {1: "mid_week", 2: "early_week", 3: "weekend", 4: "no_pattern"}
        responses["timing_pattern"] = timing_map[timing_choice]

        # Q9: Additional observations
        print("\nQ9: Any other patterns or observations?")
        print("    (Optional - press Enter to skip)")
        observations = input("    Your notes: ").strip()
        if observations:
            responses["additional_observations"] = observations

        # Q10: What to do more/less of
        print("\nQ10: Based on this week, what should you do MORE of?")
        more_of = input("     Your answer: ").strip()
        responses["do_more_of"] = more_of

        print("\n     What should you do LESS of?")
        less_of = input("     Your answer: ").strip()
        responses["do_less_of"] = less_of

        # Save check-in
        self._save_checkin(week_start, responses)

        # Update performance profile
        self._update_profile(responses)

        # Show summary
        self._show_summary(responses)

    def _get_choice_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get validated integer input from user."""
        while True:
            try:
                choice = int(input(prompt + ": ").strip())
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"    Please enter a number between {min_val} and {max_val}")
            except ValueError:
                print(f"    Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\nCheck-in cancelled.")
                sys.exit(0)

    def _save_checkin(self, week_start: str, responses: dict):
        """Save check-in responses."""
        filename = f"checkin_{week_start}.json"
        filepath = self.checkins_path / filename

        with open(filepath, 'w') as f:
            json.dump(responses, f, indent=2)

        print(f"\n✓ Check-in saved: {filepath.relative_to(self.project_root)}")

    def _update_profile(self, responses: dict):
        """Update performance profile with learnings."""

        # Load existing profile or create new
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                profile = json.load(f)
        else:
            profile = {
                "created": datetime.now().isoformat(),
                "total_checkins": 0,
                "learnings": {
                    "topics": {},
                    "platforms": {},
                    "content_styles": {},
                    "timing": {},
                    "inquiry_generating_topics": []
                },
                "recommendations": []
            }

        profile["total_checkins"] += 1
        profile["last_updated"] = datetime.now().isoformat()

        # Update learnings
        learnings = profile["learnings"]

        # Best topics
        topic = responses.get("most_relevant_topic")
        if topic:
            learnings["topics"][topic] = learnings["topics"].get(topic, 0) + 1

        # Platform performance
        platform = responses.get("best_platform_overall")
        if platform:
            learnings["platforms"][platform] = learnings["platforms"].get(platform, 0) + 1

        # Content styles
        style = responses.get("best_content_style")
        if style:
            learnings["content_styles"][style] = learnings["content_styles"].get(style, 0) + 1

        # Timing patterns
        timing = responses.get("timing_pattern")
        if timing and timing != "no_pattern":
            learnings["timing"][timing] = learnings["timing"].get(timing, 0) + 1

        # Inquiry-generating content
        if responses.get("inquiries_generated") != "none":
            inquiry_posts = responses.get("inquiry_posts", [])
            learnings["inquiry_generating_topics"].extend(inquiry_posts)

        # Generate recommendations
        profile["recommendations"] = self._generate_recommendations(learnings, profile["total_checkins"])

        # Save updated profile
        with open(self.profile_path, 'w') as f:
            json.dump(profile, f, indent=2)

        print(f"✓ Performance profile updated: {self.profile_path.relative_to(self.project_root)}")

    def _generate_recommendations(self, learnings: dict, total_checkins: int) -> list:
        """Generate content recommendations based on learnings."""

        recommendations = []

        # Top topics
        topics = learnings.get("topics", {})
        if topics:
            top_topic = max(topics.items(), key=lambda x: x[1])
            recommendations.append({
                "type": "topic",
                "action": f"Create more content about: {top_topic[0]}",
                "confidence": "high" if top_topic[1] >= 3 else "moderate"
            })

        # Best platform
        platforms = learnings.get("platforms", {})
        if platforms:
            top_platform = max(platforms.items(), key=lambda x: x[1])
            recommendations.append({
                "type": "platform",
                "action": f"Focus more on {top_platform[0]}",
                "confidence": "high" if top_platform[1] >= 3 else "moderate"
            })

        # Content style
        styles = learnings.get("content_styles", {})
        if styles:
            top_style = max(styles.items(), key=lambda x: x[1])
            style_names = {
                "educational": "educational/how-to content with actionable tips",
                "personal": "personal stories and relatable experiences",
                "inspirational": "inspirational and motivational content",
                "informational": "informational and research-based content"
            }
            recommendations.append({
                "type": "style",
                "action": f"Emphasize {style_names.get(top_style[0], top_style[0])}",
                "confidence": "high" if top_style[1] >= 2 else "moderate"
            })

        # Timing
        timing = learnings.get("timing", {})
        if timing:
            top_timing = max(timing.items(), key=lambda x: x[1])
            timing_names = {
                "mid_week": "Tuesday-Thursday",
                "early_week": "Monday-Tuesday",
                "weekend": "Saturday-Sunday"
            }
            recommendations.append({
                "type": "timing",
                "action": f"Schedule posts for {timing_names.get(top_timing[0], 'optimal times')}",
                "confidence": "moderate"
            })

        return recommendations

    def _show_summary(self, responses: dict):
        """Display check-in summary and recommendations."""

        print("\n" + "=" * 70)
        print("📊 WEEK SUMMARY")
        print("=" * 70)

        print(f"\n✅ Posts created: {responses['posts_count']}")
        print(f"🏆 Best performer: {responses['best_performing_post']}")
        print(f"📱 Best platform: {responses['best_platform_overall']}")
        print(f"📝 Best style: {responses['best_content_style']}")

        if responses.get("inquiries_generated") != "none":
            print(f"💼 Generated inquiries: Yes!")

        print("\n" + "=" * 70)
        print("💡 RECOMMENDATIONS FOR NEXT WEEK")
        print("=" * 70)

        print(f"\n✅ DO MORE:")
        print(f"   • {responses.get('do_more_of', 'N/A')}")

        print(f"\n❌ DO LESS:")
        print(f"   • {responses.get('do_less_of', 'N/A')}")

        # Load and show profile recommendations
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                profile = json.load(f)

            if profile.get("recommendations"):
                print(f"\n🎯 BASED ON YOUR OVERALL PATTERNS:")
                for rec in profile["recommendations"][:3]:  # Top 3
                    confidence = "🔥" if rec["confidence"] == "high" else "💡"
                    print(f"   {confidence} {rec['action']}")

        print("\n" + "=" * 70)
        print("✓ Check-in complete! See you next week!")
        print("=" * 70 + "\n")


def main():
    """Main CLI interface."""

    parser = argparse.ArgumentParser(
        description="Weekly performance check-in (takes ~5 minutes)"
    )

    parser.add_argument(
        "--week",
        type=str,
        help="Week start date (YYYY-MM-DD). Defaults to last Monday."
    )

    args = parser.parse_args()

    checkin = WeeklyCheckIn()
    checkin.run_checkin(week_start=args.week)


if __name__ == "__main__":
    main()
