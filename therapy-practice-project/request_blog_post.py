#!/usr/bin/env python3
"""
Request Blog Posts from Content Creator Agent

Generate SEO-optimized blog posts for Squarespace with complete metadata.

Usage:
    python request_blog_post.py --topic "Understanding ADHD in Adults" --use-api
    python request_blog_post.py --topic "Anxiety Coping Strategies" --keywords "anxiety relief, coping with anxiety" --use-api
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


def request_blog_post(
    topic: str,
    keywords: str = None,
    word_count: int = 2000,
    target_audience: str = "adults seeking therapy",
    service_focus: str = None
):
    """
    Request a blog post from the content creator agent.

    Args:
        topic: Blog post topic/title
        keywords: Primary keywords for SEO (comma-separated)
        word_count: Target word count (default 2000, range 1500-3000)
        target_audience: Who this blog is for
        service_focus: Specific therapy service to highlight

    Returns:
        Generated prompt ready to use with Claude API
    """

    print("\n" + "="*70)
    print("BLOG POST REQUEST - SQUARESPACE READY")
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

    # Parse keywords if provided
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
        primary_keyword = keyword_list[0]
        secondary_keywords = keyword_list[1:5] if len(keyword_list) > 1 else []
    else:
        primary_keyword = topic
        secondary_keywords = []

    # Service focus
    if not service_focus:
        # Try to infer from topic
        if "anxiety" in topic.lower():
            service_focus = "anxiety-therapy"
        elif "adhd" in topic.lower():
            service_focus = "adhd-therapy"
        elif "couples" in topic.lower() or "relationship" in topic.lower():
            service_focus = "couples-therapy"
        elif "trauma" in topic.lower() or "ptsd" in topic.lower():
            service_focus = "trauma-therapy"
        else:
            service_focus = "general-therapy"

    # Create detailed blog task
    task = f"""
Create a comprehensive, SEO-optimized blog post for a therapy practice's Squarespace website.

**Blog Title**: {topic}

**Target Word Count**: {word_count} words (aim for {word_count-200} to {word_count+200})

**Primary Keyword**: {primary_keyword}
**Secondary Keywords**: {', '.join(secondary_keywords) if secondary_keywords else 'Generate appropriate secondary keywords'}

**Target Audience**: {target_audience}
**Service Focus**: {service_focus}

**SEO REQUIREMENTS:**

1. **Title Tag (50-60 characters)**
   - Include primary keyword
   - Compelling and click-worthy
   - Example: "Understanding ADHD in Adults: Signs & Treatment Options"

2. **Meta Description (150-160 characters)**
   - Include primary keyword
   - Clear value proposition
   - Call-to-action
   - Example: "Discover how ADHD affects adults, common signs to look for, and evidence-based treatment approaches. Schedule a consultation today."

3. **URL Slug**
   - Lowercase, hyphens between words
   - Include primary keyword
   - Keep under 60 characters
   - Example: "understanding-adhd-in-adults"

4. **Content Structure (REQUIRED)**

   **H1**: [Main Title - include primary keyword]

   **Introduction (150-200 words)**
   - Hook with relatable scenario or surprising statistic
   - State the problem clearly
   - Preview what readers will learn
   - Include primary keyword naturally

   **H2**: [First Major Section - include keyword variation]
   **H3**: [Subsection]
   [Content - 300-400 words]

   **H2**: [Second Major Section]
   **H3**: [Subsection]
   [Content - 300-400 words]

   **H2**: [Third Major Section - addressing common questions]
   **H3**: [Subsection]
   [Content - 300-400 words]

   **H2**: When to Seek Professional Help
   [Transition to therapy services - 200-300 words]
   - Signs that professional support would be beneficial
   - What therapy can offer
   - Types of treatment available

   **H2**: How [Practice Name] Can Help
   [Service-specific information - 150-200 words]
   - Your approach/specialization
   - What makes your practice unique
   - Evidence-based methods used

   **Conclusion (150-200 words)**
   - Recap main points
   - Empowering, hopeful message
   - Clear call-to-action

**5. SEO Best Practices:**
   - Use primary keyword in: Title, first paragraph, at least one H2, conclusion, meta description
   - Use secondary keywords naturally throughout
   - Include LSI keywords (related terms)
   - Keyword density: 1-2% (natural, not forced)
   - Use bullet points and numbered lists for readability
   - Keep paragraphs to 3-4 sentences max
   - Include transitional phrases

