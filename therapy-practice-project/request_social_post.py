#!/usr/bin/env python3
"""
Request Social Media Posts from Content Creator Agent
Simple script to generate social media content on demand
"""

import sys
import os
from pathlib import Path
import importlib.util
import json
from datetime import datetime
import uuid
import re
from typing import Dict, Optional, Tuple

# Import configuration helper
try:
    from config import get_api_key, ensure_api_key
except ImportError:
    # Fallback if config.py not available
    def get_api_key():
        return os.environ.get("ANTHROPIC_API_KEY")
    def ensure_api_key():
        key = get_api_key()
        if not key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        return key

# Setup paths
FRAMEWORK_DIR = Path(__file__).parent.parent / "Claude-Agents"

def load_module(name, path):
    """Load Python module from hyphenated filename."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load framework modules
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine


def request_social_post(
    topic: str,
    platform: str = "Instagram",
    content_type: str = "educational",
    target_audience: str = "adults seeking therapy",
    business_goal: str = "attract therapy clients"
):
    """
    Request a social media post from the content creator agent.

    Args:
        topic: What the post should be about
        platform: Instagram, Facebook, or LinkedIn
        content_type: educational, announcement, tip, or testimonial
        target_audience: Who this post is for
        business_goal: What business outcome you want

    Returns:
        Generated prompt ready to use with Claude API
    """

    print("\n" + "="*70)
    print("SOCIAL MEDIA POST REQUEST")
    print("="*70 + "\n")

    # Initialize
    agents_dir = Path(__file__).parent / "agents"
    manager = AgentManager(agents_dir=str(agents_dir))
    engine = PromptEngine()

    # Load content creator
    print("Loading content creator agent...")
    content_creator = manager.load_agent("therapy-practice-content-creator")

    if not content_creator:
        print("❌ Error: Could not load content creator agent")
        return None

    print(f"✓ Loaded: {content_creator.context['role']}\n")

    # Define platform-specific requirements
    platform_specs = {
        "Instagram": {
            "length": "150-250 words",
            "hashtags": "5-10 relevant hashtags",
            "format": "Engaging hook + educational value + CTA",
            "visual": "Include visual content suggestion"
        },
        "Facebook": {
            "length": "100-250 words",
            "hashtags": "3-5 hashtags (optional)",
            "format": "Conversational tone, encourage comments",
            "visual": "Optional image suggestion"
        },
        "LinkedIn": {
            "length": "200-400 words",
            "hashtags": "3-5 professional hashtags",
            "format": "Professional thought-leadership",
            "visual": "Professional image suggestion"
        }
    }

    specs = platform_specs.get(platform, platform_specs["Instagram"])

    # Create detailed task
    task = f"""
Create a {platform} post about: {topic}

**Content Type**: {content_type}
**Target Audience**: {target_audience}
**Business Goal**: {business_goal}

**Platform Requirements for {platform}:**
- Length: {specs['length']}
- Hashtags: {specs['hashtags']}
- Format: {specs['format']}
- Visual: {specs['visual']}

**Content Standards:**
1. Professional but warm and empathetic tone
2. Evidence-based information (cite sources if making claims)
3. HIPAA compliant (no client information)
4. Include crisis resources if topic warrants (988 Suicide & Crisis Lifeline)
5. Clear call-to-action (comment, DM, or book consultation)
6. Person-first language
7. Inclusive and culturally sensitive

**Required Elements:**
- Engaging hook (first line catches attention)
- Educational value or practical tip
- Relatable to target audience
- Call-to-action appropriate to topic
- Professional hashtags
- Visual content suggestion

