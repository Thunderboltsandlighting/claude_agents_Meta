# Content Creation System v2.0 - Product Requirements Document

## Document Information

**Version:** 2.0
**Date:** October 28, 2025
**Status:** Production Ready
**Owner:** [Your Name]
**Reviewers:** [Your Name]

---

## Executive Summary

Interactive weekly content generation system that produces SEO-optimized, HIPAA-compliant content for therapy practice digital marketing. Replaces manual content creation with reproducible, checklist-driven process.

**Key Improvement Over v1.0:** Added interactivity, observance awareness, blog PRD v2.2 compliance, and automatic weekly summary generation.

---

## Problem Statement

**Current Pain Points:**
- Manual content creation takes 3-4 hours per week
- Inconsistent posting schedule
- Missing mental health awareness opportunities
- No systematic content organization
- Difficult to track what content exists
- Hard to batch schedule content
- No SEO optimization strategy

**Impact:**
- Lost marketing opportunities
- Competitor advantage in local search
- Inefficient use of founder time
- Inconsistent brand presence

---

## Solution Overview

**Automated Content Creation System** that:
1. Generates 8 social posts + 1 blog in <10 minutes
2. Tracks 60+ mental health observances automatically
3. Creates SEO-optimized blog posts (PRD v2.2 compliant)
4. Auto-generates master checklist for batch scheduling
5. Provides reproducible workflow for team execution

---

## User Stories

### US1: Weekly Content Generation
**As a** therapy practice founder
**I want to** generate a full week of content in one session
**So that** I can batch schedule everything and save time

**Acceptance Criteria:**
- [ ] System generates 8 social posts + 1 blog
- [ ] Execution time <10 minutes
- [ ] All content HIPAA compliant
- [ ] Content saved in organized folders
- [ ] Master summary file auto-generated

### US2: Observance Awareness
**As a** content creator
**I want to** automatically be notified of upcoming mental health observances
**So that** I never miss timely marketing opportunities

**Acceptance Criteria:**
- [ ] System tracks 60+ observances
- [ ] Forecasts 14 days ahead
- [ ] Suggests observance-related content
- [ ] Allows choice to use or skip observance
- [ ] Mixes observance content (40-60%) with regular content

### US3: SEO-Optimized Blogs
**As a** practice owner
**I want** blog posts optimized for Google and AI search
**So that** potential clients can find my practice online

**Acceptance Criteria:**
- [ ] Question-based H1/H2 headings
- [ ] Answer-first snippets
- [ ] FAQ section (5 Q&As)
- [ ] Schema markup (BlogPosting + FAQPage)
- [ ] Local SEO keywords (Hendersonville NC)
- [ ] 2000-3000 words

### US4: Batch Scheduling Workflow
**As a** founder with limited time
**I want** one master checklist showing all content for the week
**So that** I can review, create images, and schedule everything in one session

**Acceptance Criteria:**
- [ ] Weekly content summary auto-generated
- [ ] Contains all file paths
- [ ] Shows content previews
- [ ] Lists image requirements
- [ ] Includes scheduling checklist
- [ ] Shows hashtags for each post

### US5: Team Handoff Ready
**As a** systems-first founder
**I want** documentation that my team can execute without guessing
**So that** I can delegate content creation in the future

**Acceptance Criteria:**
- [ ] Step-by-step checklists exist
- [ ] Commands are copy/paste ready
- [ ] Success validation is clear
- [ ] No decision-making required
- [ ] Training time <30 minutes

---

## Functional Requirements

### FR1: Interactive Theme Selection
**Priority:** P0 (Must Have)

**Description:** User selects weekly content theme through interactive prompts.

**Modes:**
1. **Random Suggestions:** AI picks from service areas
2. **Observance-Based:** Focus on mental health awareness days/weeks/months
3. **Custom Theme:** User provides specific topic

