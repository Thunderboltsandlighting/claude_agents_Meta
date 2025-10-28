"""
Claude-Agents Framework Setup
Install as a reusable package
"""

from setuptools import setup, find_packages

setup(
    name="claude-agents",
    version="1.0.0",
    description="Modular framework for creating specialized Claude AI agents",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "xlsxwriter>=3.1.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "statsmodels>=0.14.0",
        "scipy>=1.10.0",
        "anthropic>=0.18.0",  # Claude API
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'claude-agents=core.cli:main',
        ],
    },
)
