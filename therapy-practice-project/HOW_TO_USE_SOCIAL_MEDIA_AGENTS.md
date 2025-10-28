# How to Use Social Media Content Agents

## Overview

This guide shows you exactly how to interact with your **3 social media content agents** to create blog posts, social media content, and manage your online presence.

---

## Your 3 Social Media Content Agents

### 1. Content Strategist
**Role**: Plans content strategy based on business data

**What it does**:
- Conducts SEO keyword research
- Plans blog content calendar
- Creates social media content calendar
- Maps business goals to content topics
- Develops content clusters

### 2. Content Creator
**Role**: Creates blog posts and social media content

**What it does**:
- Writes 1500-3000 word SEO-optimized blog posts
- Creates Instagram posts (150-250 words)
- Creates Facebook posts (100-250 words)
- Creates LinkedIn posts (200-400 words)
- Generates hashtags and CTAs

### 3. Social Media Manager
**Role**: Schedules, publishes, and engages

**What it does**:
- Schedules posts for optimal times
- Monitors engagement and comments
- Responds to community inquiries
- Tracks performance metrics
- Manages crisis situations

---

## 📝 How to Request Content

### Method 1: Quick Social Media Post (Easiest)

**Use the provided script:**

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"

# Request an Instagram post
python request_social_post.py \
  --topic "5 signs you might benefit from therapy" \
  --platform Instagram
```

**With Claude API (auto-generates):**
```bash
export ANTHROPIC_API_KEY="your-key"

python request_social_post.py \
  --topic "Anxiety coping strategies for work stress" \
  --platform Instagram \
  --use-api
```

**Available platforms:** Instagram, Facebook, LinkedIn

**Available content types:** educational, announcement, tip, testimonial

---

### Method 2: Blog Post Creation

**Step 1: Create Python script**

```python
#!/usr/bin/env python3
"""Request a blog post from content creator"""

import sys
from pathlib import Path
import importlib.util
import anthropic
import os

# Setup
FRAMEWORK_DIR = Path(__file__).parent.parent / "Claude-Agents"

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine

# Initialize
agents_dir = Path(__file__).parent / "agents"
manager = AgentManager(agents_dir=str(agents_dir))
engine = PromptEngine()

# Load content creator
creator = manager.load_agent("therapy-practice-content-creator")

# Request blog post
blog_task = """
Create a comprehensive blog post about anxiety coping strategies.

**Blog Specifications:**
- Primary Keyword: "anxiety coping strategies"
- Secondary Keywords: "how to deal with anxiety", "anxiety relief techniques"
- Word Count: 2,500 words
- Target Audience: Adults experiencing anxiety, considering therapy
- Business Goal: Attract anxiety therapy clients

**Content Requirements:**
- Evidence-based strategies (cite research)
- 10 specific coping techniques
- Real-world application examples
- Professional but approachable tone
- Include section on when to seek therapy
- Strong call-to-action to book consultation

**SEO Requirements:**
- Proper heading structure (H1, H2, H3)
- Primary keyword in title, first 100 words, and 2+ H2 headings
- 2-3 internal links to anxiety therapy service page
- External links to credible sources (APA, NIMH)
- Meta description (150-160 characters)
"""

# Generate prompt
prompt = engine.generate_prompt(
    context=creator.context,
    model=creator.model,
    tools=creator.tools,
    task=blog_task
)

# Use with Claude API
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8000,
    temperature=0.6,
    messages=[{"role": "user", "content": prompt}]
)

blog_post = response.content[0].text

# Save to file
with open("blog_anxiety_coping_strategies.md", "w") as f:
    f.write(blog_post)

print("✓ Blog post saved to blog_anxiety_coping_strategies.md")
```

**Run it:**
```bash
python create_blog_post.py
```

---

### Method 3: Weekly Content Planning

**Request complete week's content:**

```python
#!/usr/bin/env python3
"""Request weekly content calendar"""