**Acceptance Criteria:**
- [ ] User sees 3 mode options clearly
- [ ] Random mode shows 5 theme suggestions at a time
- [ ] User can regenerate for more options
- [ ] User can input custom theme at any point
- [ ] System validates theme is not empty
- [ ] System stores selected theme for content generation

**Test Data:**
```
Input: Mode 2 (Observance-Based)
Expected: Shows upcoming November observances
Action: User selects "National Family Caregivers Month"
Expected: Theme = "National Family Caregivers Month - Caregiving Support"
```

---

### FR2: Interactive Style Selection
**Priority:** P0 (Must Have)

**Description:** User customizes content style through guided questions.

**Options:**
1. **Tone:** Professional / Warm & Empathetic / Educational / Personal
2. **Social Length:** 150 / 200 / 250 words
3. **Audience:** General / Parents / Couples / Teens / Adults
4. **Blog Focus:** Comprehensive / Practical / Seeking Help / Local Resources

**Acceptance Criteria:**
- [ ] Each question shows clear options with recommendations
- [ ] System validates input (only accepts valid choices)
- [ ] System displays confirmation of selections
- [ ] Style applies to all 9 pieces of content
- [ ] System uses appropriate prompt engineering for each style

**Test Data:**
```
Tone: 2 (Warm & Empathetic)
Length: 2 (200 words)
Audience: 5 (Adults seeking individual therapy)
Blog Focus: 1 (Comprehensive)

Expected: Content generated with warm, empathetic tone at 200 words
```

---

### FR3: Social Media Content Generation
**Priority:** P0 (Must Have)

**Description:** Generate 8 social media posts distributed across 3 platforms.

**Distribution:**
- Instagram: 4 posts (Mon, Tue, Wed, Thu)
- Facebook: 2 posts (Tue, Thu)
- LinkedIn: 2 posts (Mon, Wed)

**Content Requirements:**
- Length: Based on user selection (150/200/250 words)
- Hashtags: 5-8 relevant, mix of popular + niche
- Visual suggestions: 3 options per post
- Engagement tips: Platform-specific
- HIPAA compliance: No PHI, no diagnosis via social media

**Acceptance Criteria:**
- [ ] Generates exactly 8 posts
- [ ] Posts distributed correctly across platforms
- [ ] Each post includes caption, hashtags, visual suggestions
- [ ] Content aligns with selected theme
- [ ] Tone matches user selection
- [ ] No duplicate content across posts
- [ ] Files saved in correct platform folders
- [ ] Metadata JSON created for each post
- [ ] Filenames include date for organization

**Test Data:**
```
Theme: "Anxiety and Sleep Problems"
Expected Output:
- instagram/feed-posts/scheduled/quick-tips-anxiety-sleep-2025-11-18-abc123.md
- facebook/posts/scheduled/common-myths-anxiety-sleep-2025-11-19-def456.md
... (8 total)
```

---

### FR4: Blog Post Generation (PRD v2.2 Compliance)
**Priority:** P0 (Must Have)

**Description:** Generate comprehensive blog post with all required sections.

**Required Sections:**
1. **Blog Content** (2000-3000 words)
   - Question-based H1 title
   - Answer-first snippets (2-3 sentences at top of each section)
   - Question-based H2 headings (5-7 sections)
   - FAQ section (5 Q&As)
   - Conclusion with CTA
   - References with professional insights

2. **Schema Markup**
   - BlogPosting schema JSON
   - FAQPage schema JSON
   - Ready for JSONKeeper.com

3. **Social Media Package**
   - Caption Variant 1: Educational
   - Caption Variant 2: Empathetic
   - Caption Variant 3: Call-to-Action
   - Each with hashtags and posting suggestions

4. **Instagram Carousel**
   - 10 slide prompts with copy
   - Carousel caption with hashtags

5. **SEO Metadata**
   - SEO title (60 chars)
   - Meta description (155 chars)
   - URL slug
   - Primary + semantic keywords
   - Categories, tags
   - Internal/external link suggestions
   - Featured image alt text