**Output Format:**
Please provide:
1. The complete social media post text
2. Hashtags (formatted and ready to paste)
3. Visual content suggestion (what image/graphic would work)
4. Best time to post (based on platform and audience)
5. Engagement strategy (how to respond to comments)
"""

    # Generate prompt
    print("Generating prompt...")
    prompt = engine.generate_prompt(
        context=content_creator.context,
        model=content_creator.model,
        tools=content_creator.tools,
        task=task
    )

    print(f"✓ Generated prompt ({len(prompt):,} characters)\n")

    # Display summary
    print("="*70)
    print("REQUEST SUMMARY")
    print("="*70)
    print(f"Topic:           {topic}")
    print(f"Platform:        {platform}")
    print(f"Content Type:    {content_type}")
    print(f"Target Audience: {target_audience}")
    print(f"Business Goal:   {business_goal}")
    print(f"Prompt Length:   {len(prompt):,} characters")
    print("="*70 + "\n")

    return prompt


def create_slug(text: str) -> str:
    """Create URL-friendly slug from text."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length


def get_content_folder(platform: str, content_type: str) -> Path:
    """Get the appropriate folder for content based on platform and type."""
    base_path = Path(__file__).parent / "social-media-content"

    folder_map = {
        "Instagram": {
            "feed": "instagram/feed-posts/drafts",
            "reel": "instagram/reels/drafts",
            "story": "instagram/stories/drafts"
        },
        "Facebook": {
            "post": "facebook/feed-posts/drafts",
            "reel": "facebook/reels/drafts"
        },
        "LinkedIn": {
            "post": "linkedin/posts/drafts",
            "article": "linkedin/articles/drafts"
        }
    }

    # Determine subfolder based on content type
    if platform == "Instagram":
        subfolder = "feed"  # Default to feed
    elif platform == "Facebook":
        subfolder = "post"
    elif platform == "LinkedIn":
        subfolder = "article" if "article" in content_type.lower() else "post"
    else:
        subfolder = "feed"

    folder_path = base_path / folder_map.get(platform, {}).get(subfolder, "instagram/feed-posts/drafts")
    folder_path.mkdir(parents=True, exist_ok=True)

    return folder_path


def create_metadata(
    topic: str,
    platform: str,
    content_type: str,
    target_audience: str,
    business_goal: str,
    social_post: str = None,
    scheduled_date: str = None,
    scheduled_time: str = None
) -> Dict:
    """Create metadata structure for content."""

    # Generate content ID
    content_id = str(uuid.uuid4())[:8]

    # Determine content type code
    if platform == "Instagram":
        type_code = "instagram-feed"
    elif platform == "Facebook":
        type_code = "facebook-post"
    elif platform == "LinkedIn":
        type_code = "linkedin-post"
    else:
        type_code = "social-post"

    # Calculate word count if content provided
    word_count = len(social_post.split()) if social_post else 0

    # Extract hashtags if present
    hashtags = []
    if social_post:
        hashtags = re.findall(r'#\w+', social_post)

    # Build metadata
    metadata = {
        "content_id": content_id,
        "content_type": type_code,
        "title": topic,
        "topic": topic,
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
            "word_count": word_count,
            "reading_time_minutes": max(1, word_count // 200),
            "platform": platform,
            "format": "social-media-post",
            "target_audience": target_audience
        },

        "social_media": {
            "platform": platform,
            "post_type": "feed",
            "hashtags": hashtags[:10] if hashtags else [],
            "caption_length": word_count,
            "has_cta": True,
            "cta_type": "engagement",
            "visual_content_needed": "suggested in post",
            "accessibility": {
                "alt_text": "",
                "captions_required": False
            }
        },

        "business_context": {
            "business_goal": business_goal,
            "service_promoted": "general-therapy",
            "target_conversion": "engagement",
            "campaign": None,
            "content_cluster": None
        },

        "performance": {
            "published_date": None,
            "published_url": None,
            "views": 0,
            "engagement": {
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "saves": 0
            },
            "conversions": {
                "website_clicks": 0,
                "inquiries_generated": 0,
                "bookings_attributed": 0
            }
        },

        "compliance": {
            "hipaa_compliant": True,
            "phi_check": "no_phi_present",
            "ethical_review": "pending",
            "crisis_resources_included": False
        },

        "version_history": [
            {
                "version": 1,
                "date": datetime.now().isoformat(),
                "changes": "Initial creation",
                "modified_by": "therapy-practice-content-creator"
            }
        ],

        "notes": f"Generated for {platform} about: {topic}"
    }

    # Update scheduling if provided
    if scheduled_date:
        try:
            # Parse the scheduled date
            if scheduled_time:
                dt = datetime.fromisoformat(f"{scheduled_date}T{scheduled_time}:00")
            else:
                dt = datetime.fromisoformat(f"{scheduled_date}T09:00:00")

            metadata["scheduling"]["scheduled_date"] = dt.isoformat() + "Z"
            metadata["scheduling"]["scheduled_time_local"] = dt.strftime("%H:%M %p CST")
            metadata["scheduling"]["posting_day"] = dt.strftime("%A")
            metadata["status"] = "scheduled"
        except Exception as e:
            print(f"⚠️  Could not parse scheduled date: {e}")

    return metadata


