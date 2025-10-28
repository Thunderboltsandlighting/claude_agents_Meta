#!/usr/bin/env python3
"""
Initialize Content Library Structure

Creates the complete folder structure for organizing social media content
created by therapy practice agents.
"""

from pathlib import Path
import json
from datetime import datetime


def create_content_library_structure(base_path: Path = None):
    """
    Create the complete content library folder structure.

    Args:
        base_path: Base path for the therapy practice project
                   If None, uses script's parent directory
    """
    if base_path is None:
        base_path = Path(__file__).parent

    content_root = base_path / "social-media-content"

    # Define complete folder structure
    folders = [
        # Blogs
        "blogs/published",
        "blogs/scheduled",
        "blogs/drafts",
        "blogs/published/archive",

        # Instagram
        "instagram/feed-posts/published",
        "instagram/feed-posts/scheduled",
        "instagram/feed-posts/drafts",
        "instagram/reels/published",
        "instagram/reels/scheduled",
        "instagram/reels/drafts",
        "instagram/stories/published",
        "instagram/stories/scheduled",
        "instagram/stories/drafts",

        # Facebook
        "facebook/feed-posts/published",
        "facebook/feed-posts/scheduled",
        "facebook/feed-posts/drafts",
        "facebook/reels/published",
        "facebook/reels/scheduled",
        "facebook/reels/drafts",

        # LinkedIn
        "linkedin/posts/published",
        "linkedin/posts/scheduled",
        "linkedin/posts/drafts",
        "linkedin/articles/published",
        "linkedin/articles/scheduled",
        "linkedin/articles/drafts",

        # Organization folders
        "weekly-batches",
        "campaigns",
        "templates"
    ]

    # Create all folders
    created_folders = []
    for folder_path in folders:
        full_path = content_root / folder_path
        full_path.mkdir(parents=True, exist_ok=True)
        created_folders.append(str(full_path.relative_to(base_path)))

    # Create .gitkeep files to preserve empty folders in git
    for folder_path in folders:
        full_path = content_root / folder_path
        gitkeep_file = full_path / ".gitkeep"
        gitkeep_file.touch()

    # Create README files for main folders
    create_readme_files(content_root)

    # Create library configuration file
    create_library_config(content_root)

    return created_folders


def create_readme_files(content_root: Path):
    """Create README files for main content folders."""

    readme_content = {
        "blogs": """# Blog Posts

This folder contains all blog posts created for the therapy practice.

## Organization:
- **drafts/**: Work in progress, not yet scheduled
- **scheduled/**: Approved posts with scheduled publish dates
- **published/**: Live posts that have been published
- **published/archive/**: Older posts for historical reference

## Naming Convention:
`YYYY-MM-DD_blog_topic-slug.md`

Example: `2025-10-27_blog_anxiety-coping-strategies.md`
""",

        "instagram": """# Instagram Content

This folder contains all Instagram content created for the therapy practice.

## Organization:
- **feed-posts/**: Standard Instagram feed posts
- **reels/**: Short-form video content for Instagram Reels
- **stories/**: 24-hour Instagram Stories content

Each subfolder has: drafts/, scheduled/, published/

## Naming Convention:
`YYYY-MM-DD_instagram-{type}_topic-slug.md`

Examples:
- `2025-10-27_instagram-feed_grounding-technique.md`
- `2025-10-28_instagram-reel_breathing-exercise.md`
""",

        "facebook": """# Facebook Content

This folder contains all Facebook content created for the therapy practice.

## Organization:
- **feed-posts/**: Standard Facebook posts
- **reels/**: Short-form video content for Facebook Reels

Each subfolder has: drafts/, scheduled/, published/

## Naming Convention:
`YYYY-MM-DD_facebook-{type}_topic-slug.md`

Examples:
- `2025-10-27_facebook-post_couples-therapy-benefits.md`
- `2025-10-28_facebook-reel_quick-stress-relief.md`
""",

        "linkedin": """# LinkedIn Content

This folder contains all LinkedIn content created for the therapy practice.

## Organization:
- **posts/**: Standard LinkedIn posts (shorter, 200-400 words)
- **articles/**: LinkedIn articles (longer, 800-2000 words)

Each subfolder has: drafts/, scheduled/, published/

## Naming Convention:
`YYYY-MM-DD_linkedin-{type}_topic-slug.md`

Examples:
- `2025-10-27_linkedin-post_workplace-burnout.md`
- `2025-10-28_linkedin-article_mental-health-workplace.md`
""",

        "weekly-batches": """# Weekly Content Batches

This folder contains weekly batches of content created together as part of
the weekly content strategy process.

## Organization:
Each week gets its own folder: `YYYY-week-{week_number}/`

Example: `2025-week-43/` for the 43rd week of 2025

## Contents:
Each weekly folder contains:
- `weekly_plan.md`: Content strategy for the week
- Individual content files with metadata
- Performance tracking for the week's content

## Naming Convention:
`YYYY-week-{week_number}/`

Example: `2025-week-43/`
""",

        "campaigns": """# Content Campaigns

This folder contains content organized by marketing campaigns or themes.

## Organization:
Each campaign gets its own folder with a descriptive name.

## Examples:
- `anxiety-awareness-november-2025/`
- `couples-therapy-valentines-2026/`
- `emdr-education-series-2025/`

## Contents:
Each campaign folder contains:
- `campaign_plan.md`: Strategy and goals for the campaign
- All content pieces for the campaign
- Performance tracking
- Related assets (images, graphics, etc.)

## Benefits:
- Easy to see all content for a specific campaign
- Track campaign-level performance
- Reuse successful campaign structures
""",

        "templates": """# Content Templates

This folder contains reusable content templates and examples.

## Organization:
Templates for different content types and formats.

## Contents:
- Blog post templates
- Social media post templates
- Metadata templates
- Example successful posts

## Usage:
Copy templates as starting points for new content creation.
"""
    }

    for folder, content in readme_content.items():
        readme_path = content_root / folder / "README.md"
        with open(readme_path, 'w') as f:
            f.write(content)


