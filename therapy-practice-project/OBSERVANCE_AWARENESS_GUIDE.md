# Mental Health Observance Awareness System

## Overview

Your content creation system now **automatically tracks 60+ mental health awareness days, weeks, and months** and suggests timely, relevant content with appropriate lead time.

**Problem Solved:** You'll never miss Indigenous Peoples Day, Mental Health Month, Suicide Prevention Day, or any other important observance again. The system forecasts 14 days ahead and proactively suggests observance-related content.

---

## How It Works

### 1. **Observance Calendar**

The system maintains a comprehensive calendar in [mental_health_observances.json](mental_health_observances.json) with:

- **60+ observances** tracked throughout the year
- **Pre-written content ideas** for each observance (4-7 topic variations)
- **Focus areas** (keywords related to the observance)
- **Optimal lead times** (when to post before/during the observance)

### 2. **Intelligent Forecasting**

When you run `create_weekly_batch.py`, the system:

1. **Looks ahead 14 days** from your scheduled week
2. **Identifies relevant observances** within that window
3. **Suggests timely content** with 3-7 day lead time
4. **Mixes observance content (40-60%) with regular content (40-60%)**

### 3. **Priority System**

Content suggestions follow this priority:

**PRIORITY 1: Upcoming Observances** 📅
- Timely awareness content
- Posted 3-7 days before or during observance
- Automatically rotates through observance content ideas

**PRIORITY 2: High-Priority Service Areas** 🔴
- Service areas with < 3 existing posts
- Fills gaps in your content library

**PRIORITY 3: Medium-Priority Service Areas** 🟡
- Service areas with 3-5 posts
- Maintains balanced coverage

**PRIORITY 4: Low-Priority Service Areas** 🟢
- Service areas with 6+ posts
- Keeps content fresh

---

## Major Observances Tracked

### By Month

| Month | Major Observances |
|-------|-------------------|
| **January** | Mental Wellness Month |
| **February** | Black History Month, Eating Disorders Awareness Week |
| **March** | Self-Injury Awareness Day, Brain Awareness Week, World Bipolar Day |
| **April** | Sexual Assault Awareness Month, Alcohol Awareness Month, Autism Month |
| **May** | Mental Health Month, Maternal Mental Health Week, Children's Mental Health Day |
| **June** | Pride Month, PTSD Awareness Month, Men's Health Month |
| **July** | Minority Mental Health Month, International Self-Care Day |
| **August** | Supporting Young Minds (Back to School), National Grief Awareness Day |
| **September** | Recovery Month, Suicide Prevention Month, World Suicide Prevention Day |
| **October** | ADHD Awareness Month, Depression Awareness Month, World Mental Health Day, Indigenous Peoples Day, OCD Awareness Week |
| **November** | Family Caregivers Month, Native American Heritage Month, Transgender Awareness Week, Survivors of Suicide Loss Day |
| **December** | International Day of Persons with Disabilities |

### Full Calendar

See [mental_health_observances.json](mental_health_observances.json) for the complete calendar with all 60+ observances and pre-written content ideas.

---

## Usage

### **Step 1: Create Weekly Schedule**
```bash
# Create schedule (if not already done)
python schedule_content.py --week 2025-11-04
```

### **Step 2: Preview Observances & Suggestions**
```bash
# See what observances are coming up and what topics will be suggested
python create_weekly_batch.py --week 2025-11-04 --preview
```

**Example Output:**
```
📅 Upcoming Mental Health Observances (next 2 weeks):
   📌 ADHD Awareness Month (October 1 - October 31)
      Focus: adhd, executive function, focus
   📌 Depression Awareness Month (October 1 - October 31)
      Focus: depression, treatment, awareness
   📌 World Mental Health Day (October 10)
      Focus: mental health, global awareness
   📌 Indigenous Peoples Day (October 13)
      Focus: indigenous mental health, cultural competence, trauma

SUGGESTED CONTENT TOPICS FOR THE WEEK
================================================================
Total posts to create: 9
  📅 Observance-related: 4
  📝 Regular content: 5

Tuesday - 2025-11-04
----------------------------------------------------------------
  1. [Instagram] @ 09:00 | 📅 OBSERVANCE
     Topic: Understanding ADHD in Adults
     Observance: ADHD Awareness Month

  2. [LinkedIn ] @ 09:00 | 📅 OBSERVANCE
     Topic: Indigenous Peoples Day: Honoring Resilience and Mental Health
     Observance: Indigenous Peoples Day
```

### **Step 3: Create Content**

**Option A: Interactive Mode** (Recommended)
```bash
python create_weekly_batch.py --week 2025-11-04 --use-api
```
- Review each suggested topic
- Press ENTER to keep it
- Type new topic to replace it
- Type "skip" to skip that post

**Option B: Auto-Approve Mode** (Fastest)
```bash
python create_weekly_batch.py --week 2025-11-04 --use-api --auto-approve
```
- Trusts AI completely
- Creates all content automatically
- No manual review needed

---

## Example: Indigenous Peoples Day

**Scenario:** It's October 7, 2025. You're planning content for the week of October 13.

### Without Observance Awareness:
- You manually remember Indigenous Peoples Day is October 13
- You manually create a post about it
- You post it on October 13 (day-of, less ideal)

### With Observance Awareness:
```bash
python create_weekly_batch.py --week 2025-10-06 --preview
```

