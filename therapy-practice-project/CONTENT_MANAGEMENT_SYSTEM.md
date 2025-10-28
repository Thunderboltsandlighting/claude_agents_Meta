# Content Management System Documentation

## Overview

The Therapy Practice Content Management System provides complete organization, scheduling, and tracking for all social media and blog content created by your practice agents.

**Key Features:**
- Organized folder structure for all content types
- Comprehensive metadata tracking
- Automated scheduling with optimal posting times
- Performance metrics and analytics
- Content library browsing and search
- Integration with content creation agents

---

## System Architecture

```
therapy-practice-project/
├── social-media-content/           # All content stored here
│   ├── blogs/                      # Blog posts
│   ├── instagram/                  # Instagram content
│   ├── facebook/                   # Facebook content
│   ├── linkedin/                   # LinkedIn content
│   ├── weekly-batches/             # Weekly content batches
│   ├── campaigns/                  # Campaign-specific content
│   └── templates/                  # Content templates
│
├── initialize_content_library.py   # Setup: Create folder structure
├── request_social_post.py          # Create: Generate content with AI
├── manage_content_library.py       # Manage: Search, move, organize
├── schedule_content.py             # Schedule: Plan posting times
└── view_content.py                 # View: Browse and preview content
```

---

## Quick Start Guide

### 1. Initialize the Content Library

First time setup - creates all folders:

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
python initialize_content_library.py
```

**Output:**
- Creates 28 folders for organized content storage
- Creates README files for each folder
- Creates configuration files
- Creates example templates

### 2. Create Your First Social Media Post

```bash
python request_social_post.py \
  --topic "5-4-3-2-1 grounding technique for anxiety" \
  --platform Instagram \
  --use-api
```

**What happens:**
1. Loads content creator agent
2. Generates AI prompt with your requirements
3. Calls Claude API to create post
4. **Automatically saves to** `social-media-content/instagram/feed-posts/drafts/`
5. **Creates metadata file** with all tracking information

**Result:**
- `2025-10-27_instagram-feed_grounding-technique.md` (content)
- `2025-10-27_instagram-feed_grounding-technique_meta.json` (metadata)

### 3. Schedule the Post

```bash
python request_social_post.py \
  --topic "Weekend self-care tips" \
  --platform Instagram \
  --scheduled-date "2025-11-01" \
  --scheduled-time "09:00" \
  --use-api
```

**Result:**
- Post automatically saved to `scheduled/` folder (not `drafts/`)
- Metadata includes scheduling information
- Ready for publishing on the scheduled date

### 4. View Your Content

```bash
# View recent content
python view_content.py

# View specific post
python view_content.py --file "grounding-technique"

# View full content (not just preview)
python view_content.py --file "grounding-technique" --full
```

### 5. Manage Your Content Library

```bash
# List all scheduled posts
python manage_content_library.py --list scheduled

# Search for anxiety-related content
python manage_content_library.py --search "anxiety"

# View content calendar for November
python manage_content_library.py --calendar --month November --year 2025

# Move post to published after posting
python manage_content_library.py --publish "2025-10-27_instagram-feed_grounding-technique"
```

---

## Detailed Usage

### Creating Content

#### Instagram Posts

```bash
python request_social_post.py \
  --topic "Progressive muscle relaxation technique" \
  --platform Instagram \
  --type educational \
  --use-api
```

**Platform-specific requirements automatically applied:**
- Length: 150-250 words
- Hashtags: 5-10 relevant
- Visual content suggestion included
- Hook + education + CTA format

#### Facebook Posts

```bash
python request_social_post.py \
  --topic "New EMDR therapist joining our practice" \
  --platform Facebook \
  --type announcement \
  --use-api
```

**Facebook requirements:**
- Length: 100-250 words
- Conversational tone
- Encourages comments
- Optional hashtags (3-5)

#### LinkedIn Posts

```bash
python request_social_post.py \
  --topic "Mental health importance in workplace" \
  --platform LinkedIn \
  --type educational \
  --use-api
```

**LinkedIn requirements:**
- Length: 200-400 words
- Professional thought-leadership tone
- Professional hashtags (3-5)
- Industry-relevant content

---

### Content Scheduling

#### Create Weekly Schedule

```bash
python schedule_content.py --week 2025-11-04
```

**Output:**
```
CONTENT SCHEDULE - Week of 2025-11-04
================================================================================

Monday     2025-11-04
--------------------------------------------------------------------------------
  ○ 09:00 | Instagram  | Content needed
  ○ 08:00 | LinkedIn   | Content needed

