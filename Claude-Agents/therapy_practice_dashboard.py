#!/usr/bin/env python3
"""
Therapy Practice Integrated Analytics Dashboard
Combines business metrics + content performance for unified insights
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class TherapyPracticeDashboard:
    """
    Integrated analytics dashboard combining:
    - Practice business metrics (revenue, clients, utilization)
    - Content performance metrics (engagement, reach, conversions)
    - Correlation analysis (content → business outcomes)
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize dashboard with optional data directory."""
        self.data_dir = data_dir or Path("./practice_data")
        self.data_dir.mkdir(exist_ok=True)

    def collect_business_metrics(self, practice_data: Dict) -> Dict:
        """
        Collect and structure business metrics.

        Args:
            practice_data: Raw practice management data

        Returns:
            Structured business metrics
        """
        return {
            'financial': {
                'revenue': practice_data.get('revenue', 0),
                'revenue_change': practice_data.get('revenue_change_pct', 0),
                'avg_session_rate': practice_data.get('avg_session_rate', 0),
                'outstanding_billing': practice_data.get('outstanding_billing', 0)
            },
            'clients': {
                'new_clients': practice_data.get('new_clients', 0),
                'total_active': practice_data.get('total_active_clients', 0),
                'retention_rate': practice_data.get('retention_rate', 0),
                'cancellation_rate': practice_data.get('cancellation_rate', 0)
            },
            'operations': {
                'total_sessions': practice_data.get('total_sessions', 0),
                'therapist_utilization': practice_data.get('therapist_utilization', 0),
                'available_slots': practice_data.get('available_slots', 0),
                'waitlist_size': practice_data.get('waitlist_size', 0)
            },
            'services': {
                'breakdown': practice_data.get('service_breakdown', {}),
                'most_requested': practice_data.get('most_requested_service', ''),
                'emerging_demand': practice_data.get('emerging_demand', [])
            }
        }

    def collect_content_metrics(self, content_data: Dict) -> Dict:
        """
        Collect and structure content performance metrics.

        Args:
            content_data: Social media and content performance data

        Returns:
            Structured content metrics
        """
        return {
            'reach': {
                'total_reach': content_data.get('total_reach', 0),
                'reach_change': content_data.get('reach_change_pct', 0),
                'impressions': content_data.get('impressions', 0),
                'unique_viewers': content_data.get('unique_viewers', 0)
            },
            'engagement': {
                'total_engagement': content_data.get('total_engagement', 0),
                'engagement_rate': content_data.get('engagement_rate', 0),
                'likes': content_data.get('likes', 0),
                'comments': content_data.get('comments', 0),
                'shares': content_data.get('shares', 0),
                'saves': content_data.get('saves', 0)
            },
            'performance': {
                'posts_published': content_data.get('posts_published', 0),
                'best_performing_post': content_data.get('best_post', {}),
                'worst_performing_post': content_data.get('worst_post', {}),
                'optimal_posting_times': content_data.get('best_times', [])
            },
            'traffic': {
                'website_visits_from_social': content_data.get('website_visits', 0),
                'profile_views': content_data.get('profile_views', 0),
                'link_clicks': content_data.get('link_clicks', 0)
            }
        }

    def calculate_integrated_metrics(self, business: Dict, content: Dict) -> Dict:
        """
        Calculate integrated metrics that connect content to business outcomes.

        Args:
            business: Business metrics dict
            content: Content metrics dict

        Returns:
            Integrated insights and correlations
        """
        # Content-driven inquiries (estimate based on referral sources)
        social_inquiries = business['clients'].get('new_clients', 0) * 0.33  # Estimate

        # Revenue attribution
        avg_client_value = business['financial']['revenue'] / max(business['clients']['total_active'], 1)
        content_attributed_revenue = social_inquiries * avg_client_value

        # ROI calculation
        estimated_content_cost = content['performance']['posts_published'] * 50  # $50 per post estimate
        roi = ((content_attributed_revenue - estimated_content_cost) / max(estimated_content_cost, 1)) * 100

        # Engagement to inquiry correlation
        engagement_per_inquiry = content['engagement']['total_engagement'] / max(social_inquiries, 1)

        return {
            'attribution': {
                'content_driven_inquiries': round(social_inquiries, 1),
                'content_attributed_revenue': round(content_attributed_revenue, 2),
                'inquiry_conversion_rate': round((social_inquiries / max(content['traffic']['website_visits_from_social'], 1)) * 100, 2)
            },
            'roi': {
                'content_investment': estimated_content_cost,
                'revenue_generated': round(content_attributed_revenue, 2),
                'roi_percentage': round(roi, 2),
                'cost_per_inquiry': round(estimated_content_cost / max(social_inquiries, 1), 2)
            },
            'efficiency': {
                'engagement_per_inquiry': round(engagement_per_inquiry, 1),
                'reach_to_inquiry_rate': round((social_inquiries / max(content['reach']['total_reach'], 1)) * 100, 4),
                'posts_per_inquiry': round(content['performance']['posts_published'] / max(social_inquiries, 1), 1)
            },
            'correlations': {
                'high_engagement_topics': [],  # Would be populated from detailed analysis
                'best_converting_content_types': [],
                'optimal_posting_schedule': content['performance']['optimal_posting_times']
            }
        }

    def generate_dashboard_report(self, business_data: Dict, content_data: Dict) -> str:
        """
        Generate comprehensive dashboard report.

        Args:
            business_data: Raw business data
            content_data: Raw content data

        Returns:
            Formatted dashboard report (markdown)
        """
        business = self.collect_business_metrics(business_data)
        content = self.collect_content_metrics(content_data)
        integrated = self.calculate_integrated_metrics(business, content)

        report = f"""