**Acceptance Criteria:**
- [ ] Blog file named with theme (not generic "blog-post.md")
- [ ] Word count 2000-3000
- [ ] All 5 sections present
- [ ] Question-based headings throughout
- [ ] Answer-first snippets at top of sections
- [ ] FAQ has minimum 5 Q&As
- [ ] Schema markup valid JSON
- [ ] Local SEO keywords included (Hendersonville NC)
- [ ] HIPAA compliant (no diagnosis in blog)
- [ ] E-E-A-T demonstrated (professional insights)
- [ ] File saved in blog-posts/drafts/ with descriptive folder name

**Test Data:**
```
Theme: "Anxiety and Sleep Problems"
Expected Files:
- blog-posts/drafts/anxiety-and-sleep-problems-xyz789/
  ├── anxiety-and-sleep-problems.md  (2500 words, all 5 sections)
  └── README.md  (publishing instructions)

Validation:
- Contains "## Section 1: COMPLETE BLOG POST CONTENT"
- Contains "## Section 2: SCHEMA MARKUP TEMPLATES"
- Contains "## Section 3: SOCIAL MEDIA CONTENT PACKAGE"
- Contains "## Section 4: INSTAGRAM CAROUSEL PROMPTS"
- Contains "## Section 5: SEO METADATA"
```

---

### FR5: Weekly Content Summary Generation
**Priority:** P0 (Must Have)

**Description:** Auto-generate master checklist file after content creation.

**Location:** `weekly-batches/YYYY-week-XX/WEEK_XX_CONTENT_SUMMARY.md`

**Required Sections:**
1. **Header** - Theme, date, total pieces, status checkboxes
2. **Checklist** - Review, images, scheduling tasks
3. **Social Posts** - Grouped by platform with:
   - File path
   - Topic
   - Preview (first 100 chars)
   - Hashtags (first 5)
   - Image requirements
   - Scheduled checkbox
4. **Blog Post** - Files list, publishing checklist
5. **Image Requirements** - Total count, breakdown by platform
6. **Quick File Access** - Commands to open folders
7. **Notes Section** - For tracking performance

**Acceptance Criteria:**
- [ ] File created automatically after content generation
- [ ] Named WEEK_XX_CONTENT_SUMMARY.md
- [ ] Contains all 7 required sections
- [ ] File paths are correct and relative
- [ ] Previews extracted from actual content
- [ ] Hashtags extracted from actual content
- [ ] Checkboxes are Markdown format (- [ ])
- [ ] Image count accurate
- [ ] Commands are copy/paste ready

**Test Data:**
```
Week: 2025-11-18 (Week 47)
Expected File: weekly-batches/2025-week-47/WEEK_47_CONTENT_SUMMARY.md

Validation:
- File exists
- Contains "# Week 47 Content Summary"
- Lists 8 social posts (4 Instagram, 2 Facebook, 2 LinkedIn)
- Lists 1 blog post
- Shows "Total Images Needed: 9"
- Contains executable bash commands
```

---

### FR6: Observance Awareness System
**Priority:** P1 (Should Have)

**Description:** Track and forecast mental health awareness days/weeks/months.

**Data Source:** `mental_health_observances.json`

**Tracked Observances:** 60+
- Mental Health Month (May)
- Suicide Prevention Month (September)
- ADHD Awareness Month (October)
- And 57+ more...

**Forecast Window:** 14 days ahead

**Integration:**
- Shows upcoming observances during theme selection
- Suggests observance-related content ideas
- Mixes 40-60% observance content with regular content

**Acceptance Criteria:**
- [ ] Observances loaded from JSON file
- [ ] System looks ahead 14 days from week start
- [ ] Displays top 5 upcoming observances
- [ ] Provides content ideas for each observance
- [ ] User can choose observance-based mode
- [ ] User can skip observance if desired
- [ ] Observance posts marked in summary file

