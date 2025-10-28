# How-To Guides Summary

## ✅ Complete Guides Created

Your therapy practice management system now includes **comprehensive how-to guides** for interacting with all agents.

---

## 📚 Guide Overview

### 1. Social Media Content Agents Guide
**File**: [HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md](therapy-practice-project/HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md)

**Covers**:
- ✅ How to request social media posts (Instagram, Facebook, LinkedIn)
- ✅ How to create SEO-optimized blog posts (1500-3000 words)
- ✅ How to plan weekly content strategy
- ✅ How to handle crisis situations on social media
- ✅ Complete code examples and scripts
- ✅ Troubleshooting common issues

**Agents Covered**:
- Content Strategist (SEO research, content planning)
- Content Creator (blog posts, social content)
- Social Media Manager (scheduling, engagement)

**Key Features**:
- `request_social_post.py` script for easy post generation
- Example conversations with agents
- Platform-specific requirements (Instagram vs Facebook vs LinkedIn)
- Crisis response protocols

---

### 2. Business Intelligence Agents Guide
**File**: [HOW_TO_USE_BUSINESS_AGENTS.md](therapy-practice-project/HOW_TO_USE_BUSINESS_AGENTS.md)

**Covers**:
- ✅ How to format and upload practice data
- ✅ Data templates (JSON, CSV, Python dict)
- ✅ How to request business intelligence analysis
- ✅ How to track marketing ROI
- ✅ How to research local market opportunities
- ✅ How to optimize practice operations

**Agents Covered**:
- Business Analyst (financials, KPIs, forecasting)
- Marketing Analytics (ROI, content performance)
- Market Research (local demand, competitors)
- Practice Operations (scheduling, efficiency)

**Key Features**:
- `analyze_practice_data.py` script for automated analysis
- Data export instructions for SimplePractice, TherapyNotes
- Weekly and monthly analysis workflows
- Complete code examples

---

### 3. Data Templates
**Directory**: [data_templates/](therapy-practice-project/data_templates/)

**Files Created**:
- `weekly_practice_data.json` - Weekly metrics template
- `monthly_practice_data.json` - Monthly comprehensive template
- `README.md` - Complete data template documentation

**What's Included**:
- Pre-filled example data (realistic sample data)
- Field-by-field descriptions
- Required vs. optional fields
- Data quality tips
- SimplePractice/TherapyNotes conversion examples
- Automation examples (cron jobs, schedulers)

---

## 🚀 Quick Start

### For Social Media Content:

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"

# Request an Instagram post
python request_social_post.py \
  --topic "5 signs you might benefit from therapy" \
  --platform Instagram \
  --use-api
```

### For Business Intelligence:

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"

# Analyze practice data
python analyze_practice_data.py --sample

# Or with your own data
python analyze_practice_data.py --file data_templates/weekly_practice_data.json
```

---

## 📋 What Each Guide Contains

### Social Media Agents Guide

**Section 1: Overview**
- Your 3 social media agents explained
- What each agent does
- When to use which agent

**Section 2: How to Request Content**
- Method 1: Quick social media post (easiest)
- Method 2: Blog post creation (SEO-optimized)
- Method 3: Weekly content planning

**Section 3: Common Use Cases**
- Daily social media posts
- Weekly blog posts
- Monthly content strategy
- Crisis response

**Section 4: Example Conversations**
- Request Instagram post → Get post with hashtags
- Request blog post → Get 2500-word SEO-optimized article
- Handle crisis comment → Get immediate response protocol

**Section 5: Technical Setup**
- Prerequisites (Python, Claude API)
- Test your setup
- Troubleshooting

**Section 6: Best Practices**
- DO's and DON'Ts
- Content quality tips
- Engagement strategies

---

### Business Intelligence Agents Guide

**Section 1: Overview**
- Your 4 business intelligence agents explained
- What each agent analyzes
- How they work together

**Section 2: Data Formats**
- Python dictionary format
- JSON file format
- CSV export format
- Manual input format

**Section 3: Data Templates**
- Weekly practice data template
- Monthly practice data template
- Field descriptions

