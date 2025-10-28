#!/usr/bin/env python3
"""
Content Creation Workflow Example
Demonstrates using all 4 agents in a complete content creation pipeline
"""

import sys
from pathlib import Path
import importlib.util

# Add framework to path
FRAMEWORK_DIR = Path(__file__).parent.parent / "Claude-Agents"

# Load modules dynamically (handles hyphenated filenames)
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load core modules
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine


def main():
    """
    Complete content creation workflow example.

    This demonstrates how to:
    1. Load all 4 content creation agents
    2. Generate prompts for each stage
    3. Chain agents together for complete workflow
    """

    print("="*80)
    print("CONTENT CREATION WORKFLOW EXAMPLE")
    print("="*80)

    # Initialize managers
    agents_dir = Path(__file__).parent / "agents"
    manager = AgentManager(agents_dir=str(agents_dir))
    engine = PromptEngine()

    # Load all agents
    print("\n📋 Loading agents...")
    strategist = manager.load_agent("content-creation-content-strategist")
    writer = manager.load_agent("content-creation-content-writer")
    editor = manager.load_agent("content-creation-content-editor")
    seo = manager.load_agent("content-creation-seo-specialist")

    print(f"✓ Loaded Content Strategist")
    print(f"✓ Loaded Content Writer")
    print(f"✓ Loaded Content Editor")
    print(f"✓ Loaded SEO Specialist")

    # Example content topic
    TOPIC = "The Future of AI-Powered Development Tools"
    TARGET_AUDIENCE = "Software developers and tech enthusiasts"

    print("\n" + "="*80)
    print(f"CREATING CONTENT: {TOPIC}")
    print(f"TARGET AUDIENCE: {TARGET_AUDIENCE}")
    print("="*80)

    # STEP 1: Content Strategy
    print("\n\n" + "="*80)
    print("STEP 1: CONTENT STRATEGY & PLANNING")
    print("="*80 + "\n")

    strategy_task = f"""
    Create a comprehensive content strategy for an article about "{TOPIC}".

    Target Audience: {TARGET_AUDIENCE}

    Please provide:
    1. Key themes and angles to explore
    2. Content structure (sections/headings)
    3. Audience pain points to address
    4. Value proposition (why should they read this?)
    5. Call-to-action suggestions
    6. Content promotion strategy
    """

    strategy_prompt = engine.generate_prompt(
        context=strategist.context,
        model=strategist.model,
        tools=strategist.tools,
        task=strategy_task
    )

    print("Strategy Prompt Generated:")
    print("-" * 80)
    print(strategy_prompt[:500] + "...\n[truncated for display]")
    print("-" * 80)
    print(f"Full prompt length: {len(strategy_prompt)} characters")
    print("\n💡 Next: Use this prompt with Claude API to get content strategy")
    print("   Example: anthropic.messages.create(model='claude-sonnet-4', messages=[...])")

    # STEP 2: SEO Research
    print("\n\n" + "="*80)
    print("STEP 2: SEO RESEARCH & KEYWORD ANALYSIS")
    print("="*80 + "\n")

    seo_task = f"""
    Perform comprehensive SEO research for an article about "{TOPIC}".

    Target Audience: {TARGET_AUDIENCE}

    Provide:
    1. Primary keyword (main target)
    2. 5-10 secondary keywords
    3. Long-tail keyword opportunities
    4. Search intent analysis
    5. Competitor content analysis
    6. Content gap opportunities
    7. Recommended internal/external linking strategy
    """

    seo_prompt = engine.generate_prompt(
        context=seo.context,
        model=seo.model,
        tools=seo.tools,
        task=seo_task
    )

    print("SEO Research Prompt Generated:")
    print("-" * 80)
    print(seo_prompt[:500] + "...\n[truncated for display]")
    print("-" * 80)
    print(f"Full prompt length: {len(seo_prompt)} characters")
    print("\n💡 Next: Use this prompt with Claude API to get keyword research")

    # STEP 3: Content Writing
    print("\n\n" + "="*80)
    print("STEP 3: CONTENT CREATION")
    print("="*80 + "\n")

    writing_task = f"""
    Write a comprehensive 2000-word article about "{TOPIC}".

    Target Audience: {TARGET_AUDIENCE}

    Requirements:
    - Word Count: ~2000 words
    - Tone: Professional but conversational
    - Include: Code examples (if relevant), practical tips, real-world examples
    - Structure: Introduction, 4-5 main sections, conclusion
    - SEO: Naturally incorporate keywords (will be provided from SEO research)
    - Format: Markdown with proper headings, lists, code blocks

    Content should:
    1. Hook readers in the introduction
    2. Provide actionable insights
    3. Include specific examples and use cases
    4. Address common pain points
    5. End with clear call-to-action
    """

    writing_prompt = engine.generate_prompt(
        context=writer.context,
        model=writer.model,
        tools=writer.tools,
        task=writing_task
    )

    print("Writing Prompt Generated:")
    print("-" * 80)
    print(writing_prompt[:500] + "...\n[truncated for display]")
    print("-" * 80)
    print(f"Full prompt length: {len(writing_prompt)} characters")
    print("\n💡 Next: Use this prompt with Claude API to generate content draft")

    # STEP 4: Content Editing
    print("\n\n" + "="*80)
    print("STEP 4: CONTENT REVIEW & EDITING")
    print("="*80 + "\n")

    editing_task = f"""
    Review and edit the content draft for the article about "{TOPIC}".

    [NOTE: In production, you would include the actual content draft here]

    Review Checklist:
    1. Grammar & Spelling: Check for errors
    2. Clarity: Ensure ideas are clearly expressed
    3. Readability: Target 8th-9th grade reading level
    4. Structure: Verify logical flow and organization
    5. Accuracy: Fact-check claims and statistics
    6. SEO: Verify keyword usage is natural
    7. Style: Check consistency with brand voice
    8. Engagement: Assess hook, examples, and CTA
    9. Length: Verify meets ~2000 word target
    10. Plagiarism: Flag any potential issues

    Provide:
    - Detailed feedback on each area
    - Specific edits with line-by-line changes
    - Overall quality score (1-10)
    - Recommendations for improvement
    """

    editing_prompt = engine.generate_prompt(
        context=editor.context,
        model=editor.model,
        tools=editor.tools,
        task=editing_task
    )

    print("Editing Prompt Generated:")
    print("-" * 80)
    print(editing_prompt[:500] + "...\n[truncated for display]")
    print("-" * 80)
    print(f"Full prompt length: {len(editing_prompt)} characters")
    print("\n💡 Next: Use this prompt with Claude API to review and refine content")

    # Summary
    print("\n\n" + "="*80)
    print("WORKFLOW SUMMARY")
    print("="*80 + "\n")

    print("✅ Generated 4 specialized prompts for complete content workflow:")
    print(f"   1. Strategy Prompt:  {len(strategy_prompt):,} chars")
    print(f"   2. SEO Prompt:       {len(seo_prompt):,} chars")
    print(f"   3. Writing Prompt:   {len(writing_prompt):,} chars")
    print(f"   4. Editing Prompt:   {len(editing_prompt):,} chars")
    print(f"\n   Total:               {len(strategy_prompt) + len(seo_prompt) + len(writing_prompt) + len(editing_prompt):,} chars")

    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80 + "\n")

    print("To use these prompts in production:")
    print("""
1. Set up Claude API client:

   import anthropic

   client = anthropic.Anthropic(api_key="your-api-key")

2. Use each prompt in sequence:

   # Step 1: Strategy
   strategy_response = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=6000,
       temperature=0.4,
       messages=[{"role": "user", "content": strategy_prompt}]
   )
   strategy_result = strategy_response.content[0].text

   # Step 2: SEO Research
   seo_response = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=5000,
       temperature=0.3,
       messages=[{"role": "user", "content": seo_prompt}]
   )
   seo_result = seo_response.content[0].text

   # Step 3: Content Writing (include SEO keywords)
   enhanced_writing_prompt = writing_prompt + f"\\n\\nSEO Keywords to include:\\n{seo_result}"
   content_response = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=8000,
       temperature=0.7,
       messages=[{"role": "user", "content": enhanced_writing_prompt}]
   )
   content_draft = content_response.content[0].text

   # Step 4: Content Editing (include actual draft)
   enhanced_editing_prompt = editing_prompt.replace(
       "[NOTE: In production, you would include the actual content draft here]",
       f"CONTENT DRAFT:\\n\\n{content_draft}"
   )
   editing_response = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=6000,
       temperature=0.2,
       messages=[{"role": "user", "content": enhanced_editing_prompt}]
   )
   final_content = editing_response.content[0].text

3. Save and publish your final content!
""")

    print("\n" + "="*80)
    print("✨ Example workflow complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
