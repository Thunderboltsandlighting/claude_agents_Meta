#!/usr/bin/env python3
"""
Interactive Weekly Batch Content Creator with Blog Integration

Creates weekly content with full user control:
- 8 social media posts (Mon-Thu)
- 1 PRD v2.2 compliant blog post (Friday)
- Interactive theme selection
- Style customization
- Observance awareness

Usage:
    # Interactive mode with blog
    python create_weekly_batch_v2.py --week 2025-11-11 --use-api --interactive --with-blog

    # Quick auto mode (original)
    python create_weekly_batch_v2.py --week 2025-11-11 --use-api --auto-approve
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


class InteractiveWeeklyBatchCreator:
    """Interactive weekly batch content creator with blog integration."""

    def __init__(self, library_path: Path = None):
        """Initialize the batch creator."""
        if library_path is None:
            library_path = Path(__file__).parent / "social-media-content"

        self.library_path = library_path
        self.blog_path = Path(__file__).parent / "blog-posts"
        self.performance_profile_path = Path(__file__).parent / "performance_profile.json"
        self.observances_path = Path(__file__).parent / "mental_health_observances.json"

        # Load observances calendar
        self.observances = self._load_observances()

        # Service areas for topic generation
        self.service_areas = {
            "anxiety": ["anxiety", "panic", "worry", "stress", "overwhelm"],
            "adhd": ["adhd", "attention", "focus", "executive function"],
            "depression": ["depression", "depressed", "sadness", "hopeless"],
            "couples": ["couples", "relationship", "marriage", "partner"],
            "teens": ["teen", "adolescent", "teenager", "youth"],
            "trauma": ["trauma", "ptsd", "emdr", "healing"],
            "general": ["therapy", "counseling", "mental health", "wellness"]
        }

        # Theme templates
        self.theme_templates = {
            "anxiety": [
                "Anxiety and Sleep Problems",
                "Managing Social Anxiety",
                "Panic Attack Coping Strategies",
                "Workplace Anxiety Management",
                "Anxiety in Relationships"
            ],
            "depression": [
                "Recognizing and Treating Depression",
                "Depression vs Sadness",
                "Seasonal Depression Support",
                "Depression and Relationships",
                "Finding Hope in Depression"
            ],
            "couples": [
                "Communication Skills for Healthy Relationships",
                "Rebuilding Trust in Relationships",
                "Conflict Resolution for Couples",
                "Intimacy and Connection",
                "When to Seek Couples Therapy"
            ],
            "teens": [
                "Teen Mental Health Warning Signs",
                "Supporting Anxious Teenagers",
                "Teen Depression and School Performance",
                "Helping Teens Build Coping Skills",
                "Parent-Teen Communication"
            ],
            "trauma": [
                "Understanding EMDR Therapy",
                "Healing from Past Trauma",
                "Complex PTSD vs PTSD",
                "Trauma-Informed Therapy Approaches",
                "Recovery from Sexual Trauma"
            ],
            "adhd": [
                "ADHD in Adults",
                "ADHD and Relationship Challenges",
                "Executive Function Skills",
                "ADHD Medication vs Therapy",
                "Time Management with ADHD"
            ]
        }

    def _load_observances(self) -> Dict:
        """Load mental health observances calendar."""
        if self.observances_path.exists():
            with open(self.observances_path, 'r') as f:
                return json.load(f)
        return {"observances": {}}

    def get_existing_topics(self) -> Set[str]:
        """Scan content library and extract all existing topics/titles."""
        existing_topics = set()

        for meta_file in self.library_path.rglob("*_meta.json"):
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                    title = meta.get("title", "").lower()
                    if title:
                        existing_topics.add(title)
            except:
                continue

        return existing_topics

    def interactive_theme_selection(self, observances: List[Dict]) -> Tuple[str, str]:
        """
        Interactive theme selection with 3 modes.

        Returns:
            Tuple of (theme, mode) where mode is 'random', 'observance', or 'custom'
        """
        print("\n" + "="*80)
        print("WEEKLY CONTENT CREATION")
        print("="*80)
        print("\nCreating content:")
        print("  • 8 social media posts (Mon-Thu)")
        print("  • 1 comprehensive blog post (Friday)")
        print("\nChoose your theme approach:")
        print("  1. Random Suggestions (AI picks from service areas)")
        print("  2. Observance-Based (Focus on upcoming mental health observances)")
        print("  3. Custom Theme (You provide the topic)")

        while True:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

        if choice == '3':
            # Custom theme input
            print("\n" + "-"*80)
            print("CUSTOM THEME MODE")
            print("-"*80)
            print("\nEnter your weekly theme:")
            print("(Will be used for 8 social posts + 1 comprehensive blog)")
            print("\nExamples:")
            print("  • Anxiety and sleep problems")
            print("  • Communication skills for couples")
            print("  • Teen mental health in schools")

            while True:
                theme = input("\nEnter theme: ").strip()
                if theme:
                    return (theme, 'custom')
                print("❌ Theme cannot be empty. Please enter a theme.")

        elif choice == '2':
            # Observance-based
            if not observances:
                print("\n⚠️  No observances found in the next 2 weeks.")
                print("   Switching to random suggestions...")
                choice = '1'
            else:
                print("\n" + "-"*80)
                print("OBSERVANCE-BASED THEMES")
                print("-"*80)
                print("\nUpcoming observances:")

                obs_themes = []
                for i, obs in enumerate(observances[:5], 1):
                    date_str = obs['start_date'].strftime('%B %d')
                    if obs['start_date'] != obs['end_date']:
                        date_str += f" - {obs['end_date'].strftime('%B %d')}"

                    # Generate theme from observance
                    focus = obs['focus_areas'][0] if obs['focus_areas'] else 'mental health'
                    theme = f"{obs['name']} - {focus.title()} Support"
                    obs_themes.append(theme)

                    print(f"  {i}. {theme}")
                    print(f"     ({date_str})")

                print(f"  R - Regenerate different themes")
                print(f"  C - Custom theme")

                while True:
                    obs_choice = input("\nEnter choice (1-5, R, C): ").strip().upper()

                    if obs_choice == 'C':
                        theme = input("Enter custom theme: ").strip()
                        if theme:
                            return (theme, 'observance-custom')
                    elif obs_choice == 'R':
                        # Show next set (for now, just rotate)
                        print("(Regenerate not yet implemented - showing same list)")
                        continue
                    elif obs_choice.isdigit() and 1 <= int(obs_choice) <= len(obs_themes):
                        return (obs_themes[int(obs_choice) - 1], 'observance')
                    else:
                        print(f"❌ Invalid choice. Please enter 1-{len(obs_themes)}, R, or C.")

        # Random suggestions (choice == '1' or fallback)
        print("\n" + "-"*80)
        print("RANDOM THEME SUGGESTIONS")
        print("-"*80)

        all_themes = []
        for area_themes in self.theme_templates.values():
            all_themes.extend(area_themes)

        current_offset = 0

        while True:
            # Show 5 themes
            themes_to_show = all_themes[current_offset:current_offset + 5]

            print("\nChoose your weekly theme:")
            for i, theme in enumerate(themes_to_show, 1):
                print(f"  {i}. {theme}")

            remaining = len(all_themes) - (current_offset + 5)
            if remaining > 0:
                print(f"\n  R - Show next 5 themes ({remaining} more available)")
            else:
                print(f"\n  R - Back to first 5 themes")
            print(f"  C - Custom theme")

            choice = input("\nEnter choice (1-5, R, C): ").strip().upper()

            if choice == 'C':
                theme = input("Enter custom theme: ").strip()
                if theme:
                    return (theme, 'custom')
            elif choice == 'R':
                current_offset = (current_offset + 5) % len(all_themes)
                continue
            elif choice.isdigit() and 1 <= int(choice) <= len(themes_to_show):
                return (themes_to_show[int(choice) - 1], 'random')
            else:
                print(f"❌ Invalid choice. Please enter 1-5, R, or C.")

    def interactive_style_selection(self) -> Dict:
        """
        Interactive style selection for content.

        Returns:
            Dict with tone, social_length, audience, blog_focus
        """
        print("\n" + "="*80)
        print("CONTENT STYLE")
        print("="*80)

        # Tone
        print("\nTONE:")
        print("  1. Professional & Clinical")
        print("  2. Warm & Empathetic (Recommended)")
        print("  3. Educational & Informative")
        print("  4. Personal & Story-Based")

        while True:
            tone_choice = input("\nEnter tone (1-4): ").strip()
            if tone_choice in ['1', '2', '3', '4']:
                break
            print("❌ Invalid choice. Please enter 1-4.")

        tone_map = {
            '1': 'professional',
            '2': 'warm_empathetic',
            '3': 'educational',
            '4': 'personal'
        }

        # Social post length
        print("\nSOCIAL POST LENGTH:")
        print("  1. Short (150 words)")
        print("  2. Medium (200 words) (Recommended)")
        print("  3. Longer (250 words)")

        while True:
            length_choice = input("\nEnter length (1-3): ").strip()
            if length_choice in ['1', '2', '3']:
                break
            print("❌ Invalid choice. Please enter 1-3.")

        length_map = {
            '1': 150,
            '2': 200,
            '3': 250
        }

        # Target audience
        print("\nTARGET AUDIENCE:")
        print("  1. General audience")
        print("  2. Parents")
        print("  3. Couples")
        print("  4. Teens/Young adults")
        print("  5. Adults seeking individual therapy")

        while True:
            audience_choice = input("\nEnter audience (1-5): ").strip()
            if audience_choice in ['1', '2', '3', '4', '5']:
                break
            print("❌ Invalid choice. Please enter 1-5.")

        audience_map = {
            '1': 'general',
            '2': 'parents',
            '3': 'couples',
            '4': 'teens',
            '5': 'adults_individual'
        }

        # Blog focus
        print("\nBLOG FOCUS:")
        print("  1. Comprehensive guide (covers everything)")
        print("  2. Focus on practical strategies")
        print("  3. Focus on when to seek help")
        print("  4. Local resources emphasis (Hendersonville NC)")

        while True:
            blog_choice = input("\nEnter blog focus (1-4): ").strip()
            if blog_choice in ['1', '2', '3', '4']:
                break
            print("❌ Invalid choice. Please enter 1-4.")

        blog_focus_map = {
            '1': 'comprehensive',
            '2': 'practical_strategies',
            '3': 'seeking_help',
            '4': 'local_resources'
        }

        style = {
            'tone': tone_map[tone_choice],
            'social_length': length_map[length_choice],
            'audience': audience_map[audience_choice],
            'blog_focus': blog_focus_map[blog_choice]
        }

        # Display confirmation
        print("\n✓ Style confirmed:")
        tone_names = {
            'professional': 'Professional & Clinical',
            'warm_empathetic': 'Warm & Empathetic',
            'educational': 'Educational & Informative',
            'personal': 'Personal & Story-Based'
        }
        audience_names = {
            'general': 'General audience',
            'parents': 'Parents',
            'couples': 'Couples',
            'teens': 'Teens/Young adults',
            'adults_individual': 'Adults seeking individual therapy'
        }
        blog_names = {
            'comprehensive': 'Comprehensive guide',
            'practical_strategies': 'Practical strategies focus',
            'seeking_help': 'When to seek help focus',
            'local_resources': 'Local resources emphasis'
        }

        print(f"  • Tone: {tone_names[style['tone']]}")
        print(f"  • Social length: {style['social_length']} words")
        print(f"  • Audience: {audience_names[style['audience']]}")
        print(f"  • Blog focus: {blog_names[style['blog_focus']]}")

        return style

    def generate_social_angles(self, theme: str, count: int = 8) -> List[str]:
        """
        Generate unique social media angles from a theme.

        Args:
            theme: Main theme
            count: Number of angles to generate (default 8 for Mon-Thu)

        Returns:
            List of unique angle topics
        """
        # For now, generate simple variations
        # In production, could use AI to generate these

        base_angles = [
            f"Quick Tips: {theme}",
            f"Understanding {theme}",
            f"Common Myths About {theme}",
            f"How to Talk About {theme}",
            f"Signs You Need Help With {theme}",
            f"{theme}: What to Expect in Therapy",
            f"Supporting a Loved One With {theme}",
            f"{theme} and Self-Care Strategies"
        ]

        return base_angles[:count]

    def create_social_post(
        self,
        angle: str,
        theme: str,
        platform: str,
        style: Dict,
        api_key: str
    ) -> Optional[Dict]:
        """Create a single social media post."""

        tone_prompts = {
            'professional': "Use a professional, clinical tone with evidence-based language.",
            'warm_empathetic': "Use a warm, empathetic, and supportive tone that connects emotionally.",
            'educational': "Use an educational, informative tone that teaches and explains clearly.",
            'personal': "Use a personal, story-based tone that shares relatable experiences."
        }

        audience_prompts = {
            'general': "adults in Hendersonville NC seeking mental health support",
            'parents': "parents in Western NC concerned about their children's mental health",
            'couples': "couples in Hendersonville NC seeking relationship support",
            'teens': "teenagers and young adults in Western NC",
            'adults_individual': "adults in Hendersonville NC seeking individual therapy"
        }

        prompt = f"""Create a {platform} post about: {angle}

