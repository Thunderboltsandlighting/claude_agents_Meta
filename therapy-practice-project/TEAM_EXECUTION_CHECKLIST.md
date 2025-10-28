# Team Execution Checklist

**Purpose:** Step-by-step executable checklist for creating weekly content. Follow this exactly - no decisions required.

**Time Required:** 10-15 minutes per week

**Frequency:** Once per week (recommended: Friday for next week's content)

---

## Pre-Execution Checklist

Before starting, verify these requirements:

- [ ] You are in the correct directory: `/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project/`
- [ ] Anthropic API key is loaded (file `.env` exists with `ANTHROPIC_API_KEY=sk-...`)
- [ ] Python 3.8+ is installed (run: `python3 --version`)
- [ ] You have 10-15 minutes of uninterrupted time

**Verify Directory:**
```bash
pwd
# Expected output: /Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project
```

**Verify API Key:**
```bash
cat .env | grep ANTHROPIC_API_KEY
# Expected output: ANTHROPIC_API_KEY=sk-ant-...
```

**If anything fails, STOP and contact system administrator.**

---

## Step 1: Calculate Week Date

**Goal:** Find the Monday date for the week you're creating content for.

**Current Week (creating for next week):**
```bash
python3 -c "from datetime import datetime, timedelta; monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7); print(f'Next Monday: {monday.strftime(\"%Y-%m-%d\")}')"
```

**Example output:**
```
Next Monday: 2025-11-04
```

**Write down this date:** `____________________`

---

## Step 2: Run Content Creation Script

**Copy this command exactly, replacing `YYYY-MM-DD` with the date from Step 1:**

```bash
python3 create_weekly_batch_v2.py --week YYYY-MM-DD --use-api --auto-approve
```

**Example:**
```bash
python3 create_weekly_batch_v2.py --week 2025-11-04 --use-api --auto-approve
```

**Expected behavior:**
- Script will start with a greeting
- You'll see 6 interactive prompts
- Answer each prompt by typing a number and pressing Enter

---

## Step 3: Answer Interactive Prompts

The script will ask you 6 questions. Follow this guide:

### Prompt 1: Theme Selection

```
Choose your theme approach:
  1. Random Suggestions (AI picks from service areas)
  2. Observance-Based (Focus on upcoming mental health observances)
  3. Custom Theme (You provide the topic)

Enter your choice (1-3):
```

**Recommended answer:** `2` (observance-based for timely content)

**Alternative:** `1` if no observances are upcoming

**Custom:** `3` only if you have a specific topic in mind

---

### Prompt 2: Random/Observance Selection

**If you chose option 1 (Random):**
```
Here are 5 suggested themes:
  1. Managing Workplace Stress
  2. Coping with Grief and Loss
  [...]

Choose a theme (1-5) or 'r' for new suggestions:
```

**Action:** Type a number `1-5` or type `r` for new suggestions

**If you chose option 2 (Observance):**
```
Upcoming mental health observances:
  1. World Mental Health Day (2025-10-10)
  2. ADHD Awareness Month (October)
  [...]

Choose an observance (1-5):
```

**Action:** Type a number `1-5` for the most relevant observance

---

### Prompt 3: Tone Selection

```
Choose content tone:
  1. Professional and Clinical
  2. Warm and Empathetic
  3. Educational and Informative
  4. Personal and Relatable

Enter your choice (1-4):
```

**Recommended answer:** `2` (warm and empathetic)

**Professional:** `1` for clinical topics (ADHD diagnosis, treatment modalities)

**Educational:** `3` for awareness/psychoeducation content

**Personal:** `4` for founder story/personal insights

---

### Prompt 4: Social Post Length

```
Choose social media post length:
  1. Short (150 words) - Quick tips, bite-sized insights
  2. Medium (200 words) - Balanced content, most versatile
  3. Long (250 words) - In-depth, educational content

Enter your choice (1-3):
```

**Recommended answer:** `2` (medium - 200 words)

**Short:** `1` for simple tips or quotes

**Long:** `3` for complex topics needing explanation

---

### Prompt 5: Target Audience

```
Choose primary audience:
  1. General Mental Health Audience
  2. Parents and Families
  3. Couples and Relationships
  4. Teens and Young Adults
  5. Adult Professionals

Enter your choice (1-5):
```

**Recommended answer:** `1` (general audience for broad appeal)

**Specific:** Choose 2-5 if the theme specifically targets that group

**Example:** ADHD in children → Choose `2` (Parents and Families)

---

### Prompt 6: Blog Focus

```
Choose blog post focus:
  1. Comprehensive Overview
  2. Practical Strategies and Tips
  3. When to Seek Professional Help
  4. Local Hendersonville Resources

Enter your choice (1-4):
```

**Recommended answer:** `2` (practical strategies)

**Overview:** `1` for broad topics (What is EMDR?)

**Help-seeking:** `3` for crisis topics or when therapy helps

**Local:** `4` when highlighting local resources

---

## Step 4: Wait for Generation

**What you'll see:**
```
✓ Generating social media content...
✓ Generating blog post...
✓ Creating weekly summary...
✓ Content creation complete!
```

**Time:** 2-3 minutes for AI generation

**Do not close terminal while generating.**

---

## Step 5: Locate Your Content

**The script outputs the summary file location:**
```
✓ Weekly summary saved to: weekly-batches/2025-week-45/WEEK_45_CONTENT_SUMMARY.md
```

**Open this file immediately:**
```bash
open weekly-batches/2025-week-XX/WEEK_XX_CONTENT_SUMMARY.md
```

**This file contains:**
- ✅ All file paths
- ✅ Content previews
- ✅ Hashtags
- ✅ Image requirements
- ✅ Scheduling checklist

---

## Step 6: Review Content

**Open the Weekly Content Summary file and follow its checklist:**

### Review Checklist (in the summary file)

- [ ] **Read all social post previews** - Check for tone, accuracy, HIPAA compliance
- [ ] **Read blog post** - Verify 2000-3000 words, question-based headings, FAQ section
- [ ] **Check hashtags** - Ensure relevant and appropriate
- [ ] **Note image requirements** - Count total images needed

**Quality checks:**
- [ ] No patient stories or PHI (HIPAA compliance)
- [ ] No diagnosis via content (ethical compliance)
- [ ] Tone matches practice brand
- [ ] Call-to-action is clear

**If content needs revision:** Make notes in the "Notes" section of the weekly summary file.

---

## Step 7: Create Images

**From the Weekly Content Summary:**
- Total images needed: Listed at top of summary
- Social posts: 8 images (one per post)
- Blog post: 1 featured image
- **Total: 9 images per week**

**Image specifications:**
- **Instagram:** 1080 x 1080 px (square)
- **Facebook:** 1200 x 630 px (landscape)
- **LinkedIn:** 1200 x 627 px (landscape)
- **Blog featured image:** 1200 x 630 px (landscape)

**Design tools:**
- Canva (recommended)
- Adobe Express
- Figma

**Design tips:**
- Use practice brand colors
- Include practice logo
- Text overlay with key quote from post
- Stock photos from Unsplash/Pexels (licensed)

**Save images to:**
```
weekly-batches/2025-week-XX/images/
```

**Naming convention:**
- `instagram-monday.png`
- `facebook-tuesday.png`
- `linkedin-monday.png`
- `blog-featured.png`

---

## Step 8: Schedule Content

**Use your scheduling tool (Buffer/Later/Hootsuite):**

### Schedule Each Post

**From the Weekly Content Summary, for each post:**

1. **Copy content** from the file path listed
2. **Upload image** from `images/` folder
3. **Copy hashtags** from summary
4. **Set date/time** as listed in summary
5. **Save as scheduled**
6. **Mark checkbox** in summary file as done

**Repeat for all 8 social posts.**

**Posting schedule:**
- Monday: Instagram + LinkedIn
- Tuesday: Facebook + Instagram
- Wednesday: Instagram + LinkedIn
- Thursday: Facebook + Instagram

**Optimal times** (already in summary):
- Weekday morning: 9:00 AM
- Weekday evening: 6:30 PM
- Weekend: 10:00 AM

---

## Step 9: Publish Blog Post

### Squarespace Publishing Checklist

**Open the blog post folder:**
```bash
cd blog-posts/drafts/[blog-folder-name]
```

**Files you'll use:**
- `[theme-name].md` - Main content
- `schema_blogposting.json` - Schema markup
- `schema_faqpage.json` - FAQ schema
- `social_media_package.md` - Social captions
- `instagram_carousel_prompts.md` - Carousel ideas
- `metadata.json` - SEO data

### Step 9a: Copy Content to Squarespace

1. **Log in to Squarespace:** [your-site].squarespace.com/config
2. **Pages → Blog → + New Post**
3. **Copy entire content** from `[theme-name].md` into Squarespace editor
4. **Format:**
   - Headings should be H2 (not H1)
   - FAQ section at bottom
   - References linked properly

### Step 9b: Add SEO Metadata

1. **Click Settings (gear icon)**
2. **SEO tab:**
   - **Page Title:** Copy from `metadata.json` → `seo.title`
   - **Description:** Copy from `metadata.json` → `seo.description`
   - **URL Slug:** Copy from `metadata.json` → `seo.url_slug`

### Step 9c: Add Schema Markup

1. **Click Settings → Advanced → Page Header Code Injection**
2. **Copy this template:**
```html
<script type="application/ld+json">
[PASTE SCHEMA_BLOGPOSTING.JSON CONTENT HERE]
</script>

<script type="application/ld+json">
[PASTE SCHEMA_FAQPAGE.JSON CONTENT HERE]
</script>
```
3. **Upload to JSONKeeper.com (Alternative if code injection doesn't work):**
   - Go to [jsonkeeper.com](https://jsonkeeper.com)
   - Paste `schema_blogposting.json` content → Create
   - Copy hosted URL
   - Paste `schema_faqpage.json` content → Create
   - Copy hosted URL
   - Reference both URLs in blog post

### Step 9d: Upload Featured Image

1. **Click Featured Image**
2. **Upload:** `images/blog-featured.png`
3. **Alt text:** Use title from metadata

### Step 9e: Schedule or Publish

- **Publish immediately:** Click Publish
- **Schedule:** Click Schedule → Choose Friday 9:00 AM

---

## Step 10: Post Blog Social Media Content

**Use the social media package from blog folder:**

1. **Open:** `social_media_package.md`
2. **Three caption variants provided:**
   - Short and punchy
   - Detailed and informative
   - Question-driven

**Schedule blog promotion posts:**
- **Friday (blog publish day):** Instagram post with link in bio
- **Sunday:** Facebook post with direct blog link
- **Monday:** LinkedIn article share

**Use Instagram carousel prompts:**
- **Open:** `instagram_carousel_prompts.md`
- **Create 10-slide carousel** in Canva using prompts
- **Schedule for Tuesday** following blog publish

---

## Step 11: Final Validation

**Before marking week complete, verify:**

- [ ] All 8 social posts scheduled (check scheduling tool)
- [ ] All 8 images uploaded
- [ ] Blog post published or scheduled on Squarespace
- [ ] Blog featured image uploaded
- [ ] Blog schema markup added
- [ ] Blog SEO metadata configured
- [ ] Blog social promotion scheduled (3 posts)
- [ ] Checkboxes in Weekly Content Summary file marked

**If all checked, you're done!**

---

## Step 12: Archive and Track

### Mark Week as Complete

**In the Weekly Content Summary file:**
- Update status from `DRAFT` to `SCHEDULED`
- Add completion date in Notes section

**Example:**
```markdown
**Status:** SCHEDULED ✅
**Completion Date:** 2025-10-28
```

### Move to Scheduled Folder (Optional)

```bash
# This happens automatically, but you can verify:
ls social-media-content/instagram/feed-posts/scheduled/
ls social-media-content/facebook/posts/scheduled/
ls social-media-content/linkedin/articles/scheduled/
```

---

## Troubleshooting

### Error: "command not found: python3"
**Solution:** Try `python` instead:
```bash
python create_weekly_batch_v2.py --week 2025-11-04 --use-api --auto-approve
```

### Error: "ANTHROPIC_API_KEY not found"
**Solution:** Check `.env` file exists:
```bash
ls -la .env
cat .env
```
If missing, contact administrator for API key.

### Error: "No such file or directory"
**Solution:** Verify you're in correct directory:
```bash
pwd
# Should show: /Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project
```

### Content Quality Issues
**Solution:** Regenerate with different style choices:
- Try different tone (e.g., Professional instead of Warm)
- Try different audience (e.g., General instead of Parents)
- Try different blog focus

### Script Freezes During Generation
**Solution:**
- Wait 5 minutes (API can be slow)
- If still frozen, press Ctrl+C and restart
- Check internet connection

---

## Success Criteria

**You've successfully completed the workflow when:**

✅ 8 social posts created and scheduled
✅ 1 blog post published on Squarespace
✅ 9 images created and uploaded
✅ Schema markup added to blog
✅ SEO metadata configured
✅ All checkboxes in Weekly Content Summary marked
✅ Total time: <60 minutes from start to finish

---

## Weekly Workflow Summary

| Step | Task | Time | Tools |
|------|------|------|-------|
| 1-2  | Calculate date + Run script | 1 min | Terminal |
| 3-5  | Answer prompts + Wait | 5 min | Terminal |
| 6    | Review content | 5 min | Text editor |
| 7    | Create images | 20 min | Canva |
| 8    | Schedule social posts | 15 min | Buffer/Later |
| 9    | Publish blog | 10 min | Squarespace |
| 10   | Schedule blog promo | 5 min | Buffer/Later |
| 11-12| Validate + Archive | 2 min | Checklist |
| **Total** | **Complete workflow** | **~60 min** | |

---

## Support Contacts

**Technical Issues:**
- System Administrator: [contact info]

**Content Questions:**
- Practice Owner: [contact info]

**API Key Issues:**
- System Administrator: [contact info]

---

**Document Version:** 2.0
**Last Updated:** October 28, 2025
**Next Review Date:** November 28, 2025

---

## Appendix: Quick Reference Commands

**Calculate next Monday:**
```bash
python3 -c "from datetime import datetime, timedelta; monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7); print(monday.strftime('%Y-%m-%d'))"
```

**Create content for specific week:**
```bash
python3 create_weekly_batch_v2.py --week YYYY-MM-DD --use-api --auto-approve
```

**Open weekly summary:**
```bash
open weekly-batches/2025-week-XX/WEEK_XX_CONTENT_SUMMARY.md
```

**View all scheduled content:**
```bash
python3 manage_content_library.py --calendar
```

**Find specific content:**
```bash
python3 view_content.py --search "anxiety"
```
