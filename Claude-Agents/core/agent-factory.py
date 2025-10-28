"""
Agent Factory Module
Dynamically create and deploy specialized agents for any project
Part of Claude-Agents Framework
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from string import Template


class AgentFactory:
    """
    Factory for dynamically creating specialized agents based on project needs.

    Features:
    - Create agents on-the-fly from templates
    - Auto-detect required agent types for projects
    - Generate agent configurations automatically
    - Deploy agents to projects
    """

    def __init__(self, framework_dir: str = "Claude-Agents"):
        self.framework_dir = Path(framework_dir)
        self.agents_dir = self.framework_dir / "agents"
        self.templates_dir = self.framework_dir / "prompts" / "templates"
        self.created_agents = {}

    def create_agent(
        self,
        agent_name: str,
        agent_type: str,
        context: Dict,
        model: Dict,
        tools: Dict,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Create a new agent dynamically.

        Args:
            agent_name: Name for the agent (e.g., "sql-analyst")
            agent_type: Type/template to use (e.g., "data_scientist", "business_analyst", "base_agent")
            context: Context configuration (role, expertise, scope, constraints)
            model: Model configuration
            tools: Tools configuration (skills, slash_commands, mcp_servers)
            output_dir: Where to create agent (default: framework agents directory)

        Returns:
            Path to created agent directory
        """
        if output_dir is None:
            output_dir = self.agents_dir / agent_name
        else:
            output_dir = Path(output_dir) / agent_name

        output_dir.mkdir(parents=True, exist_ok=True)

        # Create config.yaml
        config = {
            'agent_name': agent_name,
            'context': context,
            'model': model,
            'tools': tools,
            'metadata': {
                'version': '1.0.0',
                'type': 'specialist',
                'created_by': 'AgentFactory',
                'template_used': agent_type
            }
        }

        config_path = output_dir / "config.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        # Create prompt.md from template
        prompt_path = output_dir / "prompt.md"
        template_file = self.templates_dir / f"{agent_type}_template.txt"

        if template_file.exists():
            # Use template
            with open(template_file, 'r') as f:
                template_content = f.read()

            # For specialized templates, only task is dynamic
            # For base template, replace all variables
            if agent_type == "base_agent":
                template_obj = Template(template_content)
                prompt_content = template_obj.safe_substitute(
                    role=context.get('role', ''),
                    expertise=self._format_list(context.get('expertise', [])),
                    scope=context.get('scope', ''),
                    constraints=self._format_list(context.get('constraints', [])),
                    model_name=model.get('name', 'claude-sonnet-4-20250514'),
                    max_tokens=str(model.get('max_tokens', 4000)),
                    temperature=str(model.get('temperature', 0.3)),
                    response_format=model.get('response_format', 'structured'),
                    task='$task',  # Keep as placeholder
                    methodology_steps='',  # Will be filled at runtime
                    output_format='',  # Will be filled at runtime
                    skills=self._format_list(tools.get('skills', [])),
                    slash_commands=self._format_list(tools.get('slash_commands', [])),
                    mcp_servers=self._format_list(tools.get('mcp_servers', [])),
                    external_apis=''
                )
            else:
                # For specialized templates, copy as-is (only $task is dynamic)
                prompt_content = template_content

            with open(prompt_path, 'w') as f:
                f.write(prompt_content)
        else:
            # Generate basic prompt if template not found
            prompt_content = self._generate_basic_prompt(agent_name, context, model, tools)
            with open(prompt_path, 'w') as f:
                f.write(prompt_content)

        print(f"✓ Created agent '{agent_name}' at {output_dir}")
        self.created_agents[agent_name] = output_dir

        return output_dir

    def create_agent_from_template(
        self,
        agent_name: str,
        template_name: str,
        customizations: Optional[Dict] = None,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Create agent from existing template with minimal customization.

        Args:
            agent_name: Name for new agent
            template_name: Template to use (base_agent, business_analyst, data_scientist, etc.)
            customizations: Optional customizations to apply
            output_dir: Where to create agent

        Returns:
            Path to created agent directory
        """
        # Load template defaults
        template_configs = self._get_template_defaults(template_name)

        # Apply customizations
        if customizations:
            template_configs.update(customizations)

        return self.create_agent(
            agent_name=agent_name,
            agent_type=template_name,
            context=template_configs['context'],
            model=template_configs['model'],
            tools=template_configs['tools'],
            output_dir=output_dir
        )

    def auto_create_agents_for_project(
        self,
        project_type: str,
        project_name: str,
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Automatically create appropriate agents for a project type.

        Args:
            project_type: Type of project (financial_analysis, data_science, web_app, etc.)
            project_name: Name of the project
            output_dir: Where to create agents

        Returns:
            List of paths to created agent directories
        """
        agent_recommendations = self._recommend_agents_for_project(project_type)

        created = []
        for agent_spec in agent_recommendations:
            agent_path = self.create_agent_from_template(
                agent_name=f"{project_name}-{agent_spec['name']}",
                template_name=agent_spec['template'],
                customizations=agent_spec.get('customizations'),
                output_dir=output_dir
            )
            created.append(agent_path)

        print(f"\n✓ Created {len(created)} agents for '{project_type}' project")
        return created

    def _recommend_agents_for_project(self, project_type: str) -> List[Dict]:
        """Recommend agents based on project type."""

        recommendations = {
            'financial_analysis': [
                {
                    'name': 'finance-analyst',
                    'template': 'business_analyst',
                    'customizations': None
                }
            ],
            'data_science': [
                {
                    'name': 'data-analyst',
                    'template': 'data_scientist',
                    'customizations': None
                }
            ],
            'sql_database_analysis': [
                {
                    'name': 'sql-analyst',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'SQL Database Analyst',
                            'expertise': ['SQL queries', 'Database optimization', 'Data analysis', 'ETL processes'],
                            'scope': 'SQL database analysis and optimization',
                            'constraints': ['Database performance', 'Query optimization', 'Data integrity']
                        },
                        'tools': {
                            'skills': ['sql', 'database-optimization', 'data-analysis'],
                            'slash_commands': ['/query', '/optimize', '/analyze', '/report'],
                            'mcp_servers': ['postgresql', 'sqlite', 'mysql']
                        }
                    }
                },
                {
                    'name': 'business-reporter',
                    'template': 'business_analyst',
                    'customizations': None
                }
            ],
            'web_analytics': [
                {
                    'name': 'web-analyst',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'Web Analytics Specialist',
                            'expertise': ['Google Analytics', 'User behavior analysis', 'Conversion optimization', 'A/B testing'],
                            'scope': 'Web analytics and optimization',
                            'constraints': ['Privacy compliance', 'GDPR/CCPA']
                        }
                    }
                }
            ],
            'customer_analysis': [
                {
                    'name': 'customer-analyst',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'Customer Analytics Specialist',
                            'expertise': ['Customer segmentation', 'Churn analysis', 'LTV calculation', 'RFM analysis'],
                            'scope': 'Customer data analysis and insights',
                            'constraints': ['PII protection', 'Data privacy']
                        }
                    }
                },
                {
                    'name': 'business-strategist',
                    'template': 'business_analyst',
                    'customizations': None
                }
            ],
            'full_stack': [
                {
                    'name': 'data-scientist',
                    'template': 'data_scientist',
                    'customizations': None
                },
                {
                    'name': 'business-analyst',
                    'template': 'business_analyst',
                    'customizations': None
                }
            ],
            'content_creation': [
                {
                    'name': 'content-strategist',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Content Strategy Specialist',
                            'expertise': [
                                'Content planning and ideation',
                                'Audience analysis and targeting',
                                'Content calendar management',
                                'SEO optimization',
                                'Brand voice and messaging',
                                'Multi-platform content strategy'
                            ],
                            'scope': 'Content strategy, planning, and optimization',
                            'constraints': [
                                'Brand consistency',
                                'Platform-specific best practices',
                                'SEO guidelines',
                                'Content quality standards'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 6000,
                            'temperature': 0.4,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['content-planning', 'seo-optimization', 'audience-analysis'],
                            'slash_commands': ['/brainstorm', '/calendar', '/seo-audit', '/audience-research'],
                            'mcp_servers': ['google-analytics', 'semrush', 'ahrefs']
                        }
                    }
                },
                {
                    'name': 'content-writer',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Professional Content Writer',
                            'expertise': [
                                'Long-form content writing',
                                'Blog posts and articles',
                                'Social media copywriting',
                                'Technical writing',
                                'Creative storytelling',
                                'Grammar and style editing'
                            ],
                            'scope': 'Content creation across multiple formats and platforms',
                            'constraints': [
                                'Tone and voice consistency',
                                'Factual accuracy',
                                'Proper citations and attribution',
                                'Platform character limits'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 8000,
                            'temperature': 0.7,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['writing', 'editing', 'research', 'formatting'],
                            'slash_commands': ['/write', '/edit', '/proofread', '/rewrite', '/optimize'],
                            'mcp_servers': ['grammarly', 'copyscape']
                        }
                    }
                },
                {
                    'name': 'content-editor',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Content Editor and Quality Assurance',
                            'expertise': [
                                'Content editing and proofreading',
                                'Style guide enforcement',
                                'Fact-checking and verification',
                                'Content quality assessment',
                                'Readability optimization',
                                'Plagiarism detection'
                            ],
                            'scope': 'Content review, editing, and quality control',
                            'constraints': [
                                'Style guide compliance',
                                'Factual accuracy',
                                'Original content only',
                                'Accessibility standards'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 6000,
                            'temperature': 0.2,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['editing', 'proofreading', 'fact-checking', 'quality-assurance'],
                            'slash_commands': ['/review', '/edit', '/fact-check', '/style-check', '/readability'],
                            'mcp_servers': ['grammarly', 'hemingway', 'copyscape']
                        }
                    }
                },
                {
                    'name': 'seo-specialist',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'SEO and Content Optimization Specialist',
                            'expertise': [
                                'Keyword research and analysis',
                                'On-page SEO optimization',
                                'Content performance tracking',
                                'Competitor analysis',
                                'Search intent mapping',
                                'Technical SEO auditing'
                            ],
                            'scope': 'SEO strategy and content optimization',
                            'constraints': [
                                'Google guidelines compliance',
                                'White-hat SEO only',
                                'Data-driven decisions'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 5000,
                            'temperature': 0.3,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['seo-analysis', 'keyword-research', 'data-analysis'],
                            'slash_commands': ['/keyword-research', '/seo-audit', '/competitor-analysis', '/optimize'],
                            'mcp_servers': ['google-search-console', 'semrush', 'ahrefs', 'google-analytics']
                        }
                    }
                }
            ],
            'therapy_practice_management': [
                {
                    'name': 'business-analyst',
                    'template': 'business_analyst',
                    'customizations': {
                        'context': {
                            'role': 'Therapy Practice Business Analyst',
                            'expertise': [
                                'Practice revenue and financial analysis',
                                'Client acquisition and retention metrics',
                                'Therapist utilization and scheduling optimization',
                                'Service demand analysis and forecasting',
                                'Insurance billing and reimbursement tracking',
                                'Practice growth strategy and planning'
                            ],
                            'scope': 'Financial analysis and business intelligence for therapy practice',
                            'constraints': [
                                'HIPAA compliance - no PHI in reports',
                                'Confidentiality of client data',
                                'Ethical billing practices',
                                'Professional boundary maintenance'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 5000,
                            'temperature': 0.1,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['financial-analysis', 'data-analysis', 'forecasting', 'reporting'],
                            'slash_commands': ['/financial', '/kpi', '/forecast', '/variance', '/trends'],
                            'mcp_servers': ['google-sheets', 'quickbooks', 'postgresql', 'sqlite']
                        }
                    }
                },
                {
                    'name': 'content-strategist',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Therapy Practice Content Strategy Specialist',
                            'expertise': [
                                'Mental health content strategy and planning',
                                'HIPAA-compliant social media marketing',
                                'Educational content development for therapy services',
                                'Community engagement and trust building',
                                'Data-driven content planning from practice metrics',
                                'Ethical marketing for mental health professionals'
                            ],
                            'scope': 'Content strategy aligned with practice business goals',
                            'constraints': [
                                'HIPAA compliance - no client information',
                                'APA and licensing board ethical guidelines',
                                'No medical advice or therapy via social media',
                                'Professional boundaries in public content'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 6000,
                            'temperature': 0.4,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['content-planning', 'healthcare-marketing', 'audience-analysis'],
                            'slash_commands': ['/strategy', '/calendar', '/audience-research', '/content-ideas'],
                            'mcp_servers': ['google-analytics', 'instagram', 'facebook']
                        }
                    }
                },
                {
                    'name': 'content-creator',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Mental Health Content Creator',
                            'expertise': [
                                'Educational mental health content writing',
                                'Therapy practice updates and announcements',
                                'Community engagement posts',
                                'Mental health awareness campaigns',
                                'Client success stories (anonymized)',
                                'Therapeutic tips and coping strategies'
                            ],
                            'scope': 'Creating engaging, ethical mental health content',
                            'constraints': [
                                'No PHI or identifiable client information',
                                'No diagnosis or treatment via social media',
                                'Evidence-based information only',
                                'Professional tone with warmth and empathy'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 7000,
                            'temperature': 0.6,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['healthcare-writing', 'social-media-content', 'storytelling'],
                            'slash_commands': ['/create-post', '/educational', '/announcement', '/testimonial'],
                            'mcp_servers': ['canva', 'unsplash']
                        }
                    }
                },
                {
                    'name': 'social-media-manager',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Therapy Practice Social Media Manager',
                            'expertise': [
                                'Social media scheduling and posting',
                                'Community engagement and response management',
                                'Platform-specific best practices (Instagram, Facebook, LinkedIn)',
                                'Crisis response and sensitive topic handling',
                                'Online reputation management',
                                'Engagement analytics and optimization'
                            ],
                            'scope': 'Managing social media presence for therapy practice',
                            'constraints': [
                                'No therapy or medical advice via comments',
                                'Professional boundaries in all interactions',
                                'Crisis situations referred to appropriate resources',
                                'HIPAA-compliant communication'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 5000,
                            'temperature': 0.5,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['social-media-management', 'community-management', 'crisis-response'],
                            'slash_commands': ['/schedule', '/engage', '/respond', '/monitor'],
                            'mcp_servers': ['buffer', 'hootsuite', 'instagram', 'facebook', 'linkedin']
                        }
                    }
                },
                {
                    'name': 'marketing-analytics',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'Therapy Practice Marketing Analytics Specialist',
                            'expertise': [
                                'Social media performance analysis',
                                'Content engagement tracking and optimization',
                                'Client acquisition source attribution',
                                'Marketing ROI calculation',
                                'Conversion tracking (inquiries to bookings)',
                                'Integrated business + content performance analysis'
                            ],
                            'scope': 'Analytics connecting marketing efforts to business outcomes',
                            'constraints': [
                                'HIPAA compliance in data analysis',
                                'Aggregated data only - no individual tracking',
                                'Ethical attribution methods',
                                'Privacy-first analytics approach'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 5000,
                            'temperature': 0.2,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['marketing-analytics', 'data-analysis', 'roi-analysis', 'reporting'],
                            'slash_commands': ['/analyze', '/roi', '/attribution', '/optimize', '/report'],
                            'mcp_servers': ['google-analytics', 'instagram-insights', 'facebook-insights', 'postgresql']
                        }
                    }
                },
                {
                    'name': 'market-research',
                    'template': 'data_scientist',
                    'customizations': {
                        'context': {
                            'role': 'Mental Health Market Research Analyst',
                            'expertise': [
                                'Local mental health service demand analysis',
                                'Competitor analysis (other therapy practices)',
                                'Service gap identification',
                                'Demographics and community needs assessment',
                                'Treatment modality trends (EMDR, DBT, CBT, etc.)',
                                'Insurance network and reimbursement research'
                            ],
                            'scope': 'Market intelligence for practice growth and service planning',
                            'constraints': [
                                'Ethical competitive analysis',
                                'No disparagement of other providers',
                                'Focus on community needs',
                                'Evidence-based trend analysis'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 6000,
                            'temperature': 0.3,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['market-research', 'competitive-analysis', 'trend-analysis'],
                            'slash_commands': ['/research', '/competitors', '/demand', '/trends', '/demographics'],
                            'mcp_servers': ['google-search', 'census-data', 'psychologytoday-api']
                        }
                    }
                },
                {
                    'name': 'practice-operations',
                    'template': 'base_agent',
                    'customizations': {
                        'context': {
                            'role': 'Therapy Practice Operations Analyst',
                            'expertise': [
                                'Therapist scheduling and utilization optimization',
                                'Appointment capacity planning',
                                'Waitlist management strategies',
                                'Service delivery efficiency',
                                'Client flow and retention optimization',
                                'Practice workflow improvement'
                            ],
                            'scope': 'Operational efficiency and practice management',
                            'constraints': [
                                'HIPAA compliance in scheduling',
                                'Clinical quality over efficiency',
                                'Therapist wellbeing and burnout prevention',
                                'Ethical client load management'
                            ]
                        },
                        'model': {
                            'name': 'claude-sonnet-4-20250514',
                            'max_tokens': 5000,
                            'temperature': 0.2,
                            'response_format': 'structured'
                        },
                        'tools': {
                            'skills': ['operations-analysis', 'scheduling-optimization', 'workflow-improvement'],
                            'slash_commands': ['/utilization', '/capacity', '/schedule', '/optimize', '/workflow'],
                            'mcp_servers': ['google-calendar', 'simplepractice', 'therapynotes']
                        }
                    }
                }
            ]
        }

        return recommendations.get(project_type, [
            {
                'name': 'general-agent',
                'template': 'base_agent',
                'customizations': None
            }
        ])

    def _get_template_defaults(self, template_name: str) -> Dict:
        """Get default configuration for a template."""

        defaults = {
            'base_agent': {
                'context': {
                    'role': 'General Purpose Agent',
                    'expertise': ['General analysis', 'Problem solving'],
                    'scope': 'General purpose assistance',
                    'constraints': ['Follow best practices', 'Provide clear documentation']
                },
                'model': {
                    'name': 'claude-sonnet-4-20250514',
                    'max_tokens': 4000,
                    'temperature': 0.3,
                    'response_format': 'structured'
                },
                'tools': {
                    'skills': [],
                    'slash_commands': [],
                    'mcp_servers': []
                }
            },
            'business_analyst': {
                'context': {
                    'role': 'Business Finance Analyst',
                    'expertise': ['Financial analysis', 'KPI reporting', 'Forecasting', 'Budget analysis'],
                    'scope': 'Business finance analysis',
                    'constraints': ['99.9% accuracy', 'GAAP compliance', 'Data security']
                },
                'model': {
                    'name': 'claude-sonnet-4-20250514',
                    'max_tokens': 5000,
                    'temperature': 0.1,
                    'response_format': 'structured'
                },
                'tools': {
                    'skills': ['xlsx', 'pdf', 'financial-modeling', 'reporting'],
                    'slash_commands': ['/financial', '/kpi', '/forecast', '/variance', '/report'],
                    'mcp_servers': ['google-sheets', 'quickbooks', 'salesforce', 'financial-apis']
                }
            },
            'data_scientist': {
                'context': {
                    'role': 'Senior Data Scientist',
                    'expertise': ['Statistical analysis', 'Machine learning', 'Data visualization', 'Predictive modeling'],
                    'scope': 'Data science and analytics',
                    'constraints': ['Reproducible results', 'Privacy compliance', 'Statistical rigor']
                },
                'model': {
                    'name': 'claude-sonnet-4-20250514',
                    'max_tokens': 6000,
                    'temperature': 0.2,
                    'response_format': 'structured'
                },
                'tools': {
                    'skills': ['statistical-analysis', 'ml-algorithms', 'data-visualization', 'data-processing'],
                    'slash_commands': ['/analyze', '/visualize', '/model', '/stats', '/feature-eng'],
                    'mcp_servers': ['postgresql', 'sqlite', 'jupyter']
                }
            }
        }

        return defaults.get(template_name, defaults['base_agent'])

    def _generate_basic_prompt(self, agent_name: str, context: Dict, model: Dict, tools: Dict) -> str:
        """Generate a basic prompt if template not available."""

        return f"""# {agent_name.replace('-', ' ').title()}

## KEY 1: CONTEXT

**Role:** {context.get('role', 'Specialized Agent')}

**Expertise:**
{self._format_list(context.get('expertise', []))}

**Scope:** {context.get('scope', '')}

**Constraints:**
{self._format_list(context.get('constraints', []))}

---

## KEY 2: MODEL

**Model Configuration:**
- Model: {model.get('name', 'claude-sonnet-4-20250514')}
- Max Tokens: {model.get('max_tokens', 4000)}
- Temperature: {model.get('temperature', 0.3)}
- Response Format: {model.get('response_format', 'structured')}

---

## KEY 3: PROMPT

**Task:** $task

**Methodology:**
1. Analyze requirements
2. Execute task using appropriate methods
3. Validate results
4. Provide documentation

**Output Requirements:**
- Clear, actionable results
- Professional formatting
- Complete documentation

---

## KEY 4: TOOLS

**Available Skills:**
{self._format_list(tools.get('skills', []))}

**Slash Commands:**
{self._format_list(tools.get('slash_commands', []))}

**MCP Servers:**
{self._format_list(tools.get('mcp_servers', []))}

---

**Remember:** You are a specialized agent operating within the Claude-Agents framework.
"""

    def _format_list(self, items: List[str]) -> str:
        """Format list items with bullet points."""
        if not items:
            return "- None"
        return '\n'.join(f"- {item}" for item in items)

    def list_available_templates(self) -> List[str]:
        """List all available agent templates."""
        templates = []
        if self.templates_dir.exists():
            for file in self.templates_dir.glob("*_template.txt"):
                template_name = file.stem.replace('_template', '')
                templates.append(template_name)
        return templates

    def get_created_agents(self) -> Dict[str, Path]:
        """Get dictionary of created agents and their paths."""
        return self.created_agents