def create_library_config(content_root: Path):
    """Create library configuration file."""

    config = {
        "library_name": "Therapy Practice Social Media Content Library",
        "created_date": datetime.now().isoformat(),
        "version": "1.0.0",

        "content_types": {
            "blog": {
                "folder": "blogs",
                "naming_pattern": "YYYY-MM-DD_blog_topic-slug.md",
                "typical_word_count": "1500-3000",
                "review_required": True
            },
            "instagram-feed": {
                "folder": "instagram/feed-posts",
                "naming_pattern": "YYYY-MM-DD_instagram-feed_topic-slug.md",
                "typical_word_count": "150-250",
                "review_required": True
            },
            "instagram-reel": {
                "folder": "instagram/reels",
                "naming_pattern": "YYYY-MM-DD_instagram-reel_topic-slug.md",
                "typical_word_count": "50-100",
                "review_required": True
            },
            "facebook-post": {
                "folder": "facebook/feed-posts",
                "naming_pattern": "YYYY-MM-DD_facebook-post_topic-slug.md",
                "typical_word_count": "100-250",
                "review_required": True
            },
            "linkedin-post": {
                "folder": "linkedin/posts",
                "naming_pattern": "YYYY-MM-DD_linkedin-post_topic-slug.md",
                "typical_word_count": "200-400",
                "review_required": True
            }
        },

        "status_folders": {
            "draft": "Content being created or reviewed",
            "scheduled": "Content approved and scheduled for publishing",
            "published": "Content that has been published live",
            "archive": "Older content for historical reference"
        },

        "metadata_schema_version": "1.0",

        "optimal_posting_times": {
            "instagram": {
                "weekday": ["09:00", "12:00", "17:00"],
                "weekend": ["10:00", "14:00"]
            },
            "facebook": {
                "weekday": ["09:00", "13:00", "15:00"],
                "weekend": ["11:00", "14:00"]
            },
            "linkedin": {
                "weekday": ["08:00", "12:00", "17:00"],
                "weekend": []  # LinkedIn is primarily weekday platform
            }
        },

        "compliance": {
            "hipaa_check_required": True,
            "phi_check_required": True,
            "crisis_resources_required": True,
            "ethical_review_required": True
        }
    }

    config_path = content_root / "library_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Created library configuration: {config_path}")