def save_content_with_metadata(
    topic: str,
    platform: str,
    content_type: str,
    target_audience: str,
    business_goal: str,
    social_post: str,
    scheduled_date: str = None,
    scheduled_time: str = None
) -> tuple:
    """
    Save social media content and metadata to content library.

    Returns:
        Tuple of (content_file_path, metadata_file_path)
    """
    # Get folder
    if scheduled_date and scheduled_time:
        # Move to scheduled folder instead of drafts
        folder = get_content_folder(platform, content_type)
        folder = folder.parent.parent / "scheduled"
        folder.mkdir(parents=True, exist_ok=True)
    else:
        folder = get_content_folder(platform, content_type)

    # Create filename
    date_str = scheduled_date if scheduled_date else datetime.now().strftime("%Y-%m-%d")
    topic_slug = create_slug(topic)

    if platform == "Instagram":
        prefix = "instagram-feed"
    elif platform == "Facebook":
        prefix = "facebook-post"
    elif platform == "LinkedIn":
        prefix = "linkedin-post"
    else:
        prefix = "social-post"

    filename_base = f"{date_str}_{prefix}_{topic_slug}"
    content_file = folder / f"{filename_base}.md"
    meta_file = folder / f"{filename_base}_meta.json"

    # Create metadata
    metadata = create_metadata(
        topic=topic,
        platform=platform,
        content_type=content_type,
        target_audience=target_audience,
        business_goal=business_goal,
        social_post=social_post,
        scheduled_date=scheduled_date,
        scheduled_time=scheduled_time
    )

    # Save content file
    with open(content_file, 'w') as f:
        f.write(f"# {topic}\n\n")
        f.write(f"**Platform**: {platform}\n")
        f.write(f"**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Status**: {metadata['status']}\n\n")
        f.write("---\n\n")
        f.write(social_post)

    # Save metadata file
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    return content_file, meta_file


def use_with_claude_api(
    prompt: str,
    topic: str,
    platform: str,
    content_type: str,
    target_audience: str,
    business_goal: str,
    scheduled_date: str = None,
    scheduled_time: str = None
):
    """
    Example of using the generated prompt with Claude API.

    Requires ANTHROPIC_API_KEY environment variable.
    """
    try:
        import anthropic
    except ImportError:
        print("⚠️  anthropic package not installed. Install with: pip install anthropic")
        return

    # Get API key from config or environment
    try:
        api_key = ensure_api_key()
    except ValueError as e:
        print(f"⚠️  {e}")
        return

    print("Calling Claude API...")
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=7000,
        temperature=0.6,  # Content creator uses 0.6 for creativity
        messages=[{"role": "user", "content": prompt}]
    )

    social_post = response.content[0].text

    print("\n" + "="*70)
    print("GENERATED SOCIAL MEDIA POST")
    print("="*70 + "\n")
    print(social_post)
    print("\n" + "="*70)

    # Save to content library
    print("\nSaving to content library...")
    content_file, meta_file = save_content_with_metadata(
        topic=topic,
        platform=platform,
        content_type=content_type,
        target_audience=target_audience,
        business_goal=business_goal,
        social_post=social_post,
        scheduled_date=scheduled_date,
        scheduled_time=scheduled_time
    )

    print(f"\n✓ Content saved:")
    print(f"  📄 {content_file.relative_to(Path(__file__).parent)}")
    print(f"  📋 {meta_file.relative_to(Path(__file__).parent)}")

    if scheduled_date:
        print(f"\n📅 Scheduled for: {scheduled_date} at {scheduled_time or '09:00'}")
    else:
        print(f"\n📝 Saved as draft - use manage_content_library.py to schedule")

    return social_post


