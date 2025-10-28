# Content Library Structure

## Overview

This document defines the folder structure and organization system for all social media and blog content created by the therapy practice agents.

---

## Directory Structure

```
therapy-practice-project/
└── social-media-content/
    ├── blogs/
    │   ├── published/
    │   ├── scheduled/
    │   └── drafts/
    ├── instagram/
    │   ├── feed-posts/
    │   │   ├── published/
    │   │   ├── scheduled/
    │   │   └── drafts/
    │   ├── reels/
    │   │   ├── published/
    │   │   ├── scheduled/
    │   │   └── drafts/
    │   └── stories/
    │       ├── published/
    │       ├── scheduled/
    │       └── drafts/
    ├── facebook/
    │   ├── feed-posts/
    │   │   ├── published/
    │   │   ├── scheduled/
    │   │   └── drafts/
    │   └── reels/
    │       ├── published/
    │       ├── scheduled/
    │       └── drafts/
    └── linkedin/
        ├── posts/
        │   ├── published/
        │   ├── scheduled/
        │   └── drafts/
        └── articles/
            ├── published/
            ├── scheduled/
            └── drafts/
```

---

## File Naming Convention

### Format:
```
YYYY-MM-DD_content-type_topic-slug.md
```

### Examples:
- `2025-10-27_blog_anxiety-coping-strategies.md`
- `2025-10-28_instagram-feed_grounding-technique.md`
- `2025-10-29_facebook-post_couples-therapy-benefits.md`
- `2025-10-30_linkedin-article_burnout-prevention.md`

### Metadata File (automatically generated):
```
YYYY-MM-DD_content-type_topic-slug_meta.json
```

---

## Metadata Schema

Each piece of content has an accompanying metadata JSON file:

```json
{
  "content_id": "uuid-here",
  "content_type": "blog|instagram-feed|instagram-reel|facebook-post|linkedin-post",
  "title": "10 Anxiety Coping Strategies",
  "topic": "anxiety coping strategies",
  "created_date": "2025-10-27T10:30:00Z",
  "created_by_agent": "therapy-practice-content-creator",
  "status": "draft|scheduled|published|archived",

  "scheduling": {
    "scheduled_date": "2025-11-01T09:00:00Z",
    "scheduled_time_local": "09:00 AM CST",
    "posting_day": "Friday",
    "optimal_posting_time": true,
    "timezone": "America/Chicago"
  },

  "content_details": {
    "word_count": 2450,
    "reading_time_minutes": 12,
    "platform": "Blog",
    "format": "long-form",
    "target_audience": "adults with anxiety considering therapy"
  },

  "seo": {
    "primary_keyword": "anxiety coping strategies",
    "secondary_keywords": [
      "how to deal with anxiety",
      "anxiety relief techniques",
      "anxiety management"
    ],
    "meta_description": "Discover 10 evidence-based anxiety coping strategies...",
    "focus_keyphrase_density": 1.5,
    "internal_links": [
      "/services/anxiety-therapy",
      "/about/therapists"
    ],
    "external_links": [
      "https://www.apa.org/anxiety-research",
      "https://www.nimh.nih.gov/anxiety"
    ]
  },

  "social_media": {
    "platform": "Instagram",
    "post_type": "feed",
    "hashtags": [
      "#anxietyrelief",
      "#mentalhealthtips",
      "#therapistsofinstagram",
      "#copingskills",
      "#austintherapy"
    ],
    "caption_length": 180,
    "has_cta": true,
    "cta_type": "book_consultation",
    "visual_content_needed": "calming nature image or infographic",
    "accessibility": {
      "alt_text": "Peaceful forest scene for anxiety relief post",
      "captions_required": false
    }
  },

  "business_context": {
    "business_goal": "attract_anxiety_therapy_clients",
    "service_promoted": "anxiety-therapy",
    "target_conversion": "consultation_booking",
    "campaign": "anxiety-awareness-november-2025",
    "content_cluster": "anxiety-management-series"
  },

  "performance": {
    "published_date": null,
    "published_url": null,
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
    },
    "seo_performance": {
      "organic_traffic": 0,
      "keyword_rankings": {},
      "backlinks": 0
    }
  },

  "compliance": {
    "hipaa_compliant": true,
    "phi_check": "no_phi_present",
    "ethical_review": "approved",
    "crisis_resources_included": true
  },

  "version_history": [
    {
      "version": 1,
      "date": "2025-10-27T10:30:00Z",
      "changes": "Initial creation",
      "modified_by": "therapy-practice-content-creator"
    }
  ],

  "notes": "Part of November anxiety awareness campaign. Aligns with increased anxiety therapy demand from business data."
}
```

---

## Content Status Lifecycle

### Draft
- Initial creation
- In review
- Needs revisions
- Location: `drafts/` folder

### Scheduled
- Approved for publishing
- Has scheduled posting date/time
- Location: `scheduled/` folder

### Published
- Live on platform
- Tracking performance metrics
- Location: `published/` folder

### Archived
- Outdated or replaced content
- Kept for historical reference
- Location: `published/archive/` subfolder

---

## Content Organization Best Practices