Tuesday    2025-11-05
--------------------------------------------------------------------------------
  ○ 09:00 | Facebook   | Content needed
  ○ 09:00 | Instagram  | Content needed

...
```

**Automatically saved to:** `social-media-content/weekly-batches/2025-week-45/`

#### Create Schedule with Themes

```bash
python schedule_content.py --week 2025-11-04 \
  --theme "Monday:Anxiety Awareness" \
  --theme "Wednesday:Couples Therapy Tips" \
  --theme "Friday:Self-Care Weekend"
```

**Themes help:**
- Guide content creation
- Maintain consistency
- Align with campaigns

#### Find Next Available Slot

```bash
python schedule_content.py --next-slot Instagram
```

**Output:**
```
📅 Next available Instagram slot:
   Date: Tuesday, 2025-11-05
   Time: 09:00
   ✓ Optimal posting time
```

---

### Managing Content

#### List Content by Status

```bash
# All drafts
python manage_content_library.py --list draft

# All scheduled posts
python manage_content_library.py --list scheduled

# All published content
python manage_content_library.py --list published

# Everything
python manage_content_library.py --list all
```

#### Search Content

```bash
# Search by topic
python manage_content_library.py --search "anxiety"

# Search by keyword
python manage_content_library.py --search "couples therapy"

# Search by platform (searches metadata)
python manage_content_library.py --search "Instagram"
```

#### View Content Calendar

```bash
# Current month
python manage_content_library.py --calendar

# Specific month
python manage_content_library.py --calendar --month December --year 2025
```

**Calendar shows:**
- All scheduled posts by date
- Platform for each post
- Time slot for each post
- Filename for each post

#### Move Content Between Statuses

```bash
# Draft → Scheduled
python manage_content_library.py --schedule "2025-10-27_instagram-feed_topic"

# Scheduled → Published (after posting live)
python manage_content_library.py --publish "2025-10-27_instagram-feed_topic"
```

**Moving content:**
- Physically moves files to new folder
- Updates metadata status field
- Updates timestamps
- Preserves all metadata

#### Performance Reports

```bash
# All-time performance
python manage_content_library.py --performance-report

# Specific date range
python manage_content_library.py --performance-report \
  --date-range "2025-10-01:2025-10-31"
```

**Report includes:**
- Total posts published
- Total views and engagement
- Average performance metrics
- Breakdown by platform
- Breakdown by content type
- Conversion tracking

---

### Viewing Content

#### View Recent Content

```bash
# Show 10 most recent
python view_content.py

# Show 25 most recent
python view_content.py --recent 25
```

**Shows list with:**
- Title and status
- Platform
- Creation date
- Filename

#### View Specific Content

```bash
# By partial filename
python view_content.py --file "grounding-technique"

# Show full content
python view_content.py --file "grounding-technique" --full
```

**Displays:**
- Complete metadata
- Content details (word count, platform, audience)
- Scheduling information
- SEO information (for blogs)
- Social media details (hashtags, CTA)
- Business context
- Performance metrics (if published)
- Compliance status
- Full content or preview

---

## Metadata Schema

Every piece of content has a metadata JSON file tracking:

### Core Information
- `content_id`: Unique identifier
- `content_type`: Platform + format (e.g., "instagram-feed")
- `title`: Content title/topic
- `created_date`: When created
- `created_by_agent`: Which agent created it
- `status`: draft | scheduled | published | archived

### Scheduling
- `scheduled_date`: When to post (ISO format)
- `scheduled_time_local`: Local time for posting
- `posting_day`: Day of week
- `optimal_posting_time`: Whether time is optimal
- `timezone`: Timezone for scheduling

### Content Details
- `word_count`: Number of words
- `reading_time_minutes`: Estimated reading time
- `platform`: Primary platform
- `format`: Content format type
- `target_audience`: Who this is for

### Social Media (for social posts)
- `hashtags`: List of hashtags used
- `caption_length`: Character/word count
- `has_cta`: Whether includes call-to-action
- `visual_content_needed`: Visual requirements
- `accessibility`: Alt text and caption info

### SEO (for blogs)
- `primary_keyword`: Main keyword
- `secondary_keywords`: Supporting keywords
- `meta_description`: SEO meta description
- `internal_links`: Links to your pages
- `external_links`: Links to external sources

### Business Context
- `business_goal`: What business goal this supports
- `service_promoted`: Which therapy service
- `target_conversion`: Desired action
- `campaign`: Related campaign
- `content_cluster`: Content series it belongs to

### Performance (after publishing)
- `published_date`: When it went live
- `published_url`: Where it's published
- `views`: Total views
- `engagement`: Likes, comments, shares, saves
- `conversions`: Clicks, inquiries, bookings

### Compliance
- `hipaa_compliant`: HIPAA compliance check
- `phi_check`: PHI screening status
- `ethical_review`: Ethical review status
- `crisis_resources_included`: Crisis resources present

### Version History
- Track all changes to content
- Timestamps for modifications
- Who made changes

---

## Folder Structure Details

### Content Organization

```
social-media-content/
├── blogs/
│   ├── drafts/              # Work in progress
│   ├── scheduled/           # Ready to publish
│   ├── published/           # Live content
│   └── published/archive/   # Older content
│
├── instagram/
│   ├── feed-posts/
│   │   ├── drafts/
│   │   ├── scheduled/
│   │   └── published/
│   ├── reels/
│   │   ├── drafts/
│   │   ├── scheduled/
│   │   └── published/
│   └── stories/
│       ├── drafts/
│       ├── scheduled/
│       └── published/
│
├── facebook/
│   ├── feed-posts/
│   │   ├── drafts/
│   │   ├── scheduled/
│   │   └── published/
│   └── reels/
│       ├── drafts/
│       ├── scheduled/
│       └── published/
│
├── linkedin/
│   ├── posts/
│   │   ├── drafts/
│   │   ├── scheduled/
│   │   └── published/
│   └── articles/
│       ├── drafts/
│       ├── scheduled/
│       └── published/
│
├── weekly-batches/
│   └── YYYY-week-NN/
│       ├── weekly_schedule.json
│       ├── weekly_plan.md
│       └── (all content for that week)
│
├── campaigns/
│   └── campaign-name/
│       ├── campaign_plan.md
│       └── (all campaign content)
│
└── templates/
    ├── example_blog_metadata_template.json
    └── example_blog_content_template.md