import sys
from pathlib import Path
import importlib.util
import anthropic
import os

# [Same setup as above]

# Load content strategist
strategist = manager.load_agent("therapy-practice-content-strategist")

# Request weekly strategy
strategy_task = """
Create this week's content strategy based on our practice priorities.

**Business Context:**
- Anxiety therapy has 2-week waitlist (high demand)
- Couples therapy at 65% capacity (need to fill slots)
- New EMDR therapist joined last month (promote service)

**Create:**
1. **Weekly Content Themes**: What topics align with business goals
2. **Blog Post Recommendation**: 1 long-form post (what topic, keywords)
3. **Social Media Calendar**: 5-7 posts for this week
   - Which platforms (Instagram, Facebook, LinkedIn)
   - What topics for each day
   - How they connect to blog post
4. **SEO Keywords**: Target keywords for blog and social
5. **Business Alignment**: How content supports filling couples therapy slots

**Output:**
Detailed content calendar with post-by-post breakdown ready to execute.
"""

# Generate and use
prompt = engine.generate_prompt(
    context=strategist.context,
    model=strategist.model,
    tools=strategist.tools,
    task=strategy_task
)

# Call Claude API
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=7000,
    temperature=0.4,
    messages=[{"role": "user", "content": prompt}]
)

weekly_strategy = response.content[0].text

# Save
with open("weekly_content_strategy.md", "w") as f:
    f.write(weekly_strategy)

print("✓ Weekly strategy saved")
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Social Media Post

**Goal**: Post educational content about mental health

**Agent**: Content Creator

**Request**:
```bash
python request_social_post.py \
  --topic "Progressive muscle relaxation for anxiety" \
  --platform Instagram \
  --type educational \
  --use-api
```

**What you get**:
- Instagram post (150-250 words)
- 5-10 relevant hashtags
- Visual content suggestion
- Call-to-action
- Best posting time

---

### Use Case 2: Weekly Blog Post

**Goal**: Create SEO-optimized blog to attract clients

**Agent**: Content Creator

**Process**:
1. Identify topic from business data (e.g., "anxiety therapy high demand")
2. Request blog post with SEO focus
3. Receive 2,500-word optimized post
4. Publish to website
5. Promote via social media

**Code Example**: See "Method 2" above

---

### Use Case 3: Content Strategy Planning

**Goal**: Plan next month's content

**Agent**: Content Strategist

**Request**:
```python
strategy_task = """
Create content strategy for next month.

**Business Priorities:**
- Fill 10 weekly couples therapy slots
- Establish EMDR expertise in local area
- Maintain anxiety therapy waitlist momentum

**Provide:**
1. 4 blog post topics (with keywords)
2. Social media themes for each week
3. Content cluster strategy
4. SEO keyword targets
5. Expected outcomes (traffic, inquiries)
"""
```

---

### Use Case 4: Crisis Response

**Goal**: Respond to sensitive comment on social media

**Agent**: Social Media Manager

**Request**:
```python
crisis_task = """
A follower commented: "I've been feeling really hopeless lately and
don't know what to do."

**Respond with:**
1. Immediate crisis resources (988, local crisis center)
2. Compassionate but professional tone
3. NO therapy advice via comments
4. Invitation to DM or call practice
5. Follow-up protocol recommendation

**Output:**
- Public comment response
- DM message template
- Internal action steps
"""
```

---

## 📊 Agent Interaction Patterns

### Pattern 1: Business Data → Content Strategy → Creation → Publishing

```
STEP 1: Provide business context to Content Strategist
└─ "Anxiety therapy has waitlist, couples therapy needs clients"

STEP 2: Strategist plans content
└─ "Create anxiety blog, promote couples therapy on social"

STEP 3: Content Creator writes
└─ Blog post + 5 social posts

STEP 4: Social Media Manager publishes
└─ Schedule and post content
```

### Pattern 2: One-Off Social Post

