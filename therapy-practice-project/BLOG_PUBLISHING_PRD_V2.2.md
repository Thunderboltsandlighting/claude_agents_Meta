# Hendersonville Counseling Blog Publishing

## Document Overview
**Version:** 2.2  
**Last Updated:** October 27, 2025  
**Owner:** Hendersonville Counseling  
**Purpose:** Standardize blog publishing process to ensure consistency, SEO optimization, AI discoverability, social media engagement, and brand alignment (Squarespace Basic compatible)

This PRD defines the complete requirements for all blog posts created by the content creation agents.

**IMPORTANT:** All blog post generation must follow this PRD exactly.

---

## Key Requirements Summary

✅ Answer-first snippets at top of each section
✅ Question-based H2 headings
✅ FAQ section (3-5 Q&A pairs)
✅ Schema markup (BlogPosting + FAQPage via JSONKeeper)
✅ Social media content package (3 caption variants + carousel prompts)
✅ SEO metadata with semantic keywords
✅ Internal links (2-3) and external sources (2-3)
✅ E-E-A-T focus (Experience, Expertise, Authority, Trust)
✅ Professional tone with personal insights
✅ HIPAA compliant content

**See full PRD document for complete implementation details.**

---

## Implementation

### Agent Configuration

The **therapy-practice-content-creator** agent has been configured to follow PRD v2.2 standards:

**File:** [agents/therapy-practice-content-creator/config.yaml](agents/therapy-practice-content-creator/config.yaml)

**Configuration includes:**
- Format standard: Hendersonville Counseling PRD v2.2
- Core content requirements (answer-first snippets, question-based headings, FAQ sections)
- SEO optimization (semantic keywords, local SEO for Hendersonville NC)
- Schema markup templates (BlogPosting + FAQPage via JSONKeeper)
- Social media package generation (3 caption variants + 10-slide carousel)
- HIPAA compliance and E-E-A-T focus

### Blog Generation Script

**Script:** [create_squarespace_blog.py](create_squarespace_blog.py)

This script generates complete PRD v2.2 compliant blog posts with all required components.

**Usage:**
```bash
# Generate blog post with Claude API
python create_squarespace_blog.py \
  --topic "Understanding ADHD in Adults" \
  --keywords "ADHD in adults, adult ADHD symptoms, ADHD treatment" \
  --use-api

# See prompt only (no API call)
python create_squarespace_blog.py \
  --topic "Anxiety Coping Strategies" \
  --keywords "anxiety relief, coping strategies"
```

**Generated Package Includes:**
1. Complete blog post content (2000-3000 words)
2. Schema markup JSON templates (BlogPosting + FAQPage)
3. Social media package (3 caption variants)
4. Instagram carousel prompts (10 slides)
5. SEO metadata (title, description, URL slug, keywords)
6. Publishing checklist

**Output Location:** `blog-posts/drafts/[slug]/`

### Workflow

1. **Generate Blog Post:**
   ```bash
   python create_squarespace_blog.py --topic "Your Topic" --use-api
   ```

2. **Review Generated Content:**
   - Blog post markdown file
   - Schema JSON templates
   - Social media variants
   - Carousel prompts

3. **Create Schema JSONs:**
   - Copy BlogPosting schema to JSONKeeper.com
   - Copy FAQPage schema to JSONKeeper.com
   - Get hosted JSON URLs

4. **Publish to Squarespace:**
   - Copy blog content to Squarespace editor
   - Add SEO metadata (title, description, URL slug)
   - Add schema markup code (inject JSON-LD via Code Block)
   - Upload featured image
   - Publish or schedule

5. **Post Social Media Content:**
   - Use caption variants for different platforms
   - Create carousel graphics using carousel prompts
   - Schedule posts using best times from performance profile

### PRD Compliance Checklist

When creating blog posts, ensure all content includes:

- ✅ Question-based H1 title with primary keyword
- ✅ Answer-first snippet (2-3 sentences) at top
- ✅ Question-based H2 section headings
- ✅ FAQ section (5 Q&A pairs minimum)
- ✅ Professional insights demonstrating expertise
- ✅ Internal links (2-3 to service pages)
- ✅ External links (2-3 to credible sources)
- ✅ References section with professional context
- ✅ Schema markup templates (BlogPosting + FAQPage)
- ✅ Social media package (3 variants + carousel)
- ✅ SEO metadata (title, description, slug, keywords)
- ✅ Local SEO mentions (Hendersonville NC, Western NC)
- ✅ HIPAA compliant content
- ✅ Clear CTA for therapy consultations

---

## Related Documentation

- [How to Use Business Intelligence Agents](HOW_TO_USE_BUSINESS_AGENTS.md)
- [How to Use Social Media Agents](HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md)
- [Content Management System Guide](CONTENT_MANAGEMENT_SYSTEM.md)
- [Performance Learning System](PERFORMANCE_LEARNING_SYSTEM.md)

---

**Last Updated:** October 28, 2025
**Agent Configuration Updated:** October 28, 2025
**Implementation Status:** ✅ Complete