MAIN THEME: {theme}

TARGET AUDIENCE: {audience_prompts[style['audience']]}

REQUIREMENTS:
- {tone_prompts[style['tone']]}
- Approximately {style['social_length']} words
- HIPAA compliant (no diagnosis, no treatment advice)
- Include practical insights or tips
- Professional yet approachable
- Clear call-to-action for therapy consultation
- 5-8 relevant hashtags (mix of popular and niche)
- Visual content suggestions

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
                "content_type": f"{platform.lower()}-post",
                "title": angle,
                "theme": theme,
                "created_date": datetime.now().isoformat(),
                "created_by_agent": "interactive-batch-creator",
                "status": "scheduled",
                "content_details": {
                    "platform": platform,
                    "target_audience": style['audience'],
                    "tone": style['tone'],
                    "word_count": style['social_length']
                },
                "performance": {
                    "views": 0,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0
                },
                "compliance": {
                    "hipaa_reviewed": True,
                    "contains_phi": False
                }
            }

            return {
                "content": content_text,
                "metadata": metadata,
                "filename": f"{angle.lower().replace(' ', '-')[:50]}-{content_id}"
            }

        except Exception as e:
            print(f"  ❌ Error creating content: {str(e)}")
            return None

    def create_blog_post(
        self,
        theme: str,
        style: Dict,
        api_key: str
    ) -> Optional[Path]:
        """
        Create PRD v2.2 compliant blog post.

        Returns:
            Path to blog folder containing all files
        """

        blog_focus_prompts = {
            'comprehensive': "Create a comprehensive guide that covers all aspects of the topic thoroughly.",
            'practical_strategies': "Focus heavily on practical, actionable strategies readers can implement immediately.",
            'seeking_help': "Emphasize when and how to seek professional help, with clear guidance on taking the first step.",
            'local_resources': "Highlight local Hendersonville NC and Western NC resources prominently throughout."
        }

        tone_prompts = {
            'professional': "professional and clinical",
            'warm_empathetic': "warm, empathetic, and supportive",
            'educational': "educational and informative",
            'personal': "personal and relatable"
        }

        prompt = f"""# COMPREHENSIVE BLOG POST GENERATION - PRD V2.2 COMPLIANT

## CRITICAL: YOUR OUTPUT MUST INCLUDE ALL 5 SECTIONS BELOW

## MAIN THEME: {theme}

## TONE: {tone_prompts[style['tone']]}
## FOCUS: {blog_focus_prompts[style['blog_focus']]}

## SECTION 1: COMPLETE BLOG POST CONTENT (Markdown Format)

Create a 2000-3000 word blog post with:

- **Question-based H1 title** with primary keyword about {theme}
- **Answer-First Snippet** (2-3 sentences at very top)
- **Introduction** (150-200 words) that hooks the reader
- **Question-based H2 section headings** (5-7 sections)
- Each section starts with 2-3 sentence answer-first snippet
- **FAQ Section** with 5 Q&A pairs related to {theme}
- **Conclusion** with clear CTA for Hendersonville Counseling
- **References section** with professional insights

Requirements:
- HIPAA compliant (no diagnosis via blog)
- E-E-A-T focus (Experience, Expertise, Authority, Trust)
- Local SEO (mention Hendersonville NC, Western NC)
- Professional insights demonstrating expertise
- 2-3 internal link suggestions
- 2-3 external credible source links

## SECTION 2: SCHEMA MARKUP TEMPLATES (JSON Format)

Provide TWO separate JSON objects:

### BlogPosting Schema:
```json
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Blog title]",
  "description": "[150 char description]",
  "author": {{
    "@type": "Person",
    "name": "Hendersonville Counseling Team"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Hendersonville Counseling",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://hendersonvillecounseling.com/logo.png"
    }}
  }},
  "datePublished": "2025-11-15",
  "image": "https://hendersonvillecounseling.com/blog-images/[slug].jpg"
}}
```

### FAQPage Schema:
```json
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "[Question 1]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Answer 1]"
      }}
    }},
    ... (5 total Q&As)
  ]
}}
```

## SECTION 3: SOCIAL MEDIA CONTENT PACKAGE

Create 3 caption variants for promoting this blog:

### Caption Variant 1: Educational
(150-200 words, focuses on teaching key concept)

### Caption Variant 2: Empathetic
(150-200 words, focuses on emotional connection)

### Caption Variant 3: Call-to-Action
(150-200 words, focuses on taking action)

Each with:
- Complete caption text
- 8-10 relevant hashtags
- Posting suggestion (best platform/time)

## SECTION 4: INSTAGRAM CAROUSEL PROMPTS (10 Slides)

Provide copy for 10 carousel slides:

**Slide 1:** Hook with "Swipe →" and main benefit
**Slides 2-6:** Key points from blog (one per slide)
**Slides 7-8:** Additional insights or tips
**Slide 9:** Strong CTA
**Slide 10:** Resources/contact info

Plus: Complete carousel caption with hashtags

## SECTION 5: SEO METADATA & PUBLISHING CHECKLIST

Provide:
- **SEO Title** (60 characters, includes primary keyword)
- **Meta Description** (155 characters, compelling with CTA)
- **URL Slug** (lowercase, hyphens, includes keyword)
- **Primary Keyword** + 5-7 **Semantic Keywords** (LSI)
- **Categories** (2-3)
- **Tags** (5-7)
- **Featured Image Alt Text**
- **Internal Link Suggestions** (2-3 service pages)
- **External Link Suggestions** (2-3 credible sources)

---

TARGET AUDIENCE: Adults seeking therapy in Hendersonville NC and Western NC
PRACTICE: Hendersonville Counseling
LOCATION: Hendersonville NC, Western NC
SERVICES: Individual therapy, couples counseling, teen therapy, anxiety treatment, ADHD support, trauma therapy (EMDR)

Please generate all 5 sections following PRD v2.2 requirements exactly."""

        try:
            print(f"\n🤖 Creating comprehensive blog post...")
            print(f"   Theme: {theme}")
            print(f"   This will take 2-3 minutes...")

            client = anthropic.Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )

            blog_content = message.content[0].text

            # Create blog folder
            slug = theme.lower().replace(' ', '-').replace(':', '').replace(',', '')[:50]
            content_id = str(uuid.uuid4())[:8]
            blog_folder = self.blog_path / "drafts" / f"{slug}-{content_id}"
            blog_folder.mkdir(parents=True, exist_ok=True)

            # Create descriptive filename from theme
            blog_filename = slug + ".md"

            # Save main blog post with descriptive name
            blog_file = blog_folder / blog_filename
            with open(blog_file, 'w') as f:
                f.write(f"# Blog Post: {theme}\n\n")
                f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"**Theme:** {theme}\n")
                f.write(f"**Tone:** {style['tone']}\n")
                f.write(f"**Focus:** {style['blog_focus']}\n\n")
                f.write("---\n\n")
                f.write(blog_content)

            # Create README with instructions
            readme_file = blog_folder / "README.md"
            with open(readme_file, 'w') as f:
                f.write(f"# Blog Post: {theme}\n\n")
                f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("## Files in This Folder\n\n")
                f.write(f"- `{blog_filename}` - Complete blog content with all 5 sections\n")
                f.write("- `README.md` - This file (publishing instructions)\n\n")
                f.write("## Publishing Workflow\n\n")
                f.write("1. **Extract Content:**\n")
                f.write("   - Open `blog-post.md`\n")
                f.write("   - Section 1: Blog content → Copy to Squarespace\n")
                f.write("   - Section 2: Schema JSONs → Copy to JSONKeeper.com\n")
                f.write("   - Section 3: Social captions → Use for promotion\n")
                f.write("   - Section 4: Carousel → Use for Instagram graphics\n")
                f.write("   - Section 5: SEO metadata → Add to Squarespace settings\n\n")
                f.write("2. **Publish to Squarespace:**\n")
                f.write("   - Log into Squarespace\n")
                f.write("   - Create new blog post\n")
                f.write("   - Paste Section 1 content\n")
                f.write("   - Add SEO metadata (Section 5)\n")
                f.write("   - Upload featured image\n\n")
                f.write("3. **Add Schema Markup:**\n")
                f.write("   - Copy BlogPosting JSON → JSONKeeper.com → Get URL\n")
                f.write("   - Copy FAQPage JSON → JSONKeeper.com → Get URL\n")
                f.write("   - Add schema code to Squarespace (Settings → Advanced → Code Injection)\n\n")
                f.write("4. **Publish & Promote:**\n")
                f.write("   - Publish blog on Friday\n")
                f.write("   - Use social captions (Section 3) to promote throughout week\n")
                f.write("   - Create carousel graphics using Section 4 prompts\n\n")

            print(f"  ✓ Blog post created: {blog_folder.relative_to(Path.cwd())}")

            return blog_folder

        except Exception as e:
            print(f"  ❌ Error creating blog: {str(e)}")
            return None

    def save_social_content(self, content_data: Dict, platform: str, date: str) -> Optional[Path]:
        """Save social media content to appropriate folder."""

        platform_folders = {
            "Instagram": self.library_path / "instagram" / "feed-posts" / "scheduled",
            "Facebook": self.library_path / "facebook" / "posts" / "scheduled",
            "LinkedIn": self.library_path / "linkedin" / "articles" / "scheduled"
        }

        folder = platform_folders.get(platform)
        if not folder:
            return None

        folder.mkdir(parents=True, exist_ok=True)

        # Add date to filename for organization
        filename_base = f"{content_data['filename']}-{date}"

        # Save content markdown
        content_file = folder / f"{filename_base}.md"
        with open(content_file, 'w') as f:
            f.write(content_data["content"])

        # Save metadata
        meta_file = folder / f"{filename_base}_meta.json"
        with open(meta_file, 'w') as f:
            json.dump(content_data["metadata"], f, indent=2)

        return content_file

    def extract_preview_and_hashtags(self, content_file: Path) -> Tuple[str, List[str]]:
        """Extract preview text and hashtags from content file."""
        try:
            with open(content_file, 'r') as f:
                content = f.read()

            # Extract first 100 chars as preview
            lines = content.split('\n')
            preview_text = ""
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('**'):
                    preview_text = line.strip()[:100]
                    break

            # Extract hashtags
            hashtags = []
            for line in lines:
                if line.startswith('#') and not line.startswith('##'):
                    tags = [word for word in line.split() if word.startswith('#')]
                    hashtags.extend(tags[:5])  # Get first 5 hashtags
                    break

            return (preview_text if preview_text else "Preview not available", hashtags)
        except:
            return ("Preview not available", [])

    def generate_weekly_summary(
        self,
        week_start: str,
        theme: str,
        created_social: List[Dict],
        blog_folder: Optional[Path],
        style: Dict
    ):
        """Generate comprehensive weekly content summary file."""

        week_dt = datetime.fromisoformat(week_start)
        week_number = week_dt.isocalendar()[1]
        year = week_dt.year

        # Get batch folder
        batch_folder = self.library_path / "weekly-batches" / f"{year}-week-{week_number:02d}"
        batch_folder.mkdir(parents=True, exist_ok=True)

        summary_file = batch_folder / f"WEEK_{week_number}_CONTENT_SUMMARY.md"

        with open(summary_file, 'w') as f:
            # Header
            f.write(f"# Week {week_number} Content Summary ({week_start})\n\n")
            f.write(f"**Theme:** {theme}  \n")
            f.write(f"**Created:** {datetime.now().strftime('%B %d, %Y')}  \n")
            f.write(f"**Total Pieces:** {len(created_social)} social posts")
            if blog_folder:
                f.write(" + 1 blog = {} pieces  \n".format(len(created_social) + 1))
            else:
                f.write("  \n")
            f.write(f"**Status:** ⬜ Not Scheduled | ⬜ Images Created | ⬜ Scheduled | ⬜ Posted\n\n")
            f.write("---\n\n")

            # Checklist
            f.write("## CHECKLIST\n\n")
            f.write(f"- [ ] Review all {len(created_social)} social posts\n")
            if blog_folder:
                f.write("- [ ] Review blog post\n")
            f.write(f"- [ ] Create images for social posts ({len(created_social)} images needed)\n")
            if blog_folder:
                f.write("- [ ] Create blog featured image (1 image)\n")

            # Count posts by platform
            instagram_count = sum(1 for p in created_social if p['platform'] == 'Instagram')
            facebook_count = sum(1 for p in created_social if p['platform'] == 'Facebook')
            linkedin_count = sum(1 for p in created_social if p['platform'] == 'LinkedIn')

            if instagram_count > 0:
                f.write(f"- [ ] Schedule Instagram posts ({instagram_count} posts)\n")
            if facebook_count > 0:
                f.write(f"- [ ] Schedule Facebook posts ({facebook_count} posts)\n")
            if linkedin_count > 0:
                f.write(f"- [ ] Schedule LinkedIn posts ({linkedin_count} posts)\n")

            if blog_folder:
                f.write("- [ ] Publish blog to Squarespace (Friday)\n")
                f.write("- [ ] Upload schema JSONs to JSONKeeper\n")

            f.write("- [ ] Track performance with weekly_checkin.py\n\n")
            f.write("---\n\n")

            # Social media posts grouped by platform
            f.write(f"## SOCIAL MEDIA POSTS ({len(created_social)})\n\n")

            for platform in ['Instagram', 'Facebook', 'LinkedIn']:
                platform_posts = [p for p in created_social if p['platform'] == platform]
                if not platform_posts:
                    continue

                f.write(f"### {platform.upper()} ({len(platform_posts)} posts)\n\n")

                for i, post in enumerate(platform_posts, 1):
                    day_name = post['day']
                    file_path = post['file']

                    # Extract preview and hashtags
                    preview, hashtags = self.extract_preview_and_hashtags(file_path)

                    # Get topic from filename
                    topic = file_path.stem.replace('-', ' ').title()

                    f.write(f"#### Post {i}: {day_name}\n")
                    f.write(f"- **File:** `{file_path.relative_to(self.library_path.parent)}`\n")
                    f.write(f"- **Topic:** {topic}\n")
                    f.write(f"- **Preview:** \"{preview}...\"\n")
                    if hashtags:
                        f.write(f"- **Hashtags:** {' '.join(hashtags[:5])}\n")
                    f.write(f"- **Image needed:** ✏️ [Describe image needed]\n")
                    f.write(f"- **Scheduled:** ⬜\n\n")

            f.write("---\n\n")

            # Blog post section
            if blog_folder:
                friday_date = (week_dt + timedelta(days=4)).strftime('%A, %B %d')
                f.write(f"## BLOG POST ({friday_date})\n\n")
                f.write(f"**Title:** {theme}  \n")
                f.write(f"**Folder:** `{blog_folder.relative_to(self.library_path.parent)}/`\n\n")

                # List files in blog folder
                f.write("### Files:\n")
                blog_files = list(blog_folder.glob("*.md"))
                if blog_files:
                    main_blog_file = [f for f in blog_files if f.name != 'README.md'][0]
                    f.write(f"- **Main Content:** `{main_blog_file.name}` (2000-3000 words)\n")
                f.write("- **Schema #1:** Extract BlogPosting schema → Upload to JSONKeeper.com\n")
                f.write("- **Schema #2:** Extract FAQPage schema → Upload to JSONKeeper.com\n")
                f.write("- **Social Captions:** Extract from Section 3 (3 variants for promotion)\n")
                f.write("- **Carousel Prompts:** Extract from Section 4 (10 slides)\n")
                f.write("- **SEO Metadata:** Extract from Section 5\n\n")

                f.write("### Publishing Checklist:\n")
                f.write("- [ ] Create featured image (2400x1260px recommended)\n")
                f.write("- [ ] Copy blog content to Squarespace\n")
                f.write("- [ ] Upload schemas to JSONKeeper → Get URLs\n")
                f.write("- [ ] Add schema code to Squarespace (Code Injection)\n")
                f.write("- [ ] Add SEO metadata (title, description, URL slug)\n")
                f.write(f"- [ ] Schedule for {friday_date}\n")
                f.write("- [ ] Create carousel graphics (use prompts from blog)\n\n")

                f.write("### Blog Preview:\n")
                f.write(f"_A comprehensive {style['social_length']}-word guide exploring {theme.lower()} ")
                f.write("with practical strategies, professional insights, and local Hendersonville NC resources..._\n\n")

                f.write("---\n\n")

            # Image requirements summary
            f.write("## IMAGE REQUIREMENTS SUMMARY\n\n")
            f.write(f"**Total Images Needed:** {len(created_social)}")
            if blog_folder:
                f.write(f" + 1 = {len(created_social) + 1}\n\n")
            else:
                f.write("\n\n")

            for platform in ['Instagram', 'Facebook', 'LinkedIn']:
                platform_posts = [p for p in created_social if p['platform'] == platform]
                if platform_posts:
                    f.write(f"**{platform} ({len(platform_posts)}):**\n")
                    for i, post in enumerate(platform_posts, 1):
                        f.write(f"{i}. [Describe image for {post['day']} post]\n")
                    f.write("\n")

            if blog_folder:
                f.write("**Blog (1):**\n")
                f.write("1. Featured image (2400x1260px) - Related to theme\n\n")

            f.write("---\n\n")

            # Quick file access
            f.write("## QUICK FILE ACCESS\n\n")
            f.write("**Open all content folders:**\n")
            f.write("```bash\n")
            f.write(f"cd {self.library_path.relative_to(Path.cwd())}\n")
            f.write("open instagram/feed-posts/scheduled\n")
            f.write("open facebook/posts/scheduled\n")
            f.write("open linkedin/articles/scheduled\n")
            if blog_folder:
                f.write(f"open {blog_folder.relative_to(Path.cwd())}\n")
            f.write("```\n\n")

            f.write("---\n\n")

            # Notes section
            f.write("## NOTES FOR NEXT WEEK\n\n")
            f.write(f"- {theme} content created\n")
            f.write("- [Add your observations here after posting]\n")
            f.write("- [Track what performed well]\n\n")

            f.write("---\n\n")
            f.write(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}  \n")
            f.write(f"**Next Week (Week {week_number + 1}):** Generate content by {(week_dt + timedelta(days=7)).strftime('%B %d')}\n")

        return summary_file

    def create_interactive_batch(
        self,
        week_start: str,
        with_blog: bool = False
    ):
        """Main interactive workflow."""

        week_dt = datetime.fromisoformat(week_start)
        week_end = week_dt + timedelta(days=6)

        # Load observances
        from create_weekly_batch import WeeklyBatchCreator
        temp_creator = WeeklyBatchCreator()
        observances = temp_creator.find_relevant_observances(week_dt, week_end, lead_time_days=14)

        # Step 1: Interactive theme selection
        theme, mode = self.interactive_theme_selection(observances)

        print(f"\n✓ Theme selected: {theme}")
        print(f"  Mode: {mode}")

        # Step 2: Interactive style selection
        style = self.interactive_style_selection()

        # Get API key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("\n❌ Error: ANTHROPIC_API_KEY not found in environment")
            print("   Make sure your .env file is set up correctly")
            return

        # Step 3: Generate social post angles
        print("\n" + "="*80)
        print("CREATING CONTENT")
        print("="*80)

        social_angles = self.generate_social_angles(theme, count=8)

        print(f"\n🤖 Generating 8 social posts + 1 blog post...")
        print(f"   Theme: {theme}")
        print(f"   This will take 5-10 minutes...\n")

        # Distribution: 2 posts per day Mon-Thu across 3 platforms
        posting_schedule = [
            {"day": "Monday", "date": (week_dt + timedelta(days=0)).strftime('%Y-%m-%d'), "platform": "Instagram"},
            {"day": "Monday", "date": (week_dt + timedelta(days=0)).strftime('%Y-%m-%d'), "platform": "LinkedIn"},
            {"day": "Tuesday", "date": (week_dt + timedelta(days=1)).strftime('%Y-%m-%d'), "platform": "Facebook"},
            {"day": "Tuesday", "date": (week_dt + timedelta(days=1)).strftime('%Y-%m-%d'), "platform": "Instagram"},
            {"day": "Wednesday", "date": (week_dt + timedelta(days=2)).strftime('%Y-%m-%d'), "platform": "Instagram"},
            {"day": "Wednesday", "date": (week_dt + timedelta(days=2)).strftime('%Y-%m-%d'), "platform": "LinkedIn"},
            {"day": "Thursday", "date": (week_dt + timedelta(days=3)).strftime('%Y-%m-%d'), "platform": "Facebook"},
            {"day": "Thursday", "date": (week_dt + timedelta(days=3)).strftime('%Y-%m-%d'), "platform": "Instagram"},
        ]

        # Create social posts
        created_social = []
        for i, (angle, schedule_item) in enumerate(zip(social_angles, posting_schedule), 1):
            print(f"[{i}/8] {schedule_item['day']} {schedule_item['platform']}: {angle[:50]}...")

            content_data = self.create_social_post(
                angle=angle,
                theme=theme,
                platform=schedule_item['platform'],
                style=style,
                api_key=api_key
            )

            if content_data:
                content_file = self.save_social_content(
                    content_data,
                    schedule_item['platform'],
                    schedule_item['date']
                )

                if content_file:
                    print(f"  ✓ Created and saved")
                    created_social.append({
                        "day": schedule_item['day'],
                        "platform": schedule_item['platform'],
                        "file": content_file
                    })
                else:
                    print(f"  ❌ Failed to save")
            else:
                print(f"  ❌ Failed to create")

        # Create blog post if requested
        blog_folder = None
        if with_blog:
            print(f"\n[9/9] Friday Blog: {theme}")
            blog_folder = self.create_blog_post(theme, style, api_key)

        # Generate weekly content summary
        print(f"\n📋 Generating weekly content summary...")
        summary_file = self.generate_weekly_summary(
            week_start=week_start,
            theme=theme,
            created_social=created_social,
            blog_folder=blog_folder,
            style=style
        )

        # Summary
        print("\n" + "="*80)
        print("BATCH CREATION COMPLETE")
        print("="*80)

        print(f"\n✓ Successfully created: {len(created_social)} social posts" + (" + 1 blog post" if blog_folder else ""))

        print(f"\n📁 Content saved to:")
        print(f"   Social posts: social-media-content/[platform]/scheduled/")
        if blog_folder:
            print(f"   Blog post: {blog_folder.relative_to(Path.cwd())}")
        print(f"\n📋 Weekly Content Summary:")
        print(f"   {summary_file.relative_to(Path.cwd())}")
        print(f"   ✨ Open this file to review everything in one place!")

        print(f"\n🗓️ Your Posting Schedule:")
        current_day = None
        for item in created_social:
            if item['day'] != current_day:
                current_day = item['day']
                print(f"\n  {current_day}:")
            print(f"    • {item['platform']}")

        if blog_folder:
            friday_date = (week_dt + timedelta(days=4)).strftime('%A, %B %d')
            print(f"\n  Friday ({friday_date}):")
            print(f"    • Blog post (Squarespace)")

        print(f"\n🎯 Next steps:")
        print(f"   1. Open Weekly Content Summary (your master checklist)")
        print(f"   2. Review all content and create images")
        print(f"   3. Batch schedule everything in your scheduler")
        if blog_folder:
            print(f"   4. Publish Friday blog to Squarespace")
        print(f"   5. Track performance with weekly_checkin.py after posting")
        print()


def main():
    """CLI interface."""

    parser = argparse.ArgumentParser(
        description="Interactive weekly batch content creator with blog integration"
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
        "--interactive",
        action="store_true",
        help="Use interactive mode with theme and style selection"
    )

    parser.add_argument(
        "--with-blog",
        action="store_true",
        help="Include PRD v2.2 compliant blog post (Friday)"
    )

    args = parser.parse_args()

    # Validate week format
    try:
        datetime.fromisoformat(args.week)
    except ValueError:
        print(f"❌ Error: Invalid date format '{args.week}'")
        print("   Use YYYY-MM-DD format (e.g., 2025-11-04)")
        sys.exit(1)

    if not args.interactive:
        print("❌ Error: This version requires --interactive flag")
        print("   Use: python create_weekly_batch_v2.py --week YYYY-MM-DD --use-api --interactive --with-blog")
        sys.exit(1)

    if not args.use_api:
        print("❌ Error: This version requires --use-api flag")
        print("   Interactive mode requires API to generate content")
        sys.exit(1)

    # Initialize and run
    creator = InteractiveWeeklyBatchCreator()
    creator.create_interactive_batch(
        week_start=args.week,
        with_blog=args.with_blog
    )


if __name__ == "__main__":
    main()