**Test Data:**
```
Week: 2025-11-04 (Week 45)
Expected Observances:
- National Family Caregivers Month (Nov 1-30)
- Native American Heritage Month (Nov 1-30)
- Transgender Awareness Week (Nov 13-19)
- Transgender Day of Remembrance (Nov 20)
- Survivors of Suicide Loss Day (Nov 23)
```

---

### FR7: Content Deduplication
**Priority:** P1 (Should Have)

**Description:** Prevent suggesting topics that have already been created.

**Method:**
- Scan all `*_meta.json` files in content library
- Extract titles and keywords
- Check against existing topics before suggesting
- Track topics used in current batch

**Acceptance Criteria:**
- [ ] System scans all existing metadata files
- [ ] Extracts titles to lowercase
- [ ] Suggested topics not in existing set
- [ ] Topics used in current batch not repeated
- [ ] System reports count of existing topics found

**Test Data:**
```
Existing Topics: 30 (from previous weeks)
New Suggestions: Should not include any of the 30 existing topics
```

---

## Non-Functional Requirements

### NFR1: Performance
- **Content Generation:** <10 minutes for 9 pieces
- **Summary Generation:** <5 seconds
- **File Operations:** <2 seconds per file

### NFR2: Reliability
- **Error Rate:** <5%
- **API Success Rate:** >95%
- **File Save Success:** 100%

### NFR3: Usability
- **Team Training Time:** <30 minutes
- **Command Complexity:** Single command execution
- **Decision Points:** <10 per session
- **Documentation Clarity:** Executable by non-technical user

### NFR4: Maintainability
- **Code Documentation:** Docstrings for all functions
- **Version Control:** Git with meaningful commits
- **Change Tracking:** CHANGELOG.md updated
- **Test Coverage:** Acceptance tests documented

### NFR5: Security
- **API Key Storage:** Environment variables only
- **HIPAA Compliance:** No PHI in any content
- **Data Privacy:** No client information referenced

---

## Dependencies

### Technical Dependencies
- Python 3.10 or higher
- Anthropic API access (Claude Sonnet 4.5)
- API credits: ~500 per week
- Git/GitHub for version control

### External Dependencies
- Anthropic API uptime (>99%)
- Internet connection for API calls
- File system access for content storage

### Human Dependencies
- User available for 10-minute weekly session
- User has API key configured
- User understands basic terminal commands

---

## Success Metrics

### Adoption Metrics
- [ ] System used for 4 consecutive weeks
- [ ] <3 support questions per week
- [ ] User can execute without documentation after week 2

### Performance Metrics
- [ ] Content generation time <10 minutes
- [ ] Zero HIPAA violations
- [ ] 100% content created successfully
- [ ] Summary file generated 100% of time

### Quality Metrics
- [ ] Blog posts meet PRD v2.2 (100%)
- [ ] Social posts have proper hashtags (100%)
- [ ] All content has visual suggestions (100%)
- [ ] SEO metadata present in all blogs (100%)

### Business Impact (Future Tracking)
- Website traffic from blog posts
- Social media engagement rate
- Lead generation from content
- Local search ranking improvements

---

## Test Scenarios

### Test Scenario 1: Happy Path
**Objective:** Validate complete workflow executes successfully

**Steps:**
1. Run: `python create_weekly_batch_v2.py --week 2025-11-18 --use-api --interactive --with-blog`
2. Select: Mode 2 (Observance)
3. Select: Theme 1 (First observance)
4. Select: Tone 2, Length 2, Audience 5, Blog Focus 1
5. Wait for completion

**Expected Result:**
- [x] 8 social posts created
- [x] 1 blog post created
- [x] 1 summary file created
- [x] Execution time <10 minutes
- [x] "BATCH CREATION COMPLETE" message shown
- [x] All files exist at specified paths

---

### Test Scenario 2: Custom Theme
**Objective:** Validate custom theme input works