```
STEP 1: Decide topic
└─ "Post about grounding technique"

STEP 2: Request from Content Creator
└─ Use request_social_post.py script

STEP 3: Review and publish
└─ Copy to social media platform
```

### Pattern 3: Monthly Content Planning

```
STEP 1: Review business metrics
└─ What services need more clients?

STEP 2: Content Strategist creates calendar
└─ 4 blog posts + 20-30 social posts

STEP 3: Batch create content
└─ Content Creator writes all posts

STEP 4: Schedule publishing
└─ Social Media Manager schedules all
```

---

## 💬 Example Conversations with Agents

### Conversation 1: Request Instagram Post

**You → Content Creator:**
```
Create an Instagram post about the 5-4-3-2-1 grounding technique for anxiety.

Include:
- Brief explanation of the technique
- How it helps with anxiety
- Encourage followers to try it
- CTA for anxiety therapy services
- 8 relevant hashtags
```

**Content Creator → You:**
```
Feeling anxious? Try the 5-4-3-2-1 grounding technique 🌿

When anxiety strikes, this simple exercise brings you back to
the present:

5️⃣ Name 5 things you can SEE
4️⃣ Name 4 things you can TOUCH
3️⃣ Name 3 things you can HEAR
2️⃣ Name 2 things you can SMELL
1️⃣ Name 1 thing you can TASTE

This technique works by engaging your senses and interrupting
the anxiety spiral. Try it next time you feel overwhelmed.

Save this post for when you need it 💙

If anxiety is significantly impacting your daily life, therapy
can help. DM us to learn more about our anxiety therapy services.

#anxietyrelief #mentalhealthtips #therapistsofinstagram
#anxietysupport #copingskills #mindfulness #therapytools
#austintherapy
```

---

### Conversation 2: Request Blog Post

**You → Content Creator:**
```
Write a 2,500-word blog post:
- Title: "10 Evidence-Based Anxiety Coping Strategies"
- Primary keyword: anxiety coping strategies
- Include scientific research citations
- Target: adults with anxiety
- Goal: attract anxiety therapy clients
- SEO optimized with proper structure
```

**Content Creator → You:**
```
[Receives complete 2,500-word blog post with:]
- SEO-optimized title and meta description
- Proper H1, H2, H3 structure
- 10 evidence-based strategies with research citations
- Internal links to anxiety therapy services
- External links to APA, NIMH sources
- Call-to-action for booking consultation
- Reading time: ~12 minutes
- Target keyword density: 1.5%
```

---

### Conversation 3: Crisis Response

**You → Social Media Manager:**
```
Someone commented on our post: "I don't think I can do this anymore"

This seems like a crisis situation. What should we do?
```

**Social Media Manager → You:**
```
IMMEDIATE ACTIONS:

1. PUBLIC COMMENT (post within 5 minutes):
"Thank you for reaching out. If you're in crisis, please contact:
• 988 Suicide & Crisis Lifeline (call or text)
• 911 for immediate emergencies
• [Local Crisis Center]: [phone number]

We care about your safety. Please reach out to these resources
right away. 💙"

2. DIRECT MESSAGE (send immediately):
"We're concerned about your comment. Please reach out to crisis
support immediately:
• 988 Lifeline: Available 24/7
• Local crisis center: [details]

Our practice can help with ongoing support, but immediate crisis
situations require immediate professional intervention. Please
call one of these resources now.

You matter, and help is available. ❤️"

3. INTERNAL ACTION:
• Document interaction (time, comment, response)
• Monitor for follow-up comments
• If no response in 24 hours and serious concern, consider
  consulting practice's crisis protocol
• Do NOT attempt to provide therapy via social media

4. FOLLOW-UP PROTOCOL:
• Check back in 48 hours to see if they engaged with crisis resources
• If they respond positively, offer practice consultation
• Maintain professional boundaries throughout
```

---

## 🛠️ Technical Setup

### Prerequisites

