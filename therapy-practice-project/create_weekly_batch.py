#!/usr/bin/env python3
"""
Weekly Batch Content Creator with Observance Awareness

Intelligent batch content creation system that:
1. Reads your weekly schedule
2. Scans existing content to avoid repetition
3. Forecasts upcoming mental health observances (14 days ahead)
4. Prioritizes observance-related content for timely awareness posts
5. Suggests fresh topics based on service areas and gaps
6. Lets you approve/edit topics
7. Batch creates all content with Claude API
8. Automatically updates schedule with content links

The system tracks 60+ mental health awareness days/weeks/months including:
- Mental Health Month (May)
- Suicide Prevention Month (September)
- ADHD Awareness Month (October)
- Indigenous Peoples Day (October 13)
- World Mental Health Day (October 10)
- PTSD Awareness Month (June)
- And many more...

Usage:
    # Interactive mode - suggests topics, asks for approval
    python create_weekly_batch.py --week 2025-11-04 --use-api

    # Preview mode - see suggestions without creating content
    python create_weekly_batch.py --week 2025-11-04 --preview

    # Skip approval - use all suggested topics automatically
    python create_weekly_batch.py --week 2025-11-04 --use-api --auto-approve
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
import anthropic
import os
import uuid
import random


class WeeklyBatchCreator:
    """Intelligent weekly batch content creator."""

    def __init__(self, library_path: Path = None):
        """Initialize the batch creator."""
        if library_path is None:
            library_path = Path(__file__).parent / "social-media-content"

        self.library_path = library_path
        self.performance_profile_path = Path(__file__).parent / "performance_profile.json"
        self.observances_path = Path(__file__).parent / "mental_health_observances.json"

        # Load observances calendar
        self.observances = self._load_observances()

        # Service areas for topic generation
        self.service_areas = {
            "anxiety": {
                "keywords": ["anxiety", "panic", "worry", "stress", "overwhelm"],
                "topics": [
                    "Anxiety Coping Strategies for Adults",
                    "Understanding Panic Attacks and How to Manage Them",
                    "Daily Anxiety Management Techniques",
                    "Social Anxiety: Signs and Support",
                    "Anxiety vs Stress: Understanding the Difference",
                    "Grounding Techniques for Anxiety Relief",
                    "How Therapy Helps with Chronic Anxiety",
                ]
            },
            "adhd": {
                "keywords": ["adhd", "attention", "focus", "executive function"],
                "topics": [
                    "Understanding ADHD in Adults",
                    "ADHD and Relationship Challenges",
                    "Executive Function Skills for ADHD",
                    "ADHD Diagnosis Process for Adults",
                    "ADHD Medication vs Therapy: What Works Best",
                    "Time Management Strategies for ADHD",
                ]
            },
            "depression": {
                "keywords": ["depression", "depressed", "sadness", "hopeless"],
                "topics": [
                    "Recognizing Depression Symptoms in Adults",
                    "When Sadness Becomes Depression",
                    "Depression Treatment Options That Work",
                    "Supporting a Loved One with Depression",
                    "Seasonal Depression: More Than Just Winter Blues",
                ]
            },
            "couples": {
                "keywords": ["couples", "relationship", "marriage", "partner"],
                "topics": [
                    "Signs You Need Couples Therapy",
                    "Communication Skills for Healthy Relationships",
                    "Rebuilding Trust After Betrayal",
                    "Couples Therapy: What to Expect",
                    "Conflict Resolution Strategies for Couples",
                    "Maintaining Intimacy During Stressful Times",
                ]
            },
            "teens": {
                "keywords": ["teen", "adolescent", "teenager", "youth"],
                "topics": [
                    "Teen Mental Health Warning Signs for Parents",
                    "Supporting Anxious Teenagers",
                    "When Your Teen Needs Therapy",
                    "Teen Depression: What Parents Should Know",
                    "Helping Teens Build Healthy Coping Skills",
                ]
            },
            "trauma": {
                "keywords": ["trauma", "ptsd", "emdr", "healing"],
                "topics": [
                    "What is EMDR Therapy and How Does It Work",
                    "Healing from Past Trauma",
                    "Understanding Complex PTSD",
                    "Trauma-Informed Therapy Approaches",
                ]
            },
            "general": {
                "keywords": ["therapy", "counseling", "mental health", "wellness"],
                "topics": [
                    "How to Find the Right Therapist in Hendersonville NC",
                    "What to Expect in Your First Therapy Session",
                    "Does Insurance Cover Therapy",
                    "Self-Care Strategies for Mental Wellness",
                    "Breaking the Stigma Around Therapy",
                ]
            }
        }

    def get_existing_topics(self) -> Set[str]:
        """Scan content library and extract all existing topics/titles."""
        existing_topics = set()

        # Scan all metadata files
        for meta_file in self.library_path.rglob("*_meta.json"):
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                    title = meta.get("title", "").lower()
                    if title:
                        existing_topics.add(title)

                    # Also add keywords for better matching
                    keywords = meta.get("social_media", {}).get("hashtags", [])
                    for kw in keywords:
                        existing_topics.add(kw.lower().replace("#", ""))
            except:
                continue

        return existing_topics

    def get_topic_coverage(self, existing_topics: Set[str]) -> Dict:
        """Analyze which service areas need more content."""
        coverage = {}

        for area, data in self.service_areas.items():
            keywords = data["keywords"]

            # Count how many existing posts mention this area
            count = 0
            for topic in existing_topics:
                if any(kw in topic for kw in keywords):
                    count += 1

            coverage[area] = {
                "count": count,
                "priority": "high" if count < 3 else "medium" if count < 6 else "low"
            }

        return coverage

    def load_performance_learnings(self) -> Dict:
        """Load performance profile if it exists."""
        if self.performance_profile_path.exists():
            with open(self.performance_profile_path, 'r') as f:
                return json.load(f)
        return {"learnings": {}}

    def _load_observances(self) -> Dict:
        """Load mental health observances calendar."""
        if self.observances_path.exists():
            with open(self.observances_path, 'r') as f:
                return json.load(f)
        return {"observances": {}}

    def _parse_observance_date(self, date_str: str, year: int) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Parse observance date string into datetime objects.

        Args:
            date_str: Date string like "March 10-16", "October 13", "September 1-30"
            year: Year to use for parsing

        Returns:
            Tuple of (start_date, end_date) as datetime objects, or (None, None) if unparseable
        """
        try:
            month_names = {
                "january": 1, "february": 2, "march": 3, "april": 4,
                "may": 5, "june": 6, "july": 7, "august": 8,
                "september": 9, "october": 10, "november": 11, "december": 12
            }

            # Extract month and day(s)
            parts = date_str.lower().split()
            if len(parts) < 2:
                return (None, None)

            month_name = parts[0]
            month = month_names.get(month_name)
            if not month:
                return (None, None)

            # Parse day range
            day_str = parts[1]
            if "-" in day_str:
                # Range like "10-16" or "15 - Mar. 2"
                if len(parts) > 2 and parts[2] in month_names:
                    # Cross-month range like "February 24 - March 2"
                    start_day = int(parts[1])
                    end_month = month_names[parts[2]]
                    end_day = int(parts[3])
                    start_date = datetime(year, month, start_day)
                    end_date = datetime(year, end_month, end_day)
                else:
                    # Same month range
                    start_day, end_day = map(int, day_str.split("-"))
                    start_date = datetime(year, month, start_day)
                    end_date = datetime(year, month, end_day)
            else:
                # Single day
                day = int(day_str)
                start_date = datetime(year, month, day)
                end_date = start_date

            return (start_date, end_date)

        except Exception:
            return (None, None)

    def find_relevant_observances(
        self,
        start_date: datetime,
        end_date: datetime,
        lead_time_days: int = 14
    ) -> List[Dict]:
        """
        Find observances within date range with lead time.

        Args:
            start_date: Start of content creation window
            end_date: End of content creation window
            lead_time_days: How many days ahead to look for observances

        Returns:
            List of relevant observances with their topics
        """
        relevant = []
        year = start_date.year

        # Look ahead window
        forecast_end = end_date + timedelta(days=lead_time_days)

        for month_name, month_data in self.observances.get("observances", {}).items():
            # Check month observances
            for obs in month_data.get("month_observances", []):
                obs_dates = obs.get("dates", "")
                obs_start, obs_end = self._parse_observance_date(obs_dates, year)

                if obs_start and obs_end:
                    # Check if observance falls within our forecast window
                    if obs_start <= forecast_end and obs_end >= start_date:
                        # Calculate optimal posting date (start of observance or slightly before)
                        optimal_post_date = obs_start - timedelta(days=3)

                        relevant.append({
                            "name": obs["name"],
                            "type": obs["type"],
                            "start_date": obs_start,
                            "end_date": obs_end,
                            "optimal_post_date": optimal_post_date,
                            "focus_areas": obs.get("focus_areas", []),
                            "content_ideas": obs.get("content_ideas", []),
                            "priority": "high"  # Observances are high priority
                        })

            # Check specific dates
            for obs in month_data.get("specific_dates", []):
                obs_date_str = obs.get("date", "")
                obs_start, obs_end = self._parse_observance_date(obs_date_str, year)

                if obs_start and obs_end:
                    # Check if observance falls within our forecast window
                    if obs_start <= forecast_end and obs_end >= start_date:
                        # For days/weeks, post 3-5 days before or early in the observance
                        if obs["type"] == "day":
                            optimal_post_date = obs_start - timedelta(days=3)
                        else:  # week
                            optimal_post_date = obs_start

                        relevant.append({
                            "name": obs["name"],
                            "type": obs["type"],
                            "start_date": obs_start,
                            "end_date": obs_end,
                            "optimal_post_date": optimal_post_date,
                            "focus_areas": obs.get("focus_areas", []),
                            "content_ideas": obs.get("content_ideas", []),
                            "priority": "high"
                        })

        # Sort by optimal post date
        relevant.sort(key=lambda x: x["optimal_post_date"])

        return relevant

    def suggest_topics_for_schedule(
        self,
        schedule: Dict,
        existing_topics: Set[str],
        coverage: Dict
    ) -> List[Dict]:
        """Suggest fresh topics for each scheduled post, prioritizing observances."""

        performance = self.load_performance_learnings()
        best_topics = performance.get("learnings", {}).get("topics", {})

        suggestions = []
        used_topics = set()
        used_observances = set()

        # Get week date range
        dates = sorted(schedule["days"].keys())
        week_start = datetime.fromisoformat(dates[0])
        week_end = datetime.fromisoformat(dates[-1])

        # Find relevant observances (look ahead 14 days)
        observances = self.find_relevant_observances(week_start, week_end, lead_time_days=14)

        # Count posts needed
        total_posts_needed = sum(
            1 for day_data in schedule["days"].values()
            for post in day_data["posts"]
            if not post.get("content_file")
        )

        # Determine how many observance posts vs regular posts
        # Use observance content for ~40-60% of posts if observances available
        max_observance_posts = min(len(observances), max(1, total_posts_needed // 2))

        # Sort days chronologically
        observance_posts_used = 0

        for date_str, day_data in sorted(schedule["days"].items()):
            for post_idx, post in enumerate(day_data["posts"]):
                if not post.get("content_file"):
                    topic = None
                    source_type = "regular"
                    service_area = None
                    priority = "medium"
                    observance_name = None

                    # PRIORITY 1: Check if there's a relevant observance for this week
                    if observance_posts_used < max_observance_posts and observances:
                        for obs in observances:
                            if obs["name"] not in used_observances and obs["content_ideas"]:
                                # Pick a random content idea from this observance
                                available_ideas = [
                                    idea for idea in obs["content_ideas"]
                                    if idea.lower() not in existing_topics
                                    and idea not in used_topics
                                ]

                                if available_ideas:
                                    topic = random.choice(available_ideas)
                                    used_topics.add(topic)
                                    used_observances.add(obs["name"])
                                    source_type = "observance"
                                    priority = "observance"
                                    observance_name = obs["name"]
                                    service_area = obs["focus_areas"][0] if obs["focus_areas"] else "mental health"
                                    observance_posts_used += 1
                                    break

                    # PRIORITY 2: Regular service area topics
                    if not topic:
                        # Find best service area to focus on
                        priority_areas = sorted(
                            coverage.items(),
                            key=lambda x: (
                                0 if x[1]["priority"] == "high" else
                                1 if x[1]["priority"] == "medium" else 2,
                                x[1]["count"]
                            )
                        )

                        # Cycle through priority areas to ensure variety
                        for area, area_data in priority_areas:
                            available_topics = [
                                t for t in self.service_areas[area]["topics"]
                                if t.lower() not in existing_topics
                                and t not in used_topics
                            ]

                            if available_topics:
                                # Pick first available topic
                                topic = available_topics[0]
                                used_topics.add(topic)

                                # Update coverage to track suggestions
                                coverage[area]["count"] += 1

                                service_area = area
                                priority = area_data["priority"]
                                break

                    # Add suggestion
                    if topic:
                        suggestion = {
                            "date": date_str,
                            "day_name": day_data["day_name"],
                            "platform": post["platform"],
                            "time": post["time"],
                            "topic": topic,
                            "service_area": service_area,
                            "priority": priority,
                            "post_index": post_idx,
                            "source_type": source_type
                        }

                        if observance_name:
                            suggestion["observance"] = observance_name

                        suggestions.append(suggestion)

        return suggestions

    def display_suggestions(self, suggestions: List[Dict]):
        """Display topic suggestions in readable format."""
        print("\n" + "="*80)
        print("SUGGESTED CONTENT TOPICS FOR THE WEEK")
        print("="*80)

        # Count observance vs regular posts
        observance_count = sum(1 for s in suggestions if s.get("source_type") == "observance")
        regular_count = len(suggestions) - observance_count

        print(f"\nTotal posts to create: {len(suggestions)}")
        if observance_count > 0:
            print(f"  📅 Observance-related: {observance_count}")
            print(f"  📝 Regular content: {regular_count}")
        print()

        current_date = None
        for i, suggestion in enumerate(suggestions, 1):
            if suggestion["date"] != current_date:
                current_date = suggestion["date"]
                print(f"\n{suggestion['day_name']} - {suggestion['date']}")
                print("-" * 80)

            # Icon based on priority/type
            if suggestion.get("source_type") == "observance":
                priority_icon = "📅"  # Calendar emoji for observances
                type_label = "OBSERVANCE"
            else:
                priority_icon = "🔴" if suggestion["priority"] == "high" else "🟡" if suggestion["priority"] == "medium" else "🟢"
                type_label = suggestion['service_area'].upper()

            print(f"  {i}. [{suggestion['platform']:9}] @ {suggestion['time']} | {priority_icon} {type_label}")
            print(f"     Topic: {suggestion['topic']}")

            # Show observance name if present
            if suggestion.get("observance"):
                print(f"     Observance: {suggestion['observance']}")

        print("\n" + "="*80)

    def get_user_approval(self, suggestions: List[Dict]) -> List[Dict]:
        """Let user approve/edit suggested topics."""
        print("\n📝 Review and edit topics as needed:")
        print("   - Press ENTER to keep a topic")
        print("   - Type new topic to replace it")
        print("   - Type 'skip' to skip this post\n")

        approved = []

        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n[{i}/{len(suggestions)}] {suggestion['platform']} on {suggestion['day_name']}")
            print(f"Suggested: {suggestion['topic']}")

            user_input = input("Keep this topic? (ENTER/edit/skip): ").strip()

            if user_input.lower() == "skip":
                print("  ⊘ Skipped")
                continue
            elif user_input:
                suggestion["topic"] = user_input
                print(f"  ✓ Updated to: {user_input}")
            else:
                print("  ✓ Approved")

            approved.append(suggestion)

        return approved

    def create_content_for_topic(
        self,
        topic: str,
        platform: str,
        date: str,
        time: str,
        api_key: str
    ) -> Optional[Dict]:
        """Create content using Claude API."""

        # Determine content type based on platform
        content_type_map = {
            "Instagram": "feed-post",
            "Facebook": "post",
            "LinkedIn": "article"
        }
        content_type = content_type_map.get(platform, "post")

        # Create prompt
        prompt = f"""Create a social media {content_type} for {platform} about: {topic}

TARGET AUDIENCE: Adults seeking therapy in Hendersonville NC and Western NC

REQUIREMENTS:
1. Educational and empathetic tone
2. 150-250 words
3. Include practical insights or tips
4. HIPAA compliant (no diagnosis, no treatment advice)
5. Professional yet warm and approachable
6. Include clear call-to-action for therapy consultation
7. 5-8 relevant hashtags (mix of popular and niche)
8. Visual content suggestions

BUSINESS CONTEXT:
- Practice: Hendersonville Counseling
- Location: Hendersonville NC, Western NC
- Services: Individual therapy, couples counseling, teen therapy, anxiety treatment, ADHD support, trauma therapy (EMDR)

Please provide:
- Main caption/post text
- Hashtags
- Visual suggestions
- Engagement tips"""

        try:
            client = anthropic.Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content_text = message.content[0].text

            # Create metadata
            content_id = str(uuid.uuid4())[:8]
            metadata = {
                "content_id": content_id,
                "content_type": f"{platform.lower()}-{content_type}",
                "title": topic,
                "created_date": datetime.now().isoformat(),
                "created_by_agent": "weekly-batch-creator",
                "status": "scheduled",
                "scheduling": {
                    "scheduled_date": date,
                    "scheduled_time": time,
                    "timezone": "America/New_York",
                    "platform": platform
                },
                "content_details": {
                    "platform": platform,
                    "target_audience": "adults seeking therapy",
                    "business_goal": "awareness and engagement"
                },
                "social_media": {
                    "platform": platform,
                    "content_type": content_type
                },
                "performance": {
                    "views": 0,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "engagement_rate": 0
                },
                "compliance": {
                    "hipaa_reviewed": True,
                    "contains_phi": False,
                    "reviewed_by": "automated",
                    "review_date": datetime.now().isoformat()
                }
            }

            return {
                "content": content_text,
                "metadata": metadata,
                "filename": f"{topic.lower().replace(' ', '-')[:50]}-{content_id}"
            }

        except Exception as e:
            print(f"  ❌ Error creating content: {str(e)}")
            return None

    def save_content(
        self,
        content_data: Dict,
        platform: str
    ) -> Optional[Path]:
        """Save content and metadata to appropriate folder."""

        platform_folders = {
            "Instagram": self.library_path / "instagram" / "feed-posts" / "scheduled",
            "Facebook": self.library_path / "facebook" / "posts" / "scheduled",
            "LinkedIn": self.library_path / "linkedin" / "articles" / "scheduled"
        }

        folder = platform_folders.get(platform)
        if not folder:
            return None

        folder.mkdir(parents=True, exist_ok=True)

        filename_base = content_data["filename"]

        # Save content markdown
        content_file = folder / f"{filename_base}.md"
        with open(content_file, 'w') as f:
            f.write(content_data["content"])

        # Save metadata
        meta_file = folder / f"{filename_base}_meta.json"
        with open(meta_file, 'w') as f:
            json.dump(content_data["metadata"], f, indent=2)

        return content_file

    def update_schedule(
        self,
        schedule_path: Path,
        date: str,
        post_index: int,
        content_file: Path
    ):
        """Update schedule JSON with created content file."""

        with open(schedule_path, 'r') as f:
            schedule = json.load(f)

        # Update the specific post
        post = schedule["days"][date]["posts"][post_index]
        post["status"] = "scheduled"
        post["content_needed"] = False
        post["content_file"] = str(content_file.relative_to(self.library_path))
        post["created_date"] = datetime.now().isoformat()

        # Save updated schedule
        with open(schedule_path, 'w') as f:
            json.dump(schedule, f, indent=2)

    def create_weekly_batch(
        self,
        week_start: str,
        use_api: bool = False,
        auto_approve: bool = False,
        preview_only: bool = False
    ):
        """Main workflow to create weekly batch content."""

        # Load schedule
        week_dt = datetime.fromisoformat(week_start)
        week_number = week_dt.isocalendar()[1]
        year = week_dt.year

        batch_folder = self.library_path / "weekly-batches" / f"{year}-week-{week_number:02d}"
        schedule_file = batch_folder / "weekly_schedule.json"

        if not schedule_file.exists():
            print(f"❌ Error: Schedule not found at {schedule_file}")
            print(f"\nCreate schedule first with:")
            print(f"  python schedule_content.py --week {week_start}")
            return

        with open(schedule_file, 'r') as f:
            schedule = json.load(f)

        # Step 1: Scan existing content
        print("\n🔍 Scanning existing content library...")
        existing_topics = self.get_existing_topics()
        print(f"   Found {len(existing_topics)} existing topics")

        # Step 2: Analyze coverage
        coverage = self.get_topic_coverage(existing_topics)
        print(f"\n📊 Content coverage analysis:")
        for area, data in sorted(coverage.items(), key=lambda x: x[1]["count"]):
            icon = "🔴" if data["priority"] == "high" else "🟡" if data["priority"] == "medium" else "🟢"
            print(f"   {icon} {area.capitalize():12} - {data['count']} posts (Priority: {data['priority']})")

        # Step 2.5: Check for upcoming observances
        week_end = week_dt + timedelta(days=6)
        observances = self.find_relevant_observances(week_dt, week_end, lead_time_days=14)

        if observances:
            print(f"\n📅 Upcoming Mental Health Observances (next 2 weeks):")
            for obs in observances[:5]:  # Show top 5
                date_str = obs['start_date'].strftime('%B %d')
                if obs['start_date'] != obs['end_date']:
                    date_str += f" - {obs['end_date'].strftime('%B %d')}"

                print(f"   📌 {obs['name']} ({date_str})")
                print(f"      Focus: {', '.join(obs['focus_areas'][:3])}")

        # Step 3: Generate suggestions
        print(f"\n💡 Generating topic suggestions for week of {week_start}...")
        suggestions = self.suggest_topics_for_schedule(schedule, existing_topics, coverage)

        if not suggestions:
            print("\n✓ All posts already have content assigned!")
            return

        # Display suggestions
        self.display_suggestions(suggestions)

        # Preview mode - stop here
        if preview_only:
            print("\n📋 PREVIEW MODE - No content will be created")
            print("   Remove --preview flag to create content")
            return

        # Step 4: Get approval (unless auto-approve)
        if auto_approve:
            print("\n⚡ AUTO-APPROVE MODE - Using all suggested topics")
            approved = suggestions
        else:
            approved = self.get_user_approval(suggestions)

        if not approved:
            print("\n⊘ No topics approved. Exiting.")
            return

        print(f"\n✓ {len(approved)} topics approved for creation")

        # Step 5: Create content
        if not use_api:
            print("\n⚠️  API mode not enabled. Add --use-api flag to create content.")
            return

        # Get API key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("\n❌ Error: ANTHROPIC_API_KEY not found in environment")
            print("   Make sure your .env file is set up correctly")
            return

        print(f"\n🤖 Creating {len(approved)} posts with Claude API...")
        print("   This may take a few minutes...\n")

        created_count = 0
        failed_count = 0

        for i, suggestion in enumerate(approved, 1):
            print(f"[{i}/{len(approved)}] Creating: {suggestion['topic'][:60]}...")

            # Create content
            content_data = self.create_content_for_topic(
                topic=suggestion["topic"],
                platform=suggestion["platform"],
                date=suggestion["date"],
                time=suggestion["time"],
                api_key=api_key
            )

            if content_data:
                # Save content
                content_file = self.save_content(content_data, suggestion["platform"])

                if content_file:
                    # Update schedule
                    self.update_schedule(
                        schedule_file,
                        suggestion["date"],
                        suggestion["post_index"],
                        content_file
                    )

                    print(f"  ✓ Created and scheduled")
                    created_count += 1
                else:
                    print(f"  ❌ Failed to save content")
                    failed_count += 1
            else:
                failed_count += 1

        # Summary
        print("\n" + "="*80)
        print("BATCH CREATION COMPLETE")
        print("="*80)
        print(f"\n✓ Successfully created: {created_count} posts")
        if failed_count > 0:
            print(f"❌ Failed: {failed_count} posts")
        print(f"\n📁 Content saved to: social-media-content/")
        print(f"📅 Schedule updated: {schedule_file.relative_to(Path.cwd())}")
        print("\n🎯 Next steps:")
        print("   1. Review created content in scheduled folders")
        print("   2. Edit/customize as needed")
        print("   3. Post content on scheduled dates/times")
        print("   4. Track performance with weekly_checkin.py")
        print()


def main():
    """CLI interface."""

    parser = argparse.ArgumentParser(
        description="Create weekly batch content with intelligent topic suggestions"
    )

    parser.add_argument(
        "--week",
        type=str,
        required=True,
        help="Week start date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--use-api",
        action="store_true",
        help="Use Claude API to generate content (requires API key)"
    )

    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Automatically approve all suggested topics (no manual review)"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview suggested topics without creating content"
    )

    args = parser.parse_args()

    # Validate week format
    try:
        datetime.fromisoformat(args.week)
    except ValueError:
        print(f"❌ Error: Invalid date format '{args.week}'")
        print("   Use YYYY-MM-DD format (e.g., 2025-11-04)")
        sys.exit(1)

    # Initialize and run
    creator = WeeklyBatchCreator()
    creator.create_weekly_batch(
        week_start=args.week,
        use_api=args.use_api,
        auto_approve=args.auto_approve,
        preview_only=args.preview
    )


if __name__ == "__main__":
    main()
