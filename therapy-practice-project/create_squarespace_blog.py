#!/usr/bin/env python3
"""
Squarespace Blog Generator - PRD v2.2 Compliant

Generates complete blog posts following Hendersonville Counseling PRD v2.2:
- AI-optimized content with answer-first snippets
- FAQ sections for AI discovery
- Schema JSON templates (BlogPosting + FAQPage)
- 3 social media caption variants
- Instagram carousel prompts (10 slides)
- Complete SEO metadata
- E-E-A-T focused content

Usage:
    python create_squarespace_blog.py --topic "Understanding ADHD in Adults" --use-api
    python create_squarespace_blog.py --topic "Anxiety Coping Strategies" --keywords "anxiety relief, coping techniques, stress management" --use-api
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


def create_blog_prompt(
    topic: str,
    keywords: str = None,
    word_count: int = 2000,
    target_audience: str = "adults seeking therapy in Hendersonville NC",
    service_focus: str = None
):
    """Create comprehensive blog post prompt following PRD v2.2."""

    # Parse keywords
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
        primary_keyword = keyword_list[0]
        secondary_keywords = keyword_list[1:] if len(keyword_list) > 1 else []
    else:
        primary_keyword = topic
        secondary_keywords = []

    # Infer service focus if not provided
    if not service_focus:
        topic_lower = topic.lower()
        if "anxiety" in topic_lower or "worry" in topic_lower:
            service_focus = "anxiety-therapy"
        elif "adhd" in topic_lower or "attention" in topic_lower:
            service_focus = "adhd-therapy"
        elif "autism" in topic_lower or "neurodiver" in topic_lower:
            service_focus = "neurodiversity-affirming-therapy"
        elif "couples" in topic_lower or "relationship" in topic_lower or "marriage" in topic_lower:
            service_focus = "couples-therapy"
        elif "trauma" in topic_lower or "ptsd" in topic_lower:
            service_focus = "trauma-therapy"
        elif "depression" in topic_lower:
            service_focus = "depression-therapy"
        else:
            service_focus = "general-therapy"

    prompt = f"""
# COMPREHENSIVE BLOG POST GENERATION - PRD V2.2 COMPLIANT

You are creating a blog post for Hendersonville Counseling's Squarespace website that must follow their complete Blog Publishing PRD v2.2.

## Blog Post Requirements

**Topic:** {topic}
**Primary Keyword:** {primary_keyword}
**Secondary Keywords:** {', '.join(secondary_keywords) if secondary_keywords else 'Generate 5-8 appropriate semantic/long-tail keywords'}
**Target Word Count:** {word_count} words (range: {word_count-200} to {word_count+200})
**Target Audience:** {target_audience}
**Service Focus:** {service_focus}
**Location:** Hendersonville, North Carolina (Western NC)
**Practice:** Hendersonville Counseling PLLC

---

## CRITICAL: YOUR OUTPUT MUST INCLUDE ALL 5 SECTIONS BELOW

---

## SECTION 1: COMPLETE BLOG POST CONTENT (Markdown Format)

Create the blog post following this EXACT structure:

### Title (H1)
- Question-based format preferred
- Include primary keyword
- 50-60 characters for SEO
- Example: "How Can Therapy Help You Manage Anxiety in Hendersonville NC?"

### Quick Answer (Answer-First Snippet)
**[2-3 sentence direct answer to the title question]**
- This appears immediately after the title
- Clear, concise, factual
- Include primary keyword naturally
- Example: "Therapy provides evidence-based tools like cognitive behavioral techniques, mindfulness practices, and professional guidance to help you identify stress triggers and develop healthy coping strategies. Working with a licensed therapist in Hendersonville offers personalized support tailored to your unique needs and Western NC lifestyle."

### Introduction (150-200 words)
- Hook: 2-3 sentences connecting emotionally with reader's lived experience
- Validation of their struggle
- Preview what they'll learn
- Naturally mention Hendersonville/Western NC context

### H2 Section 1: [Question-Based Heading]
**Quick Answer:** [1-2 sentence answer]

[Body content 300-400 words with:]
- Short paragraphs (2-4 lines each)
- Bullet points where appropriate
- Your professional insight/experience
- Evidence from credible sources

### H2 Section 2: [Question-Based Heading]
**Quick Answer:** [1-2 sentence answer]

[Body content 300-400 words with:]
- Actionable information
- Real-world examples (HIPAA-compliant, anonymized)
- Connection to local context when relevant