```

### Naming Convention

**Format:** `YYYY-MM-DD_content-type_topic-slug.md`

**Examples:**
- `2025-10-27_blog_anxiety-coping-strategies.md`
- `2025-10-28_instagram-feed_grounding-technique.md`
- `2025-10-29_facebook-post_new-emdr-therapist.md`
- `2025-10-30_linkedin-post_workplace-mental-health.md`

**Metadata files:** Same name with `_meta.json` suffix
- `2025-10-27_blog_anxiety-coping-strategies_meta.json`

---

## Workflows

### Weekly Content Creation Workflow

**Monday Morning:**
1. Review last week's performance
   ```bash
   python manage_content_library.py --performance-report \
     --date-range "2025-10-20:2025-10-27"
   ```

2. Create this week's schedule
   ```bash
   python schedule_content.py --week 2025-11-04
   ```

3. Generate content for the week (5-7 posts)
   ```bash
   # Monday post
   python request_social_post.py \
     --topic "Monday motivation for mental health" \
     --platform Instagram \
     --scheduled-date "2025-11-04" \
     --scheduled-time "09:00" \
     --use-api

   # Tuesday post
   python request_social_post.py \
     --topic "Couples communication tips" \
     --platform Facebook \
     --scheduled-date "2025-11-05" \
     --scheduled-time "13:00" \
     --use-api

   # Continue for rest of week...
   ```

4. Review and schedule all content
   ```bash
   python manage_content_library.py --list scheduled
   ```

**Throughout the Week:**
5. Publish content on scheduled days
6. Track performance
7. Update metadata with engagement metrics

**Sunday Evening:**
8. Week in review
   ```bash
   python view_content.py --recent 7
   ```

---

### Monthly Blog Post Workflow

**Beginning of Month:**
1. Identify blog topic from business data
   - High-demand services
   - Common client questions
   - Local SEO opportunities

2. Create comprehensive blog post
   ```bash
   python create_blog_post.py \
     --topic "Anxiety Coping Strategies" \
     --keywords "anxiety relief, how to manage anxiety" \
     --word-count 2500 \
     --use-api
   ```

3. Review and edit
   ```bash
   python view_content.py --file "anxiety-coping-strategies" --full
   ```

4. Schedule for publication
   ```bash
   python manage_content_library.py --schedule "2025-11-01_blog_anxiety-coping"
   ```

5. Create supporting social media posts
   ```bash
   # Announce blog on Instagram
   python request_social_post.py \
     --topic "New blog: 10 anxiety coping strategies" \
     --platform Instagram \
     --scheduled-date "2025-11-01" \
     --use-api

   # Share on LinkedIn
   python request_social_post.py \
     --topic "Evidence-based anxiety strategies" \
     --platform LinkedIn \
     --scheduled-date "2025-11-02" \
     --use-api
   ```

**Throughout Month:**
6. Publish blog
7. Share on social media
8. Track performance (views, engagement, conversions)

**End of Month:**
9. Generate performance report
   ```bash
   python manage_content_library.py --performance-report \
     --date-range "2025-11-01:2025-11-30"
   ```

---

### Campaign Content Workflow

**Planning Phase:**
1. Create campaign folder
   ```bash
   mkdir -p "social-media-content/campaigns/anxiety-awareness-november-2025"
   ```

2. Plan campaign content
   - 1 long-form blog post
   - 8-12 social media posts
   - Platform mix (Instagram, Facebook, LinkedIn)

**Creation Phase:**
3. Generate all campaign content with campaign tag
   ```bash
   python request_social_post.py \
     --topic "Understanding anxiety triggers" \
     --platform Instagram \
     --campaign "anxiety-awareness-november-2025" \
     --scheduled-date "2025-11-05" \
     --use-api
   ```

4. Organize in campaign folder
   - Move or copy related content
   - Create campaign_plan.md overview

**Execution Phase:**
5. Schedule all posts
6. Publish according to schedule
7. Monitor performance

**Analysis Phase:**
8. Generate campaign performance report
9. Measure against goals
10. Document learnings for future campaigns

---

## Best Practices

### Content Creation
- ✅ Always include business context when creating content
- ✅ Schedule posts for optimal times (system suggests these)
- ✅ Use consistent hashtags for brand recognition
- ✅ Include CTAs appropriate to the platform
- ✅ Check HIPAA compliance before publishing
- ✅ Include crisis resources when discussing severe symptoms

### Organization
- ✅ Move content to proper status folders promptly
- ✅ Update metadata after publishing
- ✅ Track performance metrics regularly
- ✅ Archive old content to keep library manageable
- ✅ Use campaigns for related content series
- ✅ Create weekly batches for easier planning

### Scheduling
- ✅ Plan content 1 week ahead minimum
- ✅ Use optimal posting times from system
- ✅ Vary content types (educational, tips, announcements)
- ✅ Balance platforms (don't post only on Instagram)
- ✅ Consider holidays and special dates
- ✅ Leave buffer time for trending topics

### Performance Tracking
- ✅ Update engagement metrics weekly
- ✅ Track which topics get most engagement
- ✅ Monitor conversion metrics (inquiries, bookings)
- ✅ Adjust strategy based on data
- ✅ Compare performance across platforms
- ✅ Identify top-performing content for replication

---

## Troubleshooting

### "Content library not found"
**Solution:** Run initialization script
```bash
python initialize_content_library.py
```

### "Multiple matches found"
**Solution:** Be more specific with filename
```bash
# Instead of:
python view_content.py --file "anxiety"