### 1. **Immediate Save After Creation**
When content is generated by any agent, it should be immediately saved:
- Content file (.md for text content)
- Metadata file (_meta.json)
- Initial status: "draft"

### 2. **Weekly Content Batch Organization**
Create weekly folders for batch content creation:
```
social-media-content/
└── weekly-batches/
    └── 2025-week-43/
        ├── monday_instagram_post.md
        ├── monday_instagram_post_meta.json
        ├── tuesday_facebook_post.md
        ├── tuesday_facebook_post_meta.json
        └── weekly_plan.md
```

### 3. **Content Series/Campaigns**
Group related content in campaign folders:
```
social-media-content/
└── campaigns/
    └── anxiety-awareness-november-2025/
        ├── campaign_plan.md
        ├── blog_01_coping_strategies.md
        ├── instagram_series/
        └── facebook_series/
```

### 4. **Search and Discovery**
Content can be found by:
- Date (file naming)
- Status (folder location)
- Topic (metadata tags)
- Platform (parent folder)
- Campaign (campaign folder)

---

## Integration with Agents

### Content Creator Agent
When generating content, the agent will:
1. Create content file with proper naming
2. Generate metadata JSON automatically
3. Save both files to appropriate folders
4. Set initial status as "draft"

### Content Strategist Agent
When planning content:
1. Creates weekly/monthly content plans
2. Pre-generates metadata templates for planned content
3. Assigns scheduled dates
4. Organizes content by business priorities

### Social Media Manager Agent
When scheduling posts:
1. Moves content from `drafts/` to `scheduled/`
2. Updates metadata with scheduling info
3. Tracks publishing status
4. Updates performance metrics after publishing

---

## Usage Examples

### Example 1: Creating a Blog Post

**Input:**
```bash
python request_blog_post.py \
  --topic "Anxiety Coping Strategies" \
  --keywords "anxiety relief, coping with anxiety" \
  --scheduled-date "2025-11-01" \
  --use-api
```

**Output Files:**
```
social-media-content/
└── blogs/
    └── scheduled/
        ├── 2025-11-01_blog_anxiety-coping-strategies.md
        └── 2025-11-01_blog_anxiety-coping-strategies_meta.json
```

### Example 2: Creating Instagram Post

**Input:**
```bash
python request_social_post.py \
  --topic "5-4-3-2-1 Grounding Technique" \
  --platform Instagram \
  --scheduled-date "2025-10-28" \
  --scheduled-time "09:00" \
  --use-api
```

**Output Files:**
```
social-media-content/
└── instagram/
    └── feed-posts/
        └── scheduled/
            ├── 2025-10-28_instagram-feed_grounding-technique.md
            └── 2025-10-28_instagram-feed_grounding-technique_meta.json
```

### Example 3: Weekly Content Batch

**Input:**
```bash
python create_weekly_content_batch.py \
  --week "2025-week-44" \
  --theme "Couples Therapy Awareness" \
  --use-api
```

**Output:**
```
social-media-content/
└── weekly-batches/
    └── 2025-week-44/
        ├── weekly_plan.md
        ├── 2025-10-28_instagram-feed_communication-tips.md
        ├── 2025-10-28_instagram-feed_communication-tips_meta.json
        ├── 2025-10-29_facebook-post_couples-therapy-benefits.md
        ├── 2025-10-29_facebook-post_couples-therapy-benefits_meta.json
        ├── 2025-10-30_linkedin-post_relationship-health.md
        └── 2025-10-30_linkedin-post_relationship-health_meta.json
```

---

## Content Library Management Commands

### List Scheduled Content
```bash
python manage_content_library.py --list scheduled --platform all
```

### Move to Published
```bash
python manage_content_library.py --publish "2025-10-28_instagram-feed_grounding-technique"
```

### Search by Topic
```bash
python manage_content_library.py --search "anxiety"
```

### View Content Calendar
```bash
python manage_content_library.py --calendar --month "November" --year "2025"
```

### Performance Report
```bash
python manage_content_library.py --performance-report --date-range "2025-10-01:2025-10-31"
```

---

## Backup and Version Control

### Git Integration
The entire `social-media-content/` directory should be version controlled:
```bash
cd therapy-practice-project
git add social-media-content/
git commit -m "Add weekly content batch for week 44"
git push
```

### Backup Schedule
- **Daily**: Automatic backup of `social-media-content/` directory
- **Weekly**: Export content library metadata to CSV for analysis
- **Monthly**: Archive published content older than 6 months

---

## Security and Compliance

### HIPAA Compliance
- No PHI in any content files
- No client names, identifiable information
- All content reviewed for compliance before publishing

### Access Control
- Content creation: Content Creator agent
- Scheduling: Social Media Manager agent
- Publishing: Social Media Manager agent (with approval)
- Analytics: Marketing Analytics agent (read-only)

### Audit Trail
- All metadata includes version history
- All moves between folders logged
- All edits tracked with timestamps

---

## Next Steps

1. Initialize folder structure: `python initialize_content_library.py`
2. Update content creation scripts to use new structure
3. Create content library management tools
4. Set up automated scheduling system
5. Create content calendar visualization

---

**Ready to organize your practice's content systematically!**
