# Content Creator CLI - User Guide

## Launching the System

### Option 1: Quick Launch (Easiest)
```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
./start.sh
```

### Option 2: Direct Python
```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
python3 content_cli.py
```

---

## Main Menu

When you launch, you'll see:

```
================================================================================
  ██╗  ██╗███████╗███╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗
  ██║  ██║██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║
  ███████║█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║
  ██╔══██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║
  ██║  ██║███████╗██║ ╚████║██████╔╝███████╗██║  ██║███████║╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                        COUNSELING CONTENT CREATOR
================================================================================

What would you like to do?

  1. 🆕 Create New Weekly Content (8 posts + blog)
  2. 📁 View Existing Content
  3. 🖼️  Generate Images for Content
  4. ℹ️  System Information

  Q. Quit
```

---

## Menu Options

### 1. Create New Weekly Content

**What it does:** Generates a complete weekly content batch (8 social posts + 1 blog post)

**Steps:**
1. Select week (choose from suggested Mondays or enter custom date)
2. Choose whether to include blog post (Y/n)
3. Confirm you're ready to proceed
4. Interactive prompts for:
   - Theme selection (random, observance-based, or custom)
   - Content style (tone, length, audience, blog focus)
5. Claude generates all content (5-10 minutes)

**Output:** Complete week folder with:
- Social posts (Instagram, Facebook, LinkedIn)
- Blog post (if selected)
- Image generation guides
- Weekly summary checklist

---

### 2. View Existing Content

**What it does:** Browse and open existing weekly content batches

**Features:**
- Lists all created weeks
- Shows completion status (✓ Complete / ⚠ Incomplete)
- Shows image count for each week
- Quick-open week folders
- Option to open all weeks folder

**Navigation:**
- Enter number to open specific week
- Press A to open all weeks folder
- Press B to go back

---

### 3. Generate Images for Content

**What it does:** Shows image generation workflow and opens weeks needing images

**Features:**
- Lists weeks that need images created
- Shows 15-minute workflow steps
- Quick-open week folders
- Access to image prompts and guides

**Workflow shown:**
1. Open the week folder
2. Open QUICK_IMAGE_PROMPT.txt
3. Copy prompt → Paste into ChatGPT or Canva AI
4. Upload to Canva → Use 'Resize' for all formats
5. Add text overlays → Export to images/ folder

---

### 4. System Information

**What it does:** Shows system status and configuration

**Displays:**
- API key configuration status
- Number of content batches created
- Total images generated
- Project paths
- Documentation links

---

## Keyboard Shortcuts

- **Numbers (1-4):** Select menu option
- **Q:** Quit application
- **B:** Back to previous menu (where applicable)
- **A:** All/View all (in content view)
- **Ctrl+C:** Cancel current operation

---

## Week Selection

When creating new content, you'll see:

```
📅 Suggested upcoming Mondays:
  1. Week 45: 2025-11-04 (November 04)
  2. Week 46: 2025-11-11 (November 11)
  3. Week 47: 2025-11-18 (November 18)
  4. Week 48: 2025-11-25 (November 25)

  Or enter custom date

Enter choice (1-4) or date (YYYY-MM-DD):
```

**Options:**
- Press 1-4 to select suggested Monday
- Enter custom date in YYYY-MM-DD format

---

## Theme Selection (During Content Creation)

You'll be prompted to choose one of three theme modes:

### 1. Random Suggestions
- AI picks themes from therapy service areas
- Shows 5 themes at a time
- Press R to see next 5
- Press C for custom theme

### 2. Observance-Based
- Focuses on upcoming mental health observances
- Shows relevant awareness days/weeks/months
- Automatically suggests timely content

### 3. Custom Theme
- Enter any theme you want
- Examples:
  - "Anxiety and sleep problems"
  - "Communication skills for couples"
  - "Teen mental health in schools"

---

## Content Style Selection

After theme, you'll customize content style:

### Tone Options:
1. Professional & Clinical
2. Warm & Empathetic (Recommended)
3. Educational & Informative
4. Personal & Story-Based

### Social Post Length:
1. Short (150 words)
2. Medium (200 words) (Recommended)
3. Longer (250 words)

### Target Audience:
1. General audience
2. Parents
3. Couples
4. Teens/Young adults
5. Adults seeking individual therapy

### Blog Focus:
1. Comprehensive guide (covers everything)
2. Focus on practical strategies
3. Focus on when to seek help
4. Local resources emphasis (Hendersonville NC)

---

## Tips & Best Practices

### Creating Content
- **Best day:** Run on Monday morning to plan the week
- **Time needed:** 10-15 minutes total (5-10 min generation + 5 min review)
- **Frequency:** Once per week for upcoming week

### Theme Selection
- Use **observance-based** for timely, relevant content
- Use **random** when you want variety
- Use **custom** when you have specific topics in mind

### Image Creation
- Create images right after content generation while theme is fresh
- Use the 15-minute Canva workflow
- Save images to the images/ folder in each week

### Workflow
1. Monday: Generate Week N content
2. Monday: Create images (15 min)
3. Monday: Review and schedule in social media tools
4. Tuesday-Friday: Content auto-posts
5. Friday: Blog publishes

---

## Troubleshooting

### API Key Not Found
```
❌ Error: ANTHROPIC_API_KEY not found in environment
```

**Solution:**
```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
python3 setup_api_key.py
```

### Can't Find Week Folders
If "View Existing Content" shows no content but you've created some:

**Check location:**
```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
ls -la weekly-batches/
```

### CLI Won't Start
```bash
# Check Python version (need 3.10+)
python3 --version

# Check if content creator exists
ls -la create_weekly_batch_v2.py

# Try running directly
python3 content_cli.py
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Launch CLI | `./start.sh` or `python3 content_cli.py` |
| Create content | Menu option 1 |
| View content | Menu option 2 |
| Image guide | Menu option 3 |
| Check status | Menu option 4 |
| Quit | Press Q |
| Go back | Press B |

---

## File Structure

After using the CLI, your content will be organized like:

```
therapy-practice-project/
├── content_cli.py              ← The menu system
├── start.sh                    ← Quick launcher
├── create_weekly_batch_v2.py   ← Core generator
└── weekly-batches/
    ├── 2025-week-45/
    │   ├── instagram/
    │   ├── facebook/
    │   ├── linkedin/
    │   ├── blog/
    │   ├── images/
    │   ├── QUICK_IMAGE_PROMPT.txt
    │   ├── IMAGE_GENERATION_GUIDE.md
    │   └── WEEK_45_CONTENT_SUMMARY.md
    ├── 2025-week-46/
    └── 2025-week-47/
```

---

## Support

**Documentation:**
- `CLI_GUIDE.md` - This file
- `TEAM_EXECUTION_CHECKLIST.md` - Main workflow guide
- `CANVA_WORKFLOW_SYSTEM.md` - Image creation detailed guide
- `README.md` - Project overview

**Need help?**
Open an issue or check the documentation files above.

---

**Generated:** October 30, 2025
**Version:** 1.0
**For:** Hendersonville Counseling Content Creator