# Try:
python view_content.py --file "2025-10-27_instagram_anxiety"
```

### "API key not set"
**Solution:** Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Content not appearing in calendar
**Problem:** Post is in drafts/, not scheduled/

**Solution:** Move to scheduled folder
```bash
python manage_content_library.py --schedule "filename"
```

### Want to change scheduled date
**Solution:**
1. View current metadata
   ```bash
   python view_content.py --file "filename"
   ```

2. Edit metadata file directly
   - Open `*_meta.json` file
   - Update `scheduling.scheduled_date`
   - Save file

### Performance metrics not updating
**Solution:** Manually update metadata
```bash
# Edit the _meta.json file
# Update the "performance" section with actual metrics
```

---

## Tips & Tricks

### Batch Create Content
Create a script to generate multiple posts at once:
```bash
for topic in "anxiety tips" "depression support" "self-care Sunday"; do
    python request_social_post.py \
      --topic "$topic" \
      --platform Instagram \
      --use-api
    sleep 5  # Rate limiting
done
```

### Content Reuse
- Same topic, different platforms
- Repurpose blog sections into social posts
- Turn high-performing posts into blog topics

### Quick Search
Use grep to search content directly:
```bash
grep -r "anxiety" social-media-content/ --include="*.md"
```

### Backup
Regularly backup your content library:
```bash
tar -czf content-backup-$(date +%Y-%m-%d).tar.gz social-media-content/
```

---

## Next Steps

1. **Initialize your library**
   ```bash
   python initialize_content_library.py
   ```

2. **Create your first post**
   ```bash
   python request_social_post.py --topic "Your topic" --use-api
   ```

3. **Plan your week**
   ```bash
   python schedule_content.py --week $(date +%Y-%m-%d)
   ```

4. **Track your content**
   ```bash
   python view_content.py
   ```

---

**You now have a complete content management system for your therapy practice!**

The system automatically organizes everything, tracks performance, and makes it easy to maintain a consistent content calendar.