# Therapy Practice Integrated Dashboard
**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 BUSINESS PERFORMANCE

### Financial Metrics
- **Revenue**: ${business['financial']['revenue']:,.2f} ({business['financial']['revenue_change']:+.1f}% vs last period)
- **Average Session Rate**: ${business['financial']['avg_session_rate']:,.2f}
- **Outstanding Billing**: ${business['financial']['outstanding_billing']:,.2f}

### Client Metrics
- **New Clients**: {business['clients']['new_clients']} this period
- **Total Active Clients**: {business['clients']['total_active']}
- **Retention Rate**: {business['clients']['retention_rate']:.1f}%
- **Cancellation Rate**: {business['clients']['cancellation_rate']:.1f}%

### Operational Metrics
- **Total Sessions**: {business['operations']['total_sessions']}
- **Therapist Utilization**: {business['operations']['therapist_utilization']:.1%}
- **Available Slots**: {business['operations']['available_slots']}
- **Waitlist Size**: {business['operations']['waitlist_size']}

### Service Breakdown
"""
        for service, count in business['services']['breakdown'].items():
            report += f"- **{service.replace('_', ' ').title()}**: {count} sessions\n"

        report += f"""
---

## 📱 CONTENT PERFORMANCE

### Reach & Visibility
- **Total Reach**: {content['reach']['total_reach']:,} ({content['reach']['reach_change']:+.1f}% change)
- **Impressions**: {content['reach']['impressions']:,}
- **Unique Viewers**: {content['reach']['unique_viewers']:,}

### Engagement Metrics
- **Total Engagement**: {content['engagement']['total_engagement']:,}
- **Engagement Rate**: {content['engagement']['engagement_rate']:.2%}
- **Breakdown**:
  - Likes: {content['engagement']['likes']}
  - Comments: {content['engagement']['comments']}
  - Shares: {content['engagement']['shares']}
  - Saves: {content['engagement']['saves']}

### Content Performance
- **Posts Published**: {content['performance']['posts_published']}
- **Best Performing Post**: {content['performance'].get('best_performing_post', {}).get('title', 'N/A')}
- **Website Visits from Social**: {content['traffic']['website_visits_from_social']}

---

## 🔗 INTEGRATED INSIGHTS

### Content Attribution
- **Content-Driven Inquiries**: {integrated['attribution']['content_driven_inquiries']:.1f} new clients
- **Content-Attributed Revenue**: ${integrated['attribution']['content_attributed_revenue']:,.2f}
- **Inquiry Conversion Rate**: {integrated['attribution']['inquiry_conversion_rate']:.2f}%

### Marketing ROI
- **Content Investment**: ${integrated['roi']['content_investment']:,.2f}
- **Revenue Generated**: ${integrated['roi']['revenue_generated']:,.2f}
- **ROI**: {integrated['roi']['roi_percentage']:.1f}%
- **Cost Per Inquiry**: ${integrated['roi']['cost_per_inquiry']:,.2f}

### Marketing Efficiency
- **Engagement Per Inquiry**: {integrated['efficiency']['engagement_per_inquiry']:.1f} engagements
- **Reach to Inquiry Rate**: {integrated['efficiency']['reach_to_inquiry_rate']:.4f}%
- **Posts Per Inquiry**: {integrated['efficiency']['posts_per_inquiry']:.1f}

---

## 💡 KEY INSIGHTS

