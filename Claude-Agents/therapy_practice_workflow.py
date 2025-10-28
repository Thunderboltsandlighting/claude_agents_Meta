#!/usr/bin/env python3
"""
Therapy Practice Weekly Workflow Orchestration
Automates the Monday → Sunday business intelligence + content management cycle
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import importlib.util
import json


# Load modules dynamically
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Setup paths
FRAMEWORK_DIR = Path(__file__).parent
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine


class TherapyPracticeWorkflow:
    """
    Orchestrates the complete weekly workflow for therapy practice management.

    Weekly Cycle:
    - Monday: Business intelligence analysis
    - Tuesday: Content strategy development
    - Wednesday-Friday: Content creation & publishing
    - Sunday: Performance review & optimization
    """

    def __init__(self, agents_dir: str):
        """Initialize workflow with agents directory."""
        self.manager = AgentManager(agents_dir=agents_dir)
        self.engine = PromptEngine()
        self.agents = {}

        # Load all agents
        self._load_agents()

    def _load_agents(self):
        """Load all 7 therapy practice agents."""
        agent_names = [
            'therapy-practice-business-analyst',
            'therapy-practice-content-strategist',
            'therapy-practice-content-creator',
            'therapy-practice-social-media-manager',
            'therapy-practice-marketing-analytics',
            'therapy-practice-market-research',
            'therapy-practice-practice-operations'
        ]

        for name in agent_names:
            agent = self.manager.load_agent(name)
            if agent:
                short_name = name.replace('therapy-practice-', '')
                self.agents[short_name] = agent
                print(f"✓ Loaded {short_name}")
            else:
                print(f"✗ Failed to load {name}")

    def monday_business_intelligence(self, weekly_data: Dict) -> Dict:
        """
        Monday: Business Intelligence Analysis

        Analyzes practice data and identifies trends, opportunities, and issues.

        Args:
            weekly_data: Dict containing practice metrics (revenue, clients, utilization, etc.)

        Returns:
            Dict with business insights and content opportunities
        """
        print("\n" + "="*80)
        print("MONDAY: BUSINESS INTELLIGENCE ANALYSIS")
        print("="*80 + "\n")

        agent = self.agents.get('business-analyst')
        if not agent:
            print("❌ Business analyst agent not loaded")
            return {}

        # Financial analysis task
        financial_task = f"""
        Analyze weekly practice performance data:

        {json.dumps(weekly_data, indent=2)}

        Provide:
        1. **Financial Summary**: Revenue, expenses, profitability
        2. **Client Metrics**: New clients, retention rate, cancellations
        3. **Utilization Analysis**: Therapist schedule efficiency
        4. **Service Demand**: Which therapy types are most requested
        5. **Trends**: Week-over-week changes and patterns
        6. **Content Opportunities**: Topics that could address identified needs
        7. **Business Recommendations**: Actions to improve performance

        Format: Structured report with executive summary + detailed analysis
        """

        prompt = self.engine.generate_prompt(
            context=agent.context,
            model=agent.model,
            tools=agent.tools,
            task=financial_task
        )

        print("Generated Business Analysis Prompt:")
        print(f"  • Length: {len(prompt):,} characters")
        print(f"  • Task: Weekly practice performance analysis")
        print(f"\n💡 Use this prompt with Claude API to get business insights")

        return {
            'prompt': prompt,
            'task_type': 'business_intelligence',
            'next_step': 'Use insights for Tuesday content strategy'
        }

    def tuesday_content_strategy(self, business_insights: str) -> Dict:
        """
        Tuesday: Content Strategy Development

        Creates data-driven content strategy based on Monday's business insights.

        Args:
            business_insights: Results from Monday's business analysis

        Returns:
            Dict with content strategy and calendar
        """
        print("\n" + "="*80)
        print("TUESDAY: CONTENT STRATEGY DEVELOPMENT")
        print("="*80 + "\n")

        agent = self.agents.get('content-strategist')
        if not agent:
            print("❌ Content strategist agent not loaded")
            return {}

        strategy_task = f"""
        Develop this week's content strategy based on practice business insights:

        BUSINESS INSIGHTS:
        {business_insights}

        Create:
        1. **Weekly Content Themes**: Topics aligned with practice needs
        2. **Content Calendar**: 5-7 posts for this week (Wed-Sun)
        3. **Target Audience**: Who we're trying to reach with each post
        4. **Business Goals**: How content supports practice growth
        5. **Platform Strategy**: Which content for Instagram vs Facebook vs LinkedIn
        6. **Engagement Plan**: How we'll interact with community

        Constraints:
        - HIPAA compliant (no client information)
        - Professional and empathetic tone
        - Evidence-based mental health information
        - APA ethical guidelines

        Format: Weekly content plan with post-by-post breakdown
        """

        prompt = self.engine.generate_prompt(
            context=agent.context,
            model=agent.model,
            tools=agent.tools,
            task=strategy_task
        )

        print("Generated Content Strategy Prompt:")
        print(f"  • Length: {len(prompt):,} characters")
        print(f"  • Task: Data-driven content planning")
        print(f"\n💡 Use this prompt with Claude API to get content strategy")

        return {
            'prompt': prompt,
            'task_type': 'content_strategy',
            'next_step': 'Use strategy for Wed-Fri content creation'
        }

    def wednesday_friday_content_creation(self, content_strategy: str) -> List[Dict]:
        """
        Wednesday-Friday: Content Creation & Publishing

        Creates individual posts based on Tuesday's strategy.

        Args:
            content_strategy: Results from Tuesday's strategy session

        Returns:
            List of Dicts with prompts for each day's content
        """
        print("\n" + "="*80)
        print("WEDNESDAY-FRIDAY: CONTENT CREATION & PUBLISHING")
        print("="*80 + "\n")

        creator = self.agents.get('content-creator')
        social_manager = self.agents.get('social-media-manager')

        if not creator or not social_manager:
            print("❌ Required agents not loaded")
            return []

        # Generate prompts for 5 posts (Wed-Sun)
        days = ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        post_prompts = []

        for day in days:
            creation_task = f"""
            Create social media content for {day} based on this week's strategy:

            CONTENT STRATEGY:
            {content_strategy}

            Create post for {day}:
            1. **Post Text**: Engaging caption (150-300 words)
            2. **Hashtags**: 5-10 relevant, professional hashtags
            3. **Image Suggestion**: Description of visual that would accompany post
            4. **Call-to-Action**: What do we want audience to do?
            5. **Platform Optimization**: Any platform-specific adjustments

            Guidelines:
            - HIPAA compliant
            - Professional yet warm tone
            - Evidence-based information
            - Include relevant resources (988, crisis hotlines when appropriate)
            - Avoid diagnosis or treatment advice

            Format: Ready-to-publish social media post
            """

            prompt = self.engine.generate_prompt(
                context=creator.context,
                model=creator.model,
                tools=creator.tools,
                task=creation_task
            )

            post_prompts.append({
                'day': day,
                'prompt': prompt,
                'length': len(prompt),
                'task_type': 'content_creation'
            })

            print(f"✓ Generated {day} content creation prompt ({len(prompt):,} chars)")

        print(f"\n💡 Created {len(post_prompts)} post prompts for the week")
        print(f"   Use with Claude API to generate actual post content")

        return post_prompts

    def sunday_performance_review(self, weekly_metrics: Dict) -> Dict:
        """
        Sunday: Performance Review & Optimization

        Analyzes content performance and correlates with business outcomes.

        Args:
            weekly_metrics: Dict with content performance + business results

        Returns:
            Dict with performance analysis and recommendations
        """
        print("\n" + "="*80)
        print("SUNDAY: PERFORMANCE REVIEW & OPTIMIZATION")
        print("="*80 + "\n")

        analytics = self.agents.get('marketing-analytics')
        if not analytics:
            print("❌ Marketing analytics agent not loaded")
            return {}

        review_task = f"""
        Analyze this week's integrated performance (content + business):

        WEEKLY METRICS:
        {json.dumps(weekly_metrics, indent=2)}

        Provide:
        1. **Content Performance Summary**:
           - Post engagement rates
           - Reach and impressions
           - Best/worst performing content

        2. **Business Impact Analysis**:
           - New inquiries from social media
           - Conversion rate (inquiry → booking)
           - Revenue attributed to content marketing

        3. **Correlation Analysis**:
           - Which content types drive most inquiries?
           - Which days/times get best engagement?
           - Which topics resonate most with audience?

        4. **ROI Calculation**:
           - Content creation time/cost vs new client revenue
           - Marketing efficiency metrics

        5. **Recommendations for Next Week**:
           - Content topics to double down on
           - Posting times to adjust
           - New content formats to try
           - Business opportunities identified

        Format: Executive summary + detailed analytics report
        """

        prompt = self.engine.generate_prompt(
            context=analytics.context,
            model=analytics.model,
            tools=analytics.tools,
            task=review_task
        )

        print("Generated Performance Review Prompt:")
        print(f"  • Length: {len(prompt):,} characters")
        print(f"  • Task: Integrated performance analysis")
        print(f"\n💡 Use this prompt with Claude API to get performance insights")

        return {
            'prompt': prompt,
            'task_type': 'performance_review',
            'next_step': 'Apply insights to next Monday\'s analysis'
        }

    def run_full_week_simulation(self):
        """
        Simulate a complete weekly workflow.

        Demonstrates how all agents work together through the week.
        """
        print("\n" + "="*80)
        print("THERAPY PRACTICE WEEKLY WORKFLOW SIMULATION")
        print("="*80)
        print("\nThis simulation demonstrates the complete weekly cycle:")
        print("  Monday → Business Intelligence")
        print("  Tuesday → Content Strategy")
        print("  Wednesday-Friday → Content Creation")
        print("  Sunday → Performance Review")
        print("\n" + "="*80)

        # Sample data for simulation
        sample_weekly_data = {
            'revenue': 8500,
            'new_clients': 3,
            'total_sessions': 42,
            'cancellations': 2,
            'therapist_utilization': 0.85,
            'service_breakdown': {
                'individual_therapy': 28,
                'couples_therapy': 8,
                'family_therapy': 4,
                'emdr': 2
            },
            'referral_sources': {
                'social_media': 1,
                'psychology_today': 1,
                'word_of_mouth': 1
            }
        }

        # Monday: Business Analysis
        monday_results = self.monday_business_intelligence(sample_weekly_data)

        # Simulate business insights (in production, this comes from Claude API)
        sample_insights = """
        KEY FINDINGS:
        - Revenue up 8% vs last week
        - Individual therapy demand high (67% of sessions)
        - EMDR sessions low but growing interest
        - Social media drove 33% of new client inquiries
        - Therapist utilization healthy at 85%

        CONTENT OPPORTUNITIES:
        - Create educational content about EMDR therapy
        - Highlight individual therapy success stories (anonymized)
        - Share therapist availability for new clients
        """

        # Tuesday: Content Strategy
        tuesday_results = self.tuesday_content_strategy(sample_insights)

        # Simulate strategy results
        sample_strategy = """
        WEEKLY THEMES:
        - EMDR education and awareness
        - Mental health tips for individuals
        - Practice updates (new appointment slots)

        CONTENT CALENDAR:
        Wed: Educational post about EMDR
        Thu: Individual therapy success story
        Fri: Coping strategies for anxiety
        Sat: Weekend mental health tip
        Sun: Week ahead practice hours
        """

        # Wednesday-Friday: Content Creation
        content_prompts = self.wednesday_friday_content_creation(sample_strategy)

        # Sample performance metrics
        sample_metrics = {
            'content_performance': {
                'total_reach': 3500,
                'total_engagement': 142,
                'engagement_rate': 0.041,
                'best_post': 'EMDR educational post (65 engagements)'
            },
            'business_outcomes': {
                'inquiries': 2,
                'bookings': 1,
                'revenue_from_social': 850
            }
        }

        # Sunday: Performance Review
        sunday_results = self.sunday_performance_review(sample_metrics)

        # Summary
        print("\n\n" + "="*80)
        print("WEEKLY WORKFLOW SUMMARY")
        print("="*80 + "\n")

        print("✅ Completed full weekly cycle:")
        print(f"   Monday: Business intelligence prompt generated")
        print(f"   Tuesday: Content strategy prompt generated")
        print(f"   Wed-Fri: {len(content_prompts)} content creation prompts generated")
        print(f"   Sunday: Performance review prompt generated")

        print(f"\n📊 Total prompts generated: {2 + len(content_prompts) + 1}")
        print(f"   Ready to use with Claude API for actual implementation")

        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80 + "\n")

        print("To implement in production:")
        print("""
        1. Set up Claude API client:
           import anthropic
           client = anthropic.Anthropic(api_key="your-key")

        2. Run workflow for real:
           workflow = TherapyPracticeWorkflow(agents_dir="path/to/agents")

           # Monday
           monday = workflow.monday_business_intelligence(your_data)
           insights = client.messages.create(..., content=monday['prompt'])

           # Tuesday
           tuesday = workflow.tuesday_content_strategy(insights.content[0].text)
           strategy = client.messages.create(..., content=tuesday['prompt'])

           # Wed-Fri
           posts = workflow.wednesday_friday_content_creation(strategy.content[0].text)
           for post in posts:
               content = client.messages.create(..., content=post['prompt'])
               # Publish content

           # Sunday
           sunday = workflow.sunday_performance_review(metrics)
           review = client.messages.create(..., content=sunday['prompt'])

        3. Automate with cron jobs or scheduler:
           - Monday 9am: Run business analysis
           - Tuesday 10am: Generate content strategy
           - Wed-Fri 8am: Create daily content
           - Sunday 5pm: Performance review
        """)

        print("\n✨ Workflow simulation complete!\n")


def main():
    """Main entry point for workflow script."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Therapy Practice Weekly Workflow Orchestration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--agents-dir',
        required=True,
        help='Path to agents directory'
    )

    parser.add_argument(
        '--simulate',
        action='store_true',
        help='Run full week simulation'
    )

    args = parser.parse_args()

    # Initialize workflow
    workflow = TherapyPracticeWorkflow(agents_dir=args.agents_dir)

    if args.simulate:
        workflow.run_full_week_simulation()
    else:
        print("\nTherapy Practice Workflow initialized.")
        print("Use --simulate flag to run full week simulation")
        print("\nExample:")
        print(f"  python {Path(__file__).name} --agents-dir path/to/agents --simulate")


if __name__ == "__main__":
    main()