def create_example_content():
    """Create example content and metadata to demonstrate the system."""

    base_path = Path(__file__).parent
    content_root = base_path / "social-media-content"

    # Example blog post metadata
    example_blog_meta = {
        "content_id": "example-001",
        "content_type": "blog",
        "title": "10 Evidence-Based Anxiety Coping Strategies",
        "topic": "anxiety coping strategies",
        "created_date": datetime.now().isoformat(),
        "created_by_agent": "therapy-practice-content-creator",
        "status": "draft",

        "scheduling": {
            "scheduled_date": None,
            "scheduled_time_local": None,
            "posting_day": None,
            "optimal_posting_time": False,
            "timezone": "America/Chicago"
        },

        "content_details": {
            "word_count": 0,
            "reading_time_minutes": 0,
            "platform": "Blog",
            "format": "long-form",
            "target_audience": "adults with anxiety considering therapy"
        },

        "seo": {
            "primary_keyword": "anxiety coping strategies",
            "secondary_keywords": [
                "how to deal with anxiety",
                "anxiety relief techniques"
            ],
            "meta_description": "",
            "focus_keyphrase_density": 0,
            "internal_links": [],
            "external_links": []
        },

        "business_context": {
            "business_goal": "attract_anxiety_therapy_clients",
            "service_promoted": "anxiety-therapy",
            "target_conversion": "consultation_booking"
        },

        "compliance": {
            "hipaa_compliant": True,
            "phi_check": "pending",
            "ethical_review": "pending"
        }
    }

    # Save example metadata template
    templates_path = content_root / "templates"
    template_meta_path = templates_path / "example_blog_metadata_template.json"

    with open(template_meta_path, 'w') as f:
        json.dump(example_blog_meta, f, indent=2)

    print(f"✓ Created example metadata template: {template_meta_path}")

    # Create example content template
    example_blog_content = """# [Blog Title Here]

**Primary Keyword**: [keyword]
**Target Audience**: [audience]
**Word Count Goal**: 1500-3000 words
**Reading Time**: ~12 minutes

---

## Introduction (150-200 words)

[Hook - start with relatable situation or surprising fact]

[Problem statement - what struggle does the reader face?]

[Promise - what will they learn from this post?]

---

## Section 1: [H2 Heading with Keyword]

[Content here - 300-400 words]

### Subsection 1.1 [H3 Heading]

[Detailed explanation]

**Key Takeaway**: [Summary in one sentence]

---

## Section 2: [H2 Heading]

[Content here - 300-400 words]

### Subsection 2.1 [H3 Heading]

[Detailed explanation]

---

## When to Seek Professional Help

[Transition to therapy services - 200-300 words]

[Signs that professional help would be beneficial]

[What therapy can offer]

---

## Conclusion (150-200 words)

[Recap main points]

[Empowering message]

[Clear call-to-action]

---

## Call-to-Action

If you're struggling with [problem], our therapists specialize in [service].

**Schedule a free consultation**: [link]

---

**About the Author**: [Brief bio]

**Related Posts**:
- [Internal link 1]
- [Internal link 2]

**Resources**:
- [External credible source 1]
- [External credible source 2]
"""

    template_content_path = templates_path / "example_blog_content_template.md"
    with open(template_content_path, 'w') as f:
        f.write(example_blog_content)

    print(f"✓ Created example content template: {template_content_path}")


def main():
    """Main execution function."""

    print("=" * 60)
    print("Initializing Content Library Structure")
    print("=" * 60)
    print()

    base_path = Path(__file__).parent
    print(f"Base path: {base_path}")
    print()

    print("Creating folder structure...")
    created_folders = create_content_library_structure(base_path)

    print(f"\n✓ Created {len(created_folders)} folders:")
    for folder in created_folders[:5]:  # Show first 5
        print(f"  - {folder}")
    print(f"  ... and {len(created_folders) - 5} more")

    print("\n✓ Created README files for all main folders")
    print("✓ Created library configuration file")

    print("\nCreating example templates...")
    create_example_content()

    print()
    print("=" * 60)
    print("Content Library Initialized Successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the folder structure in social-media-content/")
    print("2. Read the README files in each folder")
    print("3. Use request_social_post.py to create content")
    print("4. Content will automatically be saved to the appropriate folders")
    print()
    print("View library structure:")
    print("  tree social-media-content/")
    print()


if __name__ == "__main__":
    main()