```bash
# 1. Python 3.8+
python --version

# 2. Install Claude API package
pip install anthropic

# 3. Set API key
export ANTHROPIC_API_KEY="your-api-key"

# 4. Verify agents exist
cd /Users/Coding\ Projects/Claude_Agents_Meta/therapy-practice-project
ls -la agents/
```

### Test Your Setup

```bash
# Test that agents load correctly
cd /Users/Coding\ Projects/Claude_Agents_Meta/therapy-practice-project

python -c "
import sys
sys.path.insert(0, '../Claude-Agents/core')
from pathlib import Path
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

am = load_module('agent_manager', '../Claude-Agents/core/agent-manager.py')
manager = am.AgentManager(agents_dir='agents')
creator = manager.load_agent('therapy-practice-content-creator')
print(f'✓ Loaded: {creator.context[\"role\"]}')
"
```

---

## 📋 Quick Reference Commands

### Daily Social Media Post
```bash
python request_social_post.py --topic "your topic" --use-api
```

### Weekly Content Strategy
```bash
python request_weekly_strategy.py --use-api
```

### Blog Post Creation
```bash
python request_blog_post.py --topic "your topic" --keywords "primary keyword" --use-api
```

### Batch Create Social Posts
```bash
python batch_create_posts.py --count 7 --theme "anxiety awareness" --use-api
```

---

## ❓ Troubleshooting

### Problem: "Agent not found"

**Solution:**
```bash
# Check agent name
ls therapy-practice-project/agents/

# Correct name is:
therapy-practice-content-creator
therapy-practice-content-strategist
therapy-practice-social-media-manager
```

### Problem: "Module not found"

**Solution:**
```python
# Use dynamic module loading for hyphenated filenames
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

### Problem: "API key not set"

**Solution:**
```bash
# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Or in Python
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
```

### Problem: Generated content doesn't match expectations

**Solution:**
Provide more specific instructions in your task:
```python
task = """
Create Instagram post about anxiety.

SPECIFIC REQUIREMENTS:
- Tone: Warm but professional (not casual or overly formal)
- Length: Exactly 200 words
- Hashtags: Include #austintherapy for local SEO
- CTA: "Book free consultation" (not just "DM us")
- Visual: Suggest calming nature image (not person photo)
- Crisis resources: Include if discussing severe anxiety
"""
```

---

## 🎯 Best Practices

### DO:
- ✅ Provide clear business context to strategist
- ✅ Be specific about target audience
- ✅ Include keywords for SEO-focused content
- ✅ Review generated content before publishing
- ✅ Track performance and adjust strategy
- ✅ Respond to comments within 24 hours

### DON'T:
- ❌ Request content without business context
- ❌ Publish without reviewing for accuracy
- ❌ Ignore crisis comments on social media
- ❌ Post without including call-to-action
- ❌ Forget to track which content drives inquiries
- ❌ Use the same hashtags for every post

---

## 📞 Support

**Documentation:**
- [request_social_post.py](./request_social_post.py) - Social post script
- [CONTENT_CREATION_GUIDE.md](./CONTENT_CREATION_GUIDE.md) - Content standards
- [/blog-post slash command](../Claude-Agents/slash-commands/blog-post.md)
- [/seo-research slash command](../Claude-Agents/slash-commands/seo-research.md)

**Agent Configurations:**
- [content-creator/config.yaml](./agents/therapy-practice-content-creator/config.yaml)
- [content-strategist/config.yaml](./agents/therapy-practice-content-strategist/config.yaml)
- [social-media-manager/config.yaml](./agents/therapy-practice-social-media-manager/config.yaml)

---

## 🎉 You're Ready!

You now know how to:
- ✅ Request social media posts
- ✅ Create blog content
- ✅ Plan content strategy
- ✅ Handle crisis situations
- ✅ Interact with all 3 social media agents

**Start creating content today!**

```bash
cd /Users/Coding\ Projects/Claude_Agents_Meta/therapy-practice-project

python request_social_post.py --topic "Quick stress relief technique" --use-api
```