# Example usage
if __name__ == "__main__":
    factory = AgentFactory()

    print("Available Templates:")
    for template in factory.list_available_templates():
        print(f"  - {template}")

    print("\n" + "="*60)
    print("Example 1: Create Custom SQL Analyst Agent")
    print("="*60)

    # Create a custom SQL analyst agent
    sql_agent = factory.create_agent(
        agent_name="sql-database-analyst",
        agent_type="data_scientist",
        context={
            'role': 'SQL Database Analyst',
            'expertise': [
                'SQL query optimization',
                'Database performance tuning',
                'Data analysis and reporting',
                'ETL processes'
            ],
            'scope': 'SQL database analysis, optimization, and reporting',
            'constraints': [
                'Database performance standards',
                'Query optimization best practices',
                'Data integrity requirements'
            ]
        },
        model={
            'name': 'claude-sonnet-4-20250514',
            'max_tokens': 6000,
            'temperature': 0.2,
            'response_format': 'structured'
        },
        tools={
            'skills': ['sql', 'database-optimization', 'data-analysis', 'reporting'],
            'slash_commands': ['/query', '/optimize', '/analyze', '/report', '/schema'],
            'mcp_servers': ['postgresql', 'sqlite', 'mysql']
        },
        output_dir=Path("my_project/agents")
    )

    print(f"✓ SQL Agent created at: {sql_agent}")

    print("\n" + "="*60)
    print("Example 2: Auto-Create Agents for Project")
    print("="*60)

    # Automatically create agents for SQL database analysis project
    agents = factory.auto_create_agents_for_project(
        project_type="sql_database_analysis",
        project_name="sales-db",
        output_dir=Path("my_sales_project/agents")
    )

    print("\nCreated agents:")
    for agent in agents:
        print(f"  - {agent}")