### H2 Section 3: [Question-Based Heading]
**Quick Answer:** [1-2 sentence answer]

[Body content 300-400 words]

### H2: When Should You Consider Seeking Therapy?
**Quick Answer:** [1-2 sentence answer about when to seek help]

[200-300 words covering:]
- Signs that professional support would be beneficial
- What therapy can offer
- Types of treatment available
- Gentle normalization of seeking help

### H2: How Hendersonville Counseling Can Help
[150-200 words covering:]
- Your evidence-based approach
- What makes your practice unique
- Services offered relevant to this topic
- Compassionate, professional tone
- Location mention (Hendersonville, serving Western NC)

### Conclusion (150-200 words)
- Recap main points (3-4 key takeaways)
- Empowering, hopeful message
- Clear, gentle call-to-action

### Frequently Asked Questions

**Q1: [Common question related to topic]**
A: [2-3 sentence answer]

**Q2: [Common question related to topic]**
A: [2-3 sentence answer]

**Q3: [Common question related to topic]**
A: [2-3 sentence answer]

**Q4: [Common question related to topic]**
A: [2-3 sentence answer]

**Q5: [Common question related to topic]**
A: [2-3 sentence answer]

### Next Steps
[Gentle CTA paragraph with:]
- Invitation to take action
- Link mention to appointment page
- Link to 2-3 related resources/pages

**Related Reading:**
- [Suggest internal link to related topic 1]
- [Suggest internal link to related topic 2]
- [Suggest internal link to service page]

### References
1. [Credible source 1 - APA, NIMH, NIH, university research]
2. [Credible source 2 - Medical/psychological authority]
3. [Credible source 3 - Government or academic institution]

**Professional Insight:** [1-2 sentences about your clinical experience with this topic - adds E-E-A-T credibility]

---

## SECTION 2: SCHEMA MARKUP TEMPLATES (JSON Format)

Provide TWO complete JSON schemas ready to paste into JSONKeeper.com:

### BlogPosting Schema JSON:
```json
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Exact blog title]",
  "description": "[Meta description]",
  "mainEntityOfPage": "https://www.hendersonvillecounseling.com/resources-blog/[url-slug]",
  "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
  "dateModified": "{datetime.now().strftime('%Y-%m-%d')}",
  "author": {{
    "@type": "Organization",
    "name": "Hendersonville Counseling PLLC"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Hendersonville Counseling",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://www.hendersonvillecounseling.com/path-to-logo.png"
    }},
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "120 Chadwick Square Ct Ste D",
      "addressLocality": "Hendersonville",
      "addressRegion": "NC",
      "postalCode": "28739",
      "addressCountry": "US"
    }}
  }},
  "image": [
    "https://www.hendersonvillecounseling.com/path-to-featured-image.jpg"
  ],
  "articleSection": ["[Category 1]", "[Category 2]"],
  "keywords": [
    "Hendersonville Counseling",
    "{primary_keyword}",
    [list all secondary keywords here],
    "Western North Carolina",
    "Hendersonville NC"
  ]
}}
```

### FAQPage Schema JSON:
```json
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "[Question 1 text]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Full answer 1 text]"
      }}
    }},
    {{
      "@type": "Question",
      "name": "[Question 2 text]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Full answer 2 text]"
      }}
    }},
    {{
      "@type": "Question",
      "name": "[Question 3 text]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Full answer 3 text]"
      }}
    }},
    {{
      "@type": "Question",
      "name": "[Question 4 text]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Full answer 4 text]"
      }}
    }},
    {{
      "@type": "Question",
      "name": "[Question 5 text]",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "[Full answer 5 text]"
      }}
    }}
  ]
}}
```

---

## SECTION 3: SOCIAL MEDIA CONTENT PACKAGE

Create THREE caption variants for Facebook/Instagram:

### Caption Variant 1: Educational
[Hook with surprising fact/statistic]

[2-3 sentences of valuable, shareable information]

📖 Read the full post: [link in bio]

#MentalHealth #HendersonvilleCounseling #WesternNC #[TopicHashtag] #[RelevantHashtag] #TherapyNC #MentalHealthAwareness

### Caption Variant 2: Empathetic
"[Relatable quote or feeling statement]"

[Validation sentence acknowledging the struggle]

[Hope statement about therapy/support being possible]

🌿 Read our latest post: [link in bio]

