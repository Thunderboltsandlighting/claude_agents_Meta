# Changelog

All notable changes to the Therapy Practice Content Creation System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-10-28

### Added - Interactive Content Creation System

#### Interactive Theme Selection (FR1)
- **Feature:** 3-mode theme selection system
  - Random Suggestions: AI picks from therapy service areas
  - Observance-Based: Focus on mental health awareness days
  - Custom Theme: User provides specific topic
- **Impact:** Eliminates blank page syndrome, ensures relevant content
- **Files Changed:** `create_weekly_batch_v2.py` - Added `interactive_theme_selection()` method

#### Interactive Style Selection (FR2)
- **Feature:** Customizable content parameters
  - Tone: Professional / Warm / Educational / Personal
  - Social Length: 150 / 200 / 250 words
  - Audience: General / Parents / Couples / Teens / Adults
  - Blog Focus: Comprehensive / Practical / Seeking Help / Local Resources
- **Impact:** Content matches practice voice and target audience
- **Files Changed:** `create_weekly_batch_v2.py` - Added `interactive_style_selection()` method

#### Observance Awareness System (FR6)
- **Feature:** Automatic mental health awareness day suggestions
  - 60+ tracked observances (days/weeks/months)
  - 14-day forecast ahead
  - Automatic content ideas for each observance
- **Impact:** Never miss relevant awareness days, timely content
- **Files Changed:**
  - `mental_health_observances.json` - 60+ observances database
  - `create_weekly_batch_v2.py` - Added `get_upcoming_observances()` method

#### Weekly Content Summary (FR5)
- **Feature:** Auto-generated master checklist for batch scheduling
  - All file paths with content previews
  - Extracted hashtags from actual content
  - Image requirements summary
  - Executable bash commands for quick access
  - Review/scheduling checklists
- **Impact:** Enables 1-session batch workflow, eliminates file hunting
- **Files Changed:** `create_weekly_batch_v2.py` - Added `generate_weekly_summary()` method
- **Output Location:** `weekly-batches/YYYY-week-XX/WEEK_XX_CONTENT_SUMMARY.md`

#### Content Deduplication (FR7)
- **Feature:** Automatic topic tracking to prevent repetition
  - Scans all existing `*_meta.json` files
  - Extracts previously used topics
  - Never suggests duplicate content
- **Impact:** Ensures content variety, prevents audience fatigue
- **Files Changed:** `create_weekly_batch_v2.py` - Added topic tracking logic

#### Blog PRD v2.2 Compliance (FR4)
- **Feature:** Complete blog post package generation
  - Blog content (2000-3000 words)
  - Schema markup (BlogPosting + FAQPage)
  - Social media package (3 caption variants)
  - Instagram carousel prompts (10 slides)
  - Complete SEO metadata
- **Impact:** SEO-optimized, AI-discoverable blog posts
- **Files Changed:**
  - `create_squarespace_blog.py` - Blog generation script
  - `BLOG_PUBLISHING_PRD_V2.2.md` - Blog standards document
  - `agents/therapy-practice-content-creator/config.yaml` - Agent configuration

### Changed - Major Improvements

#### Blog Filename Convention
- **Old Behavior:** All blogs named `blog-post.md`
- **New Behavior:** Blogs named with theme slug (e.g., `anxiety-coping-strategies.md`)
- **Impact:** Easy identification, better file organization
- **Files Changed:** `create_weekly_batch_v2.py` - Line ~280

#### Workflow Optimization
- **Old Assumption:** Daily posting workflow
- **New Design:** Batch scheduling workflow (1 weekly session)
- **Impact:** 10 minutes per week instead of daily effort
- **Files Changed:** All documentation updated to reflect batch workflow

#### Content Preview System
- **Old Behavior:** No content previews available
- **New Behavior:** First 100 chars + hashtags in weekly summary
- **Impact:** Review content without opening each file
- **Files Changed:** `create_weekly_batch_v2.py` - Added `extract_preview_and_hashtags()` method

### Fixed - Bug Fixes