def main():
    """Main function with example usage."""

    import argparse

    parser = argparse.ArgumentParser(
        description='Request social media posts from content creator agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Request Instagram post about anxiety
  python request_social_post.py --topic "5-4-3-2-1 grounding technique for anxiety" --platform Instagram

  # Request Facebook announcement
  python request_social_post.py --topic "New EMDR therapist joining practice" --platform Facebook --type announcement

  # Request LinkedIn thought-leadership
  python request_social_post.py --topic "The importance of mental health in the workplace" --platform LinkedIn

  # Use with Claude API (requires ANTHROPIC_API_KEY)
  python request_social_post.py --topic "Managing holiday stress" --use-api
        """
    )

    parser.add_argument(
        '--topic',
        required=True,
        help='Topic for the social media post'
    )

    parser.add_argument(
        '--platform',
        default='Instagram',
        choices=['Instagram', 'Facebook', 'LinkedIn'],
        help='Social media platform (default: Instagram)'
    )

    parser.add_argument(
        '--type',
        default='educational',
        choices=['educational', 'announcement', 'tip', 'testimonial'],
        help='Type of content (default: educational)'
    )

    parser.add_argument(
        '--audience',
        default='adults seeking therapy',
        help='Target audience (default: adults seeking therapy)'
    )

    parser.add_argument(
        '--goal',
        default='attract therapy clients',
        help='Business goal (default: attract therapy clients)'
    )

    parser.add_argument(
        '--use-api',
        action='store_true',
        help='Actually call Claude API to generate post (requires ANTHROPIC_API_KEY)'
    )

    parser.add_argument(
        '--save-prompt',
        help='Save generated prompt to file'
    )

    parser.add_argument(
        '--scheduled-date',
        help='Schedule for specific date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--scheduled-time',
        help='Schedule for specific time (HH:MM in 24-hour format)'
    )

    args = parser.parse_args()

    # Generate prompt
    prompt = request_social_post(
        topic=args.topic,
        platform=args.platform,
        content_type=args.type,
        target_audience=args.audience,
        business_goal=args.goal
    )

    if not prompt:
        return 1

    # Save prompt if requested
    if args.save_prompt:
        with open(args.save_prompt, 'w') as f:
            f.write(prompt)
        print(f"\n✓ Prompt saved to: {args.save_prompt}\n")

    # Use with Claude API if requested
    if args.use_api:
        use_with_claude_api(
            prompt=prompt,
            topic=args.topic,
            platform=args.platform,
            content_type=args.type,
            target_audience=args.audience,
            business_goal=args.goal,
            scheduled_date=args.scheduled_date,
            scheduled_time=args.scheduled_time
        )
    else:
        print("\n💡 To use this prompt:")
        print("   1. Copy the prompt above")
        print("   2. Use it with Claude API or Claude.ai")
        print("   3. Or run with --use-api flag to generate automatically")
        print("\n   Example:")
        print(f"   python {Path(__file__).name} --topic '{args.topic}' --use-api\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