#MentalHealthMatters #Therapy #HendersonvilleNC #[TopicHashtag] #Healing #SelfAcceptance #Compassion

### Caption Variant 3: Call-to-Action
[Qualifying question targeting ideal client's pain point]?

You're not alone. [Recognition of their experience]

🌿 Learn how {service_focus} can help you [benefit].

📞 Request an appointment: Link in bio or call (828) 595-9880

#HendersonvilleCounseling #[ServiceHashtag] #TherapyWorks #MentalHealthNC #WesternNC

---

## SECTION 4: INSTAGRAM CAROUSEL PROMPTS (10 Slides)

Provide complete copy for a 10-slide Instagram carousel:

**Slide 1 (Hook):**
"[Bold, attention-grabbing statement or question] Swipe → to learn more"

**Slide 2:**
[Key point 1 - Keep to 15-20 words]

**Slide 3:**
[Key point 2 - Keep to 15-20 words]

**Slide 4:**
[Key point 3 - Keep to 15-20 words]

**Slide 5:**
[Key point 4 - Keep to 15-20 words]

**Slide 6:**
[Key point 5 - Keep to 15-20 words]

**Slide 7:**
[Additional insight or "What to do if..." - 15-20 words]

**Slide 8:**
[Therapy benefit or practical tip - 15-20 words]

**Slide 9 (CTA):**
"Ready to take the next step? Read the full article (link in bio) or book a consultation today"

**Slide 10 (Resources):**
"📍 Hendersonville Counseling
Western North Carolina
@hendersonvillecounseling
www.hendersonvillecounseling.com"

**Carousel Caption:**
[3-4 sentences introducing the carousel topic]
[Include emotional hook and value proposition]
[Link in bio mention]
[7-10 hashtags including #HendersonvilleCounseling #WesternNC #[TopicHashtags]]

---

## SECTION 5: SEO METADATA & PUBLISHING CHECKLIST

**SEO Title (50-60 characters):**
[Title with primary keyword + location]

**Meta Description (150-160 characters):**
[Answer-focused description with keyword, value prop, and CTA]

**URL Slug:**
/resources-blog/[lowercase-keyword-slug]

**Primary Keyword:**
{primary_keyword}

**Secondary/Semantic Keywords:**
[List 5-8 long-tail keyword variations including location-based]

**Categories (Choose 1-2):**
- Emotional Well-Being
- Benefits of Therapy
- Coping Strategies
- Relationships & Communication
- Mindfulness & Self-Care
- Mental Health Conditions
- Therapy Approaches

**Tags (List 5-8):**
[Include mix of core + long-tail tags with location]

**Featured Image Alt Text:**
"[Descriptive alt text with emotion/location/topic - under 125 characters]"

**Internal Links to Create:**
1. [Service page or related blog post 1]
2. [Service page or related blog post 2]
3. [Service page or related blog post 3]

**External Authoritative Sources:**
1. [Full citation for reference 1]
2. [Full citation for reference 2]
3. [Full citation for reference 3]

---

## CONTENT GUIDELINES (CRITICAL)

**Tone & Voice:**
- Warm, compassionate, professional
- Person-first language
- Inclusive and culturally sensitive
- Evidence-based but accessible (8th-10th grade reading level)
- Balance professional credibility with genuine empathy

**HIPAA Compliance:**
- NO client stories with identifiable information
- NO protected health information (PHI)
- Use hypothetical examples or heavily anonymized cases
- Include disclaimer if using case examples

**E-E-A-T Focus:**
- Experience: Add your personal professional insights
- Expertise: Cite credentials and evidence-based approaches
- Authority: Reference credible research
- Trustworthiness: Accurate, up-to-date, transparent information

**AI Optimization:**
- Answer-first snippets for featured snippet potential
- Question-based headings matching search queries
- Modular content chunks AI can extract
- FAQ section AI systems can use directly
- Semantic keyword variations throughout

**Local SEO:**
- Mention Hendersonville NC naturally in content
- Reference Western North Carolina context
- Include local practice information in conclusion
- Use location-based keywords in metadata

---

## OUTPUT FORMAT

Provide ALL 5 SECTIONS clearly labeled and complete:

1. **BLOG POST CONTENT** (Full markdown-formatted post ready to paste into Squarespace)
2. **SCHEMA TEMPLATES** (Both JSONs ready for JSONKeeper)
3. **SOCIAL MEDIA CAPTIONS** (All 3 variants with hashtags)
4. **CAROUSEL PROMPTS** (All 10 slides with carousel caption)
5. **SEO METADATA** (Complete checklist for Squarespace settings)

Make this comprehensive, following every requirement of the PRD v2.2.
"""

    return prompt


def request_squarespace_blog(
    topic: str,
    keywords: str = None,
    word_count: int = 2000,
    target_audience: str = "adults seeking therapy in Hendersonville NC",
    service_focus: str = None
):
    """Request Squarespace blog post from content creator agent."""

    print("\n" + "="*80)
    print("SQUARESPACE BLOG POST GENERATOR - PRD V2.2")
    print("="*80 + "\n")

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

    # Generate comprehensive prompt
    print("Generating PRD v2.2 compliant blog prompt...")
    blog_prompt = create_blog_prompt(
        topic=topic,
        keywords=keywords,
        word_count=word_count,
        target_audience=target_audience,
        service_focus=service_focus
    )

    # Generate final prompt through engine
    prompt = engine.generate_prompt(
        context=content_creator.context,
        model=content_creator.model,
        tools=content_creator.tools,
        task=blog_prompt
    )

    print(f"✓ Generated comprehensive prompt ({len(prompt):,} characters)\n")

    # Display summary
    print("="*80)
    print("BLOG POST GENERATION SUMMARY")
    print("="*80)
    print(f"Topic:              {topic}")
    print(f"Keywords:           {keywords or 'Will be generated'}")
    print(f"Target Word Count:  {word_count} words")
    print(f"Target Audience:    {target_audience}")
    print(f"Service Focus:      {service_focus or 'Will be inferred'}")
    print(f"\nIncludes:")
    print(f"  ✅ Answer-first snippets & question-based headings")
    print(f"  ✅ FAQ section (5 Q&As)")
    print(f"  ✅ Schema JSON templates (BlogPosting + FAQPage)")
    print(f"  ✅ 3 social media caption variants")
    print(f"  ✅ Instagram carousel prompts (10 slides)")
    print(f"  ✅ Complete SEO metadata")
    print(f"  ✅ E-E-A-T focus with professional insights")
    print(f"  ✅ HIPAA compliant content")
    print("="*80 + "\n")

    return prompt


def save_squarespace_blog_package(
    topic: str,
    keywords: str,
    full_output: str,
    scheduled_date: str = None
):
    """Save complete blog package to organized folder structure."""

    library_path = Path(__file__).parent / "social-media-content"

    # Determine folder
    if scheduled_date:
        folder = library_path / "blogs" / "scheduled"
    else:
        folder = library_path / "blogs" / "drafts"

    folder.mkdir(parents=True, exist_ok=True)

    # Create slug
    slug = re.sub(r'[^\w\s-]', '', topic.lower())
    slug = re.sub(r'[-\s]+', '-', slug)[:60]

    date_str = scheduled_date if scheduled_date else datetime.now().strftime("%Y-%m-%d")
    filename_base = f"{date_str}_squarespace-blog_{slug}"

    # Save complete package
    package_file = folder / f"{filename_base}_COMPLETE.md"
    with open(package_file, 'w') as f:
        f.write(f"# {topic}\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Format:** Squarespace Blog - PRD v2.2 Compliant\n")
        f.write(f"**Status:** {'Scheduled' if scheduled_date else 'Draft'}\n\n")
        f.write("="*80 + "\n\n")
        f.write(full_output)

    # Create metadata
    metadata = {
        "content_id": str(uuid.uuid4())[:8],
        "content_type": "squarespace-blog-prd-v2.2",
        "title": topic,
        "created_date": datetime.now().isoformat(),
        "status": "scheduled" if scheduled_date else "draft",
        "prd_version": "2.2",
        "includes": {
            "blog_content": True,
            "schema_jsons": True,
            "social_media_captions": 3,
            "carousel_prompts": True,
            "seo_metadata": True,
            "faq_section": True,
            "answer_first_snippets": True
        },
        "keywords": keywords,
        "scheduled_date": scheduled_date,
        "platform": "Squarespace",
        "practice": "Hendersonville Counseling"
    }

    meta_file = folder / f"{filename_base}_meta.json"
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    return package_file, meta_file


def use_with_claude_api(
    prompt: str,
    topic: str,
    keywords: str,
    scheduled_date: str = None
):
    """Generate blog with Claude API."""

    try:
        import anthropic
    except ImportError:
        print("⚠️  anthropic package not installed. Install with: pip install anthropic")
        return

    try:
        api_key = ensure_api_key()
    except ValueError as e:
        print(f"⚠️  {e}")
        return

    print("Calling Claude API to generate complete blog package...")
    print("(This will take 60-90 seconds for comprehensive content)\n")

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    full_output = response.content[0].text

    print("\n" + "="*80)
    print("✅ COMPLETE BLOG PACKAGE GENERATED")
    print("="*80)
    print(f"\nGenerated {len(full_output.split())} words")
    print(f"Preview: {full_output[:300]}...\n")

    # Save complete package
    print("Saving complete blog package...")
    package_file, meta_file = save_squarespace_blog_package(
        topic=topic,
        keywords=keywords or topic,
        full_output=full_output,
        scheduled_date=scheduled_date
    )

    print(f"\n✓ Complete package saved:")
    print(f"  📦 {package_file.relative_to(Path(__file__).parent)}")
    print(f"  📋 {meta_file.relative_to(Path(__file__).parent)}")

    print(f"\n📋 YOUR COMPLETE PACKAGE INCLUDES:")
    print(f"   1️⃣  Blog post content (PRD v2.2 format)")
    print(f"   2️⃣  Schema JSON templates (BlogPosting + FAQPage)")
    print(f"   3️⃣  3 social media caption variants")
    print(f"   4️⃣  Instagram carousel prompts (10 slides)")
    print(f"   5️⃣  Complete SEO metadata")

    print(f"\n💡 NEXT STEPS:")
    print(f"   1. Review the complete package file")
    print(f"   2. Copy blog content to Squarespace")
    print(f"   3. Create schemas on JSONKeeper.com")
    print(f"   4. Add schema links to blog post")
    print(f"   5. Use social media captions for promotion")
    print(f"   6. Create carousel in Canva with provided prompts")

    return full_output


def main():
    """Main CLI interface."""

    import argparse

    parser = argparse.ArgumentParser(
        description='Generate Squarespace blogs following PRD v2.2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Basic blog post
  python create_squarespace_blog.py \\
    --topic "Understanding ADHD in Adults" \\
    --use-api

  # With specific keywords
  python create_squarespace_blog.py \\
    --topic "How Therapy Helps Manage Anxiety" \\
    --keywords "anxiety therapy, anxiety treatment Hendersonville, managing anxiety, therapy for anxiety" \\
    --use-api

  # Schedule for publishing
  python create_squarespace_blog.py \\
    --topic "Benefits of Couples Therapy" \\
    --scheduled-date "2025-11-15" \\
    --use-api

  # Custom word count
  python create_squarespace_blog.py \\
    --topic "Complete Guide to Trauma Recovery" \\
    --keywords "trauma therapy, PTSD treatment, trauma recovery" \\
    --word-count 2500 \\
    --use-api
        """
    )

    parser.add_argument(
        '--topic',
        required=True,
        help='Blog post topic (question format preferred)'
    )

    parser.add_argument(
        '--keywords',
        help='Primary and secondary keywords (comma-separated)'
    )

    parser.add_argument(
        '--word-count',
        type=int,
        default=2000,
        help='Target word count (default: 2000)'
    )

    parser.add_argument(
        '--audience',
        default='adults seeking therapy in Hendersonville NC',
        help='Target audience'
    )

    parser.add_argument(
        '--service',
        help='Specific service focus (e.g., anxiety-therapy, couples-therapy)'
    )

    parser.add_argument(
        '--scheduled-date',
        help='Schedule for date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--use-api',
        action='store_true',
        help='Generate with Claude API'
    )

    args = parser.parse_args()

    # Generate prompt
    prompt = request_squarespace_blog(
        topic=args.topic,
        keywords=args.keywords,
        word_count=args.word_count,
        target_audience=args.audience,
        service_focus=args.service
    )

    if not prompt:
        return 1

    # Generate with API if requested
    if args.use_api:
        use_with_claude_api(
            prompt=prompt,
            topic=args.topic,
            keywords=args.keywords,
            scheduled_date=args.scheduled_date
        )
    else:
        print("\n💡 To generate the complete blog package:")
        print("   Add --use-api flag\n")
        print("   Example:")
        print(f"   python {Path(__file__).name} --topic '{args.topic}' --use-api\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