**6. Internal Linking (3-5 links):**
   - Link to relevant service pages
   - Link to other blog posts (if applicable)
   - Example: "Learn more about our [anxiety therapy services](/services/anxiety-therapy)"

**7. External Linking (2-3 authoritative sources):**
   - Research studies (NIMH, APA, peer-reviewed journals)
   - Government health resources
   - Reputable mental health organizations
   - Example: "[National Institute of Mental Health study on ADHD](https://www.nimh.nih.gov/adhd)"

**8. Call-to-Action:**
   - Multiple CTAs throughout (not just at end)
   - Clear next steps
   - Low-barrier options (free consultation, contact form)
   - Example: "Schedule a free 15-minute consultation to discuss your concerns"

**9. HIPAA Compliance:**
   - NO client stories with identifiable information
   - NO protected health information (PHI)
   - Use hypothetical examples or heavily anonymized cases
   - Include disclaimer if using case examples

**10. Readability:**
   - Write at 8th-10th grade reading level
   - Short sentences (15-20 words average)
   - Active voice
   - Conversational but professional tone
   - Define technical terms

**11. E-A-T (Expertise, Authoritativeness, Trustworthiness):**
   - Cite credible sources
   - Reference professional credentials
   - Link to evidence-based research
   - Provide accurate, up-to-date information

**OUTPUT FORMAT:**

Provide the blog post with:

1. **SEO Metadata Block** (for Squarespace):
```
Title: [50-60 char title]
Meta Description: [150-160 char description]
URL Slug: [lowercase-with-hyphens]
Primary Keyword: [keyword]
Secondary Keywords: [keyword1, keyword2, keyword3]
Focus Service: [service-name]
```

2. **Full Blog Post Content** (markdown formatted, ready to paste into Squarespace)

3. **Internal Links Suggestions**: List of suggested internal links to create

4. **External Sources Used**: List of external sources to link to

5. **Image Suggestions**:
   - Featured image idea
   - 2-3 in-content images with alt text

6. **Author Bio Suggestion**: Short bio to include at end