**Section 4: How to Upload Data**
- Method 1: Direct script (recommended)
- Method 2: Export from practice software
- Method 3: Manual data entry

**Section 5: Using Each Agent**
- Business Analyst (revenue, KPIs)
- Marketing Analytics (ROI tracking)
- Market Research (local opportunities)
- Practice Operations (efficiency)

**Section 6: Complete Workflows**
- Weekly workflow (Monday: analyze → plan content)
- Monthly workflow (comprehensive review)
- Quarterly workflow (strategic planning)

---

## 🎯 Integration Examples

### Example 1: Complete Weekly Cycle

**Monday Morning - Business Intelligence:**
```bash
# Export data from practice software
# Convert to JSON
# Analyze
python analyze_practice_data.py --file weekly_data.json
```

**Output**: "Anxiety therapy has waitlist, couples therapy at 60% capacity"

**Tuesday Morning - Content Strategy:**
```python
# Use business insights to plan content
# Focus: Create anxiety content, promote couples therapy

python request_content_strategy.py \
  --business-context "anxiety-waitlist-couples-underutilized"
```

**Output**: Weekly content calendar (1 blog + 5 social posts)

**Wednesday - Content Creation:**
```bash
# Create blog post about anxiety
python request_blog_post.py \
  --topic "Anxiety Coping Strategies" \
  --keywords "anxiety relief, coping strategies"

# Create social posts
python request_social_post.py --topic "Quick anxiety relief technique"
```

**Sunday Evening - Performance Review:**
```python
# Analyze what worked
python analyze_marketing_roi.py \
  --business-data weekly_data.json \
  --content-data content_performance.json
```

**Output**: ROI calculation, recommendations for next week

---

### Example 2: Monthly Strategic Planning

**First Monday of Month:**
```bash
# Comprehensive business analysis
python analyze_practice_data.py --file monthly_data.json

# Market research
python research_local_market.py --location "Austin, TX"

# Content strategy for next month
python plan_monthly_content.py --based-on business_insights.json
```

---

## 📊 What You Can Do Now

### Social Media Content:
- ✅ Request Instagram posts on-demand
- ✅ Create Facebook announcements
- ✅ Generate LinkedIn thought-leadership
- ✅ Write 2500-word SEO-optimized blog posts
- ✅ Plan weekly content calendars
- ✅ Handle crisis situations professionally
- ✅ Batch create content for the week

### Business Intelligence:
- ✅ Analyze weekly practice performance
- ✅ Track monthly trends and KPIs
- ✅ Calculate marketing ROI
- ✅ Research local market opportunities
- ✅ Identify which services need more marketing
- ✅ Optimize therapist scheduling
- ✅ Forecast revenue and capacity needs
- ✅ Track referral sources

---

## 🛠️ Available Scripts

### Social Media Scripts:
- `request_social_post.py` - Generate social media posts
- `request_blog_post.py` - Create SEO-optimized blogs
- `request_weekly_strategy.py` - Plan weekly content
- `batch_create_posts.py` - Batch create multiple posts

### Business Intelligence Scripts:
- `analyze_practice_data.py` - Analyze business metrics
- `analyze_marketing_roi.py` - Track content ROI
- `research_local_market.py` - Market research
- `optimize_operations.py` - Scheduling optimization

### Data Management:
- `collect_weekly_data.py` - Automated data collection
- `convert_exports.py` - Convert CSV to JSON
- `generate_dashboard.py` - Create integrated dashboard

---

## 📖 Documentation Structure

```
therapy-practice-project/
├── HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md  ← Social media guide
├── HOW_TO_USE_BUSINESS_AGENTS.md      ← Business intelligence guide
├── CONTENT_CREATION_GUIDE.md          ← Content standards
├── request_social_post.py              ← Social post script (ready to use)
├── analyze_practice_data.py            ← Business analysis script
└── data_templates/
    ├── README.md                       ← Data template guide
    ├── weekly_practice_data.json       ← Weekly template
    └── monthly_practice_data.json      ← Monthly template
```