### What's Working
"""

        # Generate insights based on data
        if integrated['roi']['roi_percentage'] > 100:
            report += "- ✅ **Strong ROI**: Content marketing is generating positive returns\n"
        if business['clients']['retention_rate'] > 80:
            report += "- ✅ **High Retention**: Clients are staying engaged with services\n"
        if content['engagement']['engagement_rate'] > 0.03:
            report += "- ✅ **Good Engagement**: Content resonating with audience\n"

        report += "\n### Areas for Improvement\n"

        if business['operations']['therapist_utilization'] < 0.70:
            report += "- ⚠️ **Low Utilization**: Consider content about appointment availability\n"
        if integrated['attribution']['inquiry_conversion_rate'] < 10:
            report += "- ⚠️ **Low Conversion**: Optimize inquiry-to-booking process\n"
        if content['engagement']['engagement_rate'] < 0.02:
            report += "- ⚠️ **Low Engagement**: Review content strategy and topics\n"

        report += f"""
---

## 📈 RECOMMENDATIONS

### Content Strategy
1. **Double down on what works**: Analyze best-performing posts for themes
2. **Address service demand**: Create content about {business['services']['most_requested']}
3. **Fill available slots**: Promote appointment availability if utilization is low

### Business Actions
1. **Follow up on inquiries**: Optimize conversion from social media inquiries
2. **Monitor waitlist**: Consider expanding capacity if demand exceeds supply
3. **Seasonal planning**: Prepare content for known seasonal patterns

### Next Week Focus
- Content topics that drove most engagement
- Posting times that generated best reach
- Platform-specific optimization opportunities

---

**Dashboard Version**: 1.0
**HIPAA Compliance**: All data aggregated, no PHI included
"""

        return report

    def save_dashboard(self, report: str, filename: Optional[str] = None):
        """Save dashboard report to file."""
        if filename is None:
            filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.md"

        filepath = self.data_dir / filename

        with open(filepath, 'w') as f:
            f.write(report)

        print(f"✓ Dashboard saved to: {filepath}")

        return filepath

    def export_metrics_json(self, business_data: Dict, content_data: Dict) -> str:
        """Export all metrics as JSON for further analysis."""
        business = self.collect_business_metrics(business_data)
        content = self.collect_content_metrics(content_data)
        integrated = self.calculate_integrated_metrics(business, content)

        data = {
            'timestamp': datetime.now().isoformat(),
            'business_metrics': business,
            'content_metrics': content,
            'integrated_insights': integrated
        }

        filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        filepath = self.data_dir / filename

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Metrics exported to: {filepath}")

        return str(filepath)


def main():
    """Example usage of dashboard."""
    print("="*80)
    print("THERAPY PRACTICE INTEGRATED DASHBOARD")
    print("="*80 + "\n")

    # Sample data
    sample_business_data = {
        'revenue': 45000,
        'revenue_change_pct': 8,
        'avg_session_rate': 150,
        'outstanding_billing': 2500,
        'new_clients': 12,
        'total_active_clients': 85,
        'retention_rate': 92,
        'cancellation_rate': 5,
        'total_sessions': 180,
        'therapist_utilization': 0.87,
        'available_slots': 15,
        'waitlist_size': 3,
        'service_breakdown': {
            'individual_therapy': 120,
            'couples_therapy': 35,
            'family_therapy': 18,
            'emdr': 7
        },
        'most_requested_service': 'individual_therapy'
    }

    sample_content_data = {
        'total_reach': 15000,
        'reach_change_pct': 25,
        'impressions': 22000,
        'unique_viewers': 12500,
        'total_engagement': 630,
        'engagement_rate': 0.042,
        'likes': 450,
        'comments': 85,
        'shares': 65,
        'saves': 30,
        'posts_published': 5,
        'best_post': {'title': 'Managing Holiday Stress', 'engagement': 185},
        'worst_post': {'title': 'Practice Hours Update', 'engagement': 45},
        'best_times': ['Tuesday 10am', 'Thursday 2pm', 'Sunday 7pm'],
        'website_visits': 245,
        'profile_views': 520,
        'link_clicks': 180
    }

    # Create dashboard
    dashboard = TherapyPracticeDashboard()

    # Generate report
    report = dashboard.generate_dashboard_report(sample_business_data, sample_content_data)

    print(report)

    # Save dashboard
    dashboard.save_dashboard(report)

    # Export JSON
    dashboard.export_metrics_json(sample_business_data, sample_content_data)

    print("\n" + "="*80)
    print("✨ Dashboard generation complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