#### Blog Discovery Issue
- **Issue:** Generic filenames made blogs hard to find
- **Fix:** Theme-based filenames with descriptive slugs
- **User Feedback:** "blog what named blog-post.. thats hard to find when Im sifting through all of this"

#### Organization Chaos
- **Issue:** Files scattered, no master checklist
- **Fix:** Weekly Content Summary auto-generated with all file paths
- **User Feedback:** "my autism is screaming at me that this isnt organized"

#### Missing Context
- **Issue:** Team can't execute without founder guidance
- **Fix:** Executable checklists, acceptance criteria, test data
- **User Feedback:** "give me a PRD with acceptance criteria, test data, and a clear 'what changed' changelog"

---

## [1.0.0] - 2025-10-01

### Initial Release

#### Core Features
- Basic content generation using Claude API
- Social media post creation (Instagram, Facebook, LinkedIn)
- Blog post creation
- Content library organization
- Metadata tracking
- Performance tracking system

#### File Structure
- `request_social_post.py` - Single post generation
- `create_squarespace_blog.py` - Blog generation
- `manage_content_library.py` - Content management
- `schedule_content.py` - Scheduling tools
- `weekly_checkin.py` - Performance tracking

#### Content Organization
- Platform-based folders (Instagram, Facebook, LinkedIn)
- Status-based subfolders (drafts, scheduled, published)
- JSON metadata for each piece

#### Limitations
- Manual theme selection required
- No observance awareness
- No master checklist
- Generic blog filenames
- No content deduplication
- No style customization

---

## [Unreleased] - Future Versions

### Planned for v2.1.0
- **Business Intelligence Integration**
  - ROI tracking per content piece
  - Performance analytics dashboard
  - A/B testing capabilities

- **Advanced Performance Learning**
  - AI-powered topic recommendations based on past performance
  - Optimal posting time refinement based on practice data
  - Content format optimization (carousel vs. single image)

- **Enhanced Collaboration**
  - Multi-user support
  - Approval workflows
  - Comment/revision system

### Planned for v3.0.0
- **Template Extraction System**
  - Generic business content templates
  - Industry-agnostic framework
  - Custom service area mapping

- **Multi-Practice Support**
  - Manage multiple therapy practices
  - Shared content library
  - Practice-specific customization

---

## Version History Summary

| Version | Release Date | Key Feature | Impact |
|---------|-------------|-------------|--------|
| 2.0.0   | 2025-10-28  | Interactive batch creation + Observance awareness | 10-min weekly workflow |
| 1.0.0   | 2025-10-01  | Basic content generation | Manual content creation |

---

## Migration Guide

### Upgrading from v1.0 to v2.0

#### Breaking Changes
None - v2.0 is fully backward compatible.

#### New Features Available
1. **Interactive Mode:** Run `python create_weekly_batch_v2.py` for guided content creation
2. **Weekly Summary:** Check `weekly-batches/YYYY-week-XX/WEEK_XX_CONTENT_SUMMARY.md` for master checklist
3. **Observance Awareness:** System suggests relevant awareness days automatically

#### Recommended Actions
1. Continue using existing content library structure
2. Adopt new weekly summary workflow for batch scheduling
3. Review `mental_health_observances.json` for content calendar planning

#### File Changes
- **New Files:**
  - `create_weekly_batch_v2.py`
  - `mental_health_observances.json`
  - `SYSTEM_OVERVIEW.md`
  - `PRD_v2.0.md`
  - `CHANGELOG.md`
  - `TEAM_EXECUTION_CHECKLIST.md`
  - `ACCEPTANCE_TEST.md`

- **Modified Files:**
  - `BLOG_PUBLISHING_PRD_V2.2.md` - Updated with agent configuration

- **Deprecated Files:**
  - None (v1.0 scripts still functional)

---

## Support

For questions or issues:
- Review `TEAM_EXECUTION_CHECKLIST.md` for step-by-step guidance
- Check `ACCEPTANCE_TEST.md` for validation procedures
- Consult `PRD_v2.0.md` for detailed requirements
- See `SYSTEM_OVERVIEW.md` for architecture

---

**Last Updated:** October 28, 2025
**Maintained By:** Therapy Practice Content Team