**System automatically suggests:**
```
📅 Upcoming Mental Health Observances (next 2 weeks):
   📌 Indigenous Peoples Day (October 13)
      Focus: indigenous mental health, cultural competence, trauma

SUGGESTED CONTENT TOPICS:
  1. [Instagram] @ 09:00 | 📅 OBSERVANCE
     Topic: Indigenous Peoples Day: Honoring Resilience and Mental Health
     Observance: Indigenous Peoples Day
```

**Result:**
- System forecasts Indigenous Peoples Day 7 days ahead
- Suggests timely content automatically
- Content posts October 10 (3 days before) for optimal awareness
- You never have to remember manually!

---

## How Content Ideas Are Selected

For each observance, the system has **4-7 pre-written topic variations**.

**Example: ADHD Awareness Month**
1. "Understanding ADHD in Adults"
2. "ADHD and Relationship Challenges"
3. "Executive Function Skills for ADHD"
4. "ADHD Diagnosis Process for Adults"
5. "ADHD Medication vs Therapy: What Works Best"
6. "Time Management Strategies for ADHD"

The system:
- **Randomly selects** from available ideas
- **Checks if you've already posted** that topic
- **Avoids duplicates** within the same batch
- **Rotates through all variations** over time

---

## Adding Your Own Observances

You can add custom observances to [mental_health_observances.json](mental_health_observances.json):

```json
{
  "observances": {
    "december": {
      "specific_dates": [
        {
          "name": "Your Custom Observance",
          "date": "December 15",
          "type": "day",
          "focus_areas": ["keyword1", "keyword2"],
          "content_ideas": [
            "Custom Topic Idea 1",
            "Custom Topic Idea 2",
            "Custom Topic Idea 3"
          ]
        }
      ]
    }
  }
}
```

---

## Lead Time Recommendations

The system uses smart lead times based on observance type:

| Type | Lead Time | Example |
|------|-----------|---------|
| **Month** | 3 days before start | Post Sept 28 for October observances |
| **Week** | Start of week | Post Monday for week observances |
| **Day** | 3-5 days before | Post Oct 7 for Oct 10 observance |

---

## Benefits

✅ **Never Miss Important Dates**
- Automatic forecasting 14 days ahead
- No manual calendar checking needed

✅ **Timely Content**
- Posts appear before/during observances
- Maximum relevance and engagement

✅ **Reduced Planning Load**
- System remembers 60+ dates for you
- Pre-written content ideas ready to use

✅ **Balanced Content Mix**
- 40-60% observance content (timely)
- 40-60% evergreen content (consistent)

✅ **Culturally Relevant**
- Tracks diverse observances (Indigenous Peoples Day, Pride Month, Minority Mental Health Month, etc.)
- Shows community awareness and cultural competence

✅ **Engagement Boost**
- Trending hashtags on observance days
- Aligns with what people are talking about

---

## Visual Indicators

When reviewing suggestions, look for these icons:

| Icon | Meaning |
|------|---------|
| 📅 | Observance-related content (high priority) |
| 🔴 | High-priority service area (< 3 posts) |
| 🟡 | Medium-priority service area (3-5 posts) |
| 🟢 | Low-priority service area (6+ posts) |

---

## Complete Workflow

```bash
# Week of October 6 - Create content for Week 45
cd therapy-practice-project

# 1. Create schedule
python schedule_content.py --week 2025-10-06

# 2. Preview observances and suggestions
python create_weekly_batch.py --week 2025-10-06 --preview

# Output shows:
# - Upcoming observances (Indigenous Peoples Day, World Mental Health Day)
# - Suggested topics (mix of observance + regular)
# - Content gaps filled

# 3. Create all content in one command
python create_weekly_batch.py --week 2025-10-06 --use-api

# 4. Review created content in scheduled folders
# 5. Post manually on scheduled dates
# 6. Track performance with weekly check-ins
python weekly_checkin.py
```

---

## FAQ

**Q: Will I ONLY get observance content?**
No! The system mixes 40-60% observance content with 40-60% regular service area content for balance.

**Q: What if I don't like the suggested observance topic?**
In interactive mode, you can type a new topic to replace it or type "skip" to skip that post.

**Q: Can I turn off observance awareness?**
Yes, the system will still work if you delete or empty the `mental_health_observances.json` file. It will just suggest regular topics.

**Q: What if there are no observances this week?**
The system looks ahead 14 days. If no observances are found, it suggests 100% regular service area topics.

**Q: Can I add my own custom observances?**
Yes! Edit `mental_health_observances.json` and add your custom dates with content ideas.

**Q: How does it avoid repeating observance content from last year?**
The system checks your existing content library for duplicate topics before suggesting anything.

---

## Related Files

- [create_weekly_batch.py](create_weekly_batch.py) - Main batch creator script
- [mental_health_observances.json](mental_health_observances.json) - Complete observance calendar
- [schedule_content.py](schedule_content.py) - Weekly schedule creator
- [weekly_checkin.py](weekly_checkin.py) - Performance tracking
- [PERFORMANCE_LEARNING_SYSTEM.md](PERFORMANCE_LEARNING_SYSTEM.md) - Performance learning guide

---

**Last Updated:** October 28, 2025
**System Status:** ✅ Operational with 60+ observances tracked