**IMPORTANT REMINDERS:**
- Evidence-based information only
- HIPAA compliant (no PHI)
- Person-first language
- Inclusive and culturally sensitive
- Professional yet warm tone
- Focus on hope and solutions
- Include crisis resources if topic warrants (988 Lifeline)
"""

    # Generate prompt
    print("Generating comprehensive blog post prompt...")
    prompt = engine.generate_prompt(
        context=content_creator.context,
        model=content_creator.model,
        tools=content_creator.tools,
        task=task
    )

    print(f"✓ Generated prompt ({len(prompt):,} characters)\n")

    # Display summary
    print("="*70)
    print("BLOG POST REQUEST SUMMARY")
    print("="*70)
    print(f"Topic:              {topic}")
    print(f"Target Word Count:  {word_count} words")
    print(f"Primary Keyword:    {primary_keyword}")
    if secondary_keywords:
        print(f"Secondary Keywords: {', '.join(secondary_keywords)}")
    print(f"Target Audience:    {target_audience}")
    print(f"Service Focus:      {service_focus}")
    print(f"Prompt Length:      {len(prompt):,} characters")
    print("="*70 + "\n")

    return prompt


def create_slug(text: str) -> str:
    """Create URL-friendly slug from text."""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:60]


def create_blog_metadata(
    topic: str,
    keywords: str,
    word_count: int,
    target_audience: str,
    service_focus: str,
    blog_content: str = None,
    scheduled_date: str = None
) -> Dict:
    """Create metadata structure for blog post."""

    content_id = str(uuid.uuid4())[:8]

    # Parse keywords
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
        primary_keyword = keyword_list[0]
        secondary_keywords = keyword_list[1:] if len(keyword_list) > 1 else []
    else:
        primary_keyword = topic
        secondary_keywords = []

    # Calculate actual word count if content provided
    actual_word_count = len(blog_content.split()) if blog_content else 0

    metadata = {
        "content_id": content_id,
        "content_type": "blog",
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
            "timezone": "America/Chicago",
            "publish_immediately": False
        },

        "content_details": {
            "word_count": actual_word_count,
            "target_word_count": word_count,
            "reading_time_minutes": max(1, actual_word_count // 200),
            "platform": "Squarespace Blog",
            "format": "long-form-blog",
            "target_audience": target_audience
        },

        "seo": {
            "primary_keyword": primary_keyword,
            "secondary_keywords": secondary_keywords,
            "meta_description": "",
            "url_slug": create_slug(topic),
            "title_tag": "",
            "focus_keyphrase_density": 0,
            "internal_links": [],
            "external_links": [],
            "image_alt_texts": []
        },

        "business_context": {
            "business_goal": "attract_therapy_clients",
            "service_promoted": service_focus,
            "target_conversion": "consultation_booking",
            "campaign": None,
            "content_cluster": None
        },

        "performance": {
            "published_date": None,
            "published_url": None,
            "page_views": 0,
            "unique_visitors": 0,
            "avg_time_on_page": 0,
            "bounce_rate": 0,
            "engagement": {
                "comments": 0,
                "shares": 0,
                "likes": 0
            },
            "conversions": {
                "form_submissions": 0,
                "phone_calls": 0,
                "inquiries_generated": 0,
                "bookings_attributed": 0
            },
            "seo_performance": {
                "organic_traffic": 0,
                "keyword_rankings": {},
                "backlinks": 0,
                "domain_authority_impact": 0
            }
        },

        "compliance": {
            "hipaa_compliant": True,
            "phi_check": "pending",
            "ethical_review": "pending",
            "crisis_resources_included": False,
            "sources_cited": []
        },

        "squarespace": {
            "category": "Mental Health",
            "tags": [primary_keyword] + secondary_keywords[:3],
            "featured_image_needed": True,
            "excerpt": "",
            "author": "Practice Team"
        },

        "version_history": [
            {
                "version": 1,
                "date": datetime.now().isoformat(),
                "changes": "Initial creation",
                "modified_by": "therapy-practice-content-creator"
            }
        ],

        "notes": f"Blog post for Squarespace website. Target: {word_count} words. Focus: {service_focus}"
    }

    if scheduled_date:
        try:
            dt = datetime.fromisoformat(f"{scheduled_date}T09:00:00")
            metadata["scheduling"]["scheduled_date"] = dt.isoformat() + "Z"
            metadata["scheduling"]["posting_day"] = dt.strftime("%A")
            metadata["status"] = "scheduled"
        except:
            pass

    return metadata


def save_blog_post(
    topic: str,
    keywords: str,
    word_count: int,
    target_audience: str,
    service_focus: str,
    blog_content: str,
    scheduled_date: str = None
) -> Tuple:
    """Save blog post and metadata to content library."""

    # Determine folder
    library_path = Path(__file__).parent / "social-media-content"

    if scheduled_date:
        folder = library_path / "blogs" / "scheduled"
    else:
        folder = library_path / "blogs" / "drafts"

    folder.mkdir(parents=True, exist_ok=True)

    # Create filename
    date_str = scheduled_date if scheduled_date else datetime.now().strftime("%Y-%m-%d")
    topic_slug = create_slug(topic)

    filename_base = f"{date_str}_blog_{topic_slug}"
    content_file = folder / f"{filename_base}.md"
    meta_file = folder / f"{filename_base}_meta.json"

    # Create metadata
    metadata = create_blog_metadata(
        topic=topic,
        keywords=keywords,
        word_count=word_count,
        target_audience=target_audience,
        service_focus=service_focus,
        blog_content=blog_content,
        scheduled_date=scheduled_date
    )

    # Save content file
    with open(content_file, 'w') as f:
        f.write(f"# {topic}\n\n")
        f.write(f"**Platform**: Squarespace Blog\n")
        f.write(f"**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Status**: {metadata['status']}\n")
        f.write(f"**Word Count**: {metadata['content_details']['word_count']} words\n")
        f.write(f"**Reading Time**: ~{metadata['content_details']['reading_time_minutes']} minutes\n\n")
        f.write("---\n\n")
        f.write(blog_content)

    # Save metadata file
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    return content_file, meta_file


def use_with_claude_api(
    prompt: str,
    topic: str,
    keywords: str,
    word_count: int,
    target_audience: str,
    service_focus: str,
    scheduled_date: str = None
):
    """Generate blog post using Claude API."""

    try:
        import anthropic
    except ImportError:
        print("⚠️  anthropic package not installed. Install with: pip install anthropic")
        return

    # Get API key
    try:
        api_key = ensure_api_key()
    except ValueError as e:
        print(f"⚠️  {e}")
        return

    print("Calling Claude API to generate blog post...")
    print("(This may take 30-60 seconds for long-form content)\n")

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,  # More tokens for long-form blog content
        temperature=0.7,  # Slightly higher for creative blog writing
        messages=[{"role": "user", "content": prompt}]
    )

    blog_content = response.content[0].text

    print("\n" + "="*70)
    print("GENERATED BLOG POST")
    print("="*70 + "\n")
    print(blog_content[:500] + "...\n")
    print(f"[Full blog post: {len(blog_content.split())} words]")
    print("="*70)

    # Save to content library
    print("\nSaving to content library...")
    content_file, meta_file = save_blog_post(
        topic=topic,
        keywords=keywords,
        word_count=word_count,
        target_audience=target_audience,
        service_focus=service_focus,
        blog_content=blog_content,
        scheduled_date=scheduled_date
    )

    print(f"\n✓ Blog post saved:")
    print(f"  📄 {content_file.relative_to(Path(__file__).parent)}")
    print(f"  📋 {meta_file.relative_to(Path(__file__).parent)}")

    if scheduled_date:
        print(f"\n📅 Scheduled for publishing: {scheduled_date}")
    else:
        print(f"\n📝 Saved as draft")
        print(f"   Review and edit before publishing to Squarespace")

    print(f"\n💡 Next steps:")
    print(f"   1. Review the blog post")
    print(f"   2. Copy SEO metadata to Squarespace")
    print(f"   3. Paste content into Squarespace blog editor")
    print(f"   4. Add images with suggested alt text")
    print(f"   5. Publish!")

    return blog_content


def main():
    """Main CLI interface."""

    import argparse

    parser = argparse.ArgumentParser(
        description='Generate SEO-optimized blog posts for Squarespace',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Basic blog post
  python request_blog_post.py \\
    --topic "Understanding ADHD in Adults" \\
    --use-api

  # With specific keywords
  python request_blog_post.py \\
    --topic "10 Anxiety Coping Strategies That Actually Work" \\
    --keywords "anxiety coping, anxiety relief, managing anxiety" \\
    --use-api

  # Custom word count
  python request_blog_post.py \\
    --topic "Complete Guide to Couples Therapy" \\
    --word-count 2500 \\
    --use-api

  # Schedule for future publishing
  python request_blog_post.py \\
    --topic "Trauma Recovery: A Therapist's Guide" \\
    --keywords "trauma therapy, ptsd treatment, trauma recovery" \\
    --scheduled-date "2025-11-15" \\
    --use-api
        """
    )

    parser.add_argument(
        '--topic',
        required=True,
        help='Blog post topic/title'
    )

    parser.add_argument(
        '--keywords',
        help='Primary keywords for SEO (comma-separated)'
    )

    parser.add_argument(
        '--word-count',
        type=int,
        default=2000,
        help='Target word count (default: 2000, range: 1500-3000)'
    )

    parser.add_argument(
        '--audience',
        default='adults seeking therapy',
        help='Target audience (default: adults seeking therapy)'
    )

    parser.add_argument(
        '--service',
        help='Specific therapy service to focus on (e.g., anxiety-therapy, couples-therapy)'
    )

    parser.add_argument(
        '--scheduled-date',
        help='Schedule for specific date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--use-api',
        action='store_true',
        help='Generate content with Claude API'
    )

    parser.add_argument(
        '--save-prompt',
        help='Save generated prompt to file'
    )

    args = parser.parse_args()

    # Validate word count
    if args.word_count < 1500 or args.word_count > 3000:
        print("⚠️  Warning: Word count should be between 1500-3000 for optimal SEO")
        print(f"   You specified: {args.word_count}")

    # Generate prompt
    prompt = request_blog_post(
        topic=args.topic,
        keywords=args.keywords,
        word_count=args.word_count,
        target_audience=args.audience,
        service_focus=args.service
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
            keywords=args.keywords or args.topic,
            word_count=args.word_count,
            target_audience=args.audience,
            service_focus=args.service or "general-therapy",
            scheduled_date=args.scheduled_date
        )
    else:
        print("\n💡 To generate the blog post:")
        print("   Add --use-api flag to generate with Claude API")
        print("\n   Example:")
        print(f"   python {Path(__file__).name} --topic '{args.topic}' --use-api\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