**Steps:**
1. Run command with --interactive
2. Select: Mode 3 (Custom)
3. Enter: "Anxiety and Sleep Problems"
4. Complete style selection
5. Wait for completion

**Expected Result:**
- [x] System accepts custom theme
- [x] All content relates to anxiety and sleep
- [x] Theme appears in summary file
- [x] No errors during generation

---

### Test Scenario 3: Duplicate Prevention
**Objective:** Validate system doesn't suggest existing topics

**Steps:**
1. Create Week 47 content
2. Note topics created
3. Attempt to create Week 48 content
4. Review suggestions

**Expected Result:**
- [x] Week 48 suggestions different from Week 47
- [x] System reports finding existing topics
- [x] No duplicate topics suggested

---

### Test Scenario 4: Blog PRD Compliance
**Objective:** Validate blog meets all PRD v2.2 requirements

**Steps:**
1. Create weekly content with blog
2. Open blog markdown file
3. Check for all 5 sections
4. Validate each requirement

**Expected Result:**
- [x] Section 1: Blog content present (2000-3000 words)
- [x] Question-based H1/H2 headings
- [x] Answer-first snippets present
- [x] FAQ section with 5 Q&As
- [x] Section 2: Schema markup (BlogPosting + FAQPage)
- [x] Section 3: Social media package (3 variants)
- [x] Section 4: Carousel prompts (10 slides)
- [x] Section 5: SEO metadata (complete)

---

### Test Scenario 5: Summary File Accuracy
**Objective:** Validate summary file contains accurate information

**Steps:**
1. Create weekly content
2. Open WEEK_XX_CONTENT_SUMMARY.md
3. Verify each section
4. Check file paths
5. Try bash commands

**Expected Result:**
- [x] All 8 social posts listed
- [x] Blog post listed
- [x] File paths are correct
- [x] Previews extracted from actual content
- [x] Hashtags extracted from actual content
- [x] Image count accurate
- [x] Bash commands executable

---

## Risks & Mitigations

### Risk 1: API Rate Limits
**Probability:** Low
**Impact:** High
**Mitigation:** Monitor usage, implement retry logic, batch requests efficiently

### Risk 2: API Cost
**Probability:** Medium
**Impact:** Medium
**Mitigation:** ~500 credits per week ($5-10), acceptable for business value

### Risk 3: Content Quality Inconsistency
**Probability:** Medium
**Impact:** Medium
**Mitigation:** User reviews all content before publishing, can edit as needed

### Risk 4: HIPAA Violation
**Probability:** Very Low
**Impact:** Critical
**Mitigation:** Prompts explicitly forbid PHI, user reviews all content, no client info referenced

### Risk 5: File System Errors
**Probability:** Low
**Impact:** Medium
**Mitigation:** Error handling, validation, clear error messages

---

## Rollout Plan

### Week 1: Documentation & Testing
- [ ] Complete all Phase 1 documentation
- [ ] Test with Week 47 creation
- [ ] Validate against all acceptance criteria
- [ ] Fix any issues found

### Week 2: Production Use
- [ ] Use for actual Week 48 content creation
- [ ] Track execution time
- [ ] Note any friction points
- [ ] Gather feedback

### Week 3-4: Optimization
- [ ] Implement improvements based on feedback
- [ ] Update documentation
- [ ] Prepare for team handoff

### Week 5+: Team Delegation (Future)
- [ ] Train team member using checklist
- [ ] Monitor execution
- [ ] Provide support as needed

---

## Approval

**Created By:** [Your Name]
**Date:** October 28, 2025

**Approved By:** ________________
**Date:** ________________

**Version:** 2.0
**Status:** Ready for Implementation

---

## Related Documents

- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- [CHANGELOG.md](CHANGELOG.md)
- [TEAM_EXECUTION_CHECKLIST.md](TEAM_EXECUTION_CHECKLIST.md)
- [ACCEPTANCE_TEST.md](ACCEPTANCE_TEST.md)

---

**Last Updated:** October 28, 2025