---

## 🎓 Learning Path

### Week 1: Social Media
**Day 1-2**: Read social media guide
**Day 3**: Request first Instagram post
**Day 4**: Create first blog post
**Day 5**: Plan weekly content calendar

### Week 2: Business Intelligence
**Day 1-2**: Read business intelligence guide
**Day 3**: Set up data templates
**Day 4**: Run first analysis with sample data
**Day 5**: Analyze your real practice data

### Week 3: Integration
**Day 1**: Complete Monday business analysis
**Day 2**: Use insights for content strategy
**Day 3-5**: Create content based on insights
**Day 6**: Review performance
**Day 7**: Plan next week

### Week 4: Optimization
**Day 1**: Refine data collection process
**Day 2**: Optimize content workflow
**Day 3**: Track ROI metrics
**Day 4**: Adjust strategy based on results
**Day 5**: Automate repetitive tasks

---

## ⚡ Quick Reference

### Social Media Post Request:
```bash
python request_social_post.py --topic "your topic" --use-api
```

### Blog Post Request:
```python
python request_blog_post.py \
  --topic "Anxiety Coping Strategies" \
  --keywords "anxiety relief" \
  --use-api
```

### Business Analysis:
```bash
python analyze_practice_data.py --file weekly_data.json
```

### Marketing ROI:
```bash
python analyze_marketing_roi.py \
  --business weekly_data.json \
  --content content_performance.json
```

---

## 🎯 Success Metrics

After using these guides for 1 month, you should see:

**Content Creation**:
- ✅ 4-8 blog posts published
- ✅ 20-30 social media posts
- ✅ Consistent posting schedule
- ✅ Growing social media engagement

**Business Intelligence**:
- ✅ Weekly performance reviews completed
- ✅ Clear trends identified
- ✅ Data-driven decisions
- ✅ Improved practice metrics

**Integration**:
- ✅ Content aligned with business goals
- ✅ Measurable ROI from content
- ✅ Clear attribution (content → clients)
- ✅ Optimized service offerings

---

## 📞 Support

**Guides**:
- [HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md](therapy-practice-project/HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md)
- [HOW_TO_USE_BUSINESS_AGENTS.md](therapy-practice-project/HOW_TO_USE_BUSINESS_AGENTS.md)
- [data_templates/README.md](therapy-practice-project/data_templates/README.md)

**Scripts**:
- [request_social_post.py](therapy-practice-project/request_social_post.py)
- analyze_practice_data.py (referenced in guide)

**Other Documentation**:
- [CONTENT_CREATION_GUIDE.md](therapy-practice-project/CONTENT_CREATION_GUIDE.md)
- [therapy-practice-project/README.md](therapy-practice-project/README.md)
- [THERAPY_PRACTICE_COMPLETE_GUIDE.md](THERAPY_PRACTICE_COMPLETE_GUIDE.md)

---

## ✨ Summary

You now have **complete how-to guides** for:

- ✅ **Social Media Agents** - Request posts, blogs, strategy
- ✅ **Business Intelligence Agents** - Upload data, get insights
- ✅ **Data Templates** - Format your practice data correctly
- ✅ **Integration Workflows** - Connect business data to content

**Everything you need to start using your therapy practice management system!**

---

**Start today:**
```bash
# Social media
cd therapy-practice-project
python request_social_post.py --topic "Mental health tip" --use-api

# Business intelligence
python analyze_practice_data.py --sample
```

**Files Created**:
- [HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md](therapy-practice-project/HOW_TO_USE_SOCIAL_MEDIA_AGENTS.md) ✅
- [HOW_TO_USE_BUSINESS_AGENTS.md](therapy-practice-project/HOW_TO_USE_BUSINESS_AGENTS.md) ✅
- [data_templates/](therapy-practice-project/data_templates/) ✅
  - weekly_practice_data.json ✅
  - monthly_practice_data.json ✅
  - README.md ✅
- [HOW_TO_GUIDES_SUMMARY.md](HOW_TO_GUIDES_SUMMARY.md) ✅ (this file)
