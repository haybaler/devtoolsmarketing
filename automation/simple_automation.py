#!/usr/bin/env python3
"""
Enhanced Developer Tools Directory Automation
Comprehensive newsletter generation with rich content
"""

import os
import sys
import json
import requests
import datetime
import random
from typing import Dict, List, Any

class EnhancedAutomation:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')  # Free GitHub API
        self.openai_key = os.getenv('OPENAI_API_KEY')   # OpenAI API (~$20/month)
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY')  # NVIDIA NIM API
        
    def parse_readme_categories(self) -> Dict[str, List[str]]:
        """Parse README.md and extract categories with bullet items as queries."""
        import re

        readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        categories: Dict[str, List[str]] = {}

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print('README.md not found - using fallback categories')
            return {}

        in_section = False
        current = None

        for line in lines:
            if line.startswith('## ') and 'Categories' in line:
                in_section = True
                continue

            if in_section:
                if line.startswith('## ') and 'Categories' not in line:
                    break
                if line.startswith('### '):
                    current = re.sub(r'^###\s+', '', line).strip()
                    categories[current] = []
                    continue
                if line.startswith('-') and current:
                    bullet = re.sub(r'[*`\-]', '', line).strip()
                    bullet = bullet.split(':')[0].strip()
                    if bullet:
                        categories[current].append(bullet)

        return categories

    def get_trending_repos_by_category(self) -> Dict[str, List[Dict]]:
        """Get trending developer tools organized by category"""

        categories = self.parse_readme_categories()
        if not categories:
            # Fallback static categories if README parsing fails
            categories = {
                "AI Development": [
                    "AI code generation", "AI pair programming", "AI coding assistant",
                    "AI code review", "AI testing", "natural language to code"
                ],
                "Editors & IDEs": [
                    "code editor", "IDE", "development environment", "text editor",
                    "VS Code extension", "vim plugin"
                ],
                "Infrastructure & DevOps": [
                    "cloud deployment", "CI/CD", "docker", "kubernetes",
                    "monitoring", "observability", "infrastructure"
                ],
                "Frontend & Mobile": [
                    "React tools", "Vue tools", "Angular tools", "mobile development",
                    "UI components", "design system", "frontend framework"
                ],
                "Backend & Data": [
                    "API development", "database tools", "authentication",
                    "microservices", "backend framework", "data pipeline"
                ],
                "Testing & QA": [
                    "testing framework", "automated testing", "performance testing",
                    "security testing", "code quality", "linting"
                ]
            }

        trending_by_category = {}
        
        for category, queries in categories.items():
            trending_by_category[category] = []
            
            for query in queries[:2]:  # Limit to avoid rate limits
                url = f"https://api.github.com/search/repositories"
                params = {
                    'q': f'{query} created:>2024-06-01',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 3
                }
                
                headers = {}
                if self.github_token:
                    headers['Authorization'] = f'token {self.github_token}'
                
                try:
                    response = requests.get(url, params=params, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        for repo in data.get('items', []):
                            trending_by_category[category].append({
                                'name': repo['name'],
                                'full_name': repo['full_name'],
                                'description': repo['description'] or 'No description',
                                'stars': repo['stargazers_count'],
                                'url': repo['html_url'],
                                'language': repo['language'],
                                'created_at': repo['created_at']
                            })
                except Exception as e:
                    print(f"Error fetching {category} data: {e}")
            
            # Remove duplicates and get top tools
            unique_tools = {tool['full_name']: tool for tool in trending_by_category[category]}.values()
            trending_by_category[category] = sorted(unique_tools, key=lambda x: x['stars'], reverse=True)[:3]
        
        return trending_by_category
    
    def get_enhanced_weekly_highlights(self) -> Dict[str, Any]:
        """Enhanced weekly highlights with more comprehensive data"""
        return {
            "featured_companies": [
                {
                    "name": "Cursor (Anysphere)",
                    "category": "AI-Enhanced Editors",
                    "valuation": "$9.9B",
                    "funding": "$900M Series C",
                    "investors": ["Thrive Capital", "Andreessen Horowitz"],
                    "why_hot": "Revolutionary AI-native coding experience transforming developer workflows",
                    "users": "1M+ developers",
                    "growth": "300% YoY"
                },
                {
                    "name": "Replit",
                    "category": "Cloud-Based IDEs", 
                    "valuation": "$800M+",
                    "funding": "$100M+ total",
                    "why_hot": "AI-powered Ghostwriter integration making cloud development mainstream",
                    "users": "20M+ developers"
                },
                {
                    "name": "Retool",
                    "category": "Low-Code Platforms",
                    "valuation": "$3.2B", 
                    "funding": "$145M Series C",
                    "why_hot": "Leading enterprise internal app platform with AI agents",
                    "enterprise_customers": "5000+"
                }
            ],
            "yc_portfolio": [
                {
                    "name": "Cortex",
                    "batch": "W20",
                    "category": "Developer Platforms",
                    "description": "Internal developer portal for engineering teams",
                    "valuation": "$470M",
                    "growth_stage": "Series B"
                },
                {
                    "name": "Fume",
                    "batch": "W24", 
                    "category": "AI Development",
                    "description": "AI software developer that automatically fixes bugs",
                    "stage": "Seed",
                    "why_hot": "Autonomous bug fixing with human-level code understanding"
                },
                {
                    "name": "Mocha",
                    "batch": "S23",
                    "category": "No-Code Development", 
                    "description": "AI-powered app builder for non-technical users",
                    "stage": "Early stage"
                }
            ],
            "market_insights": {
                "total_investment_2024": "$15B+",
                "avg_series_a": "$25M (up 40% from 2023)",
                "top_trends": [
                    "'Vibe Coding' Revolution: Natural language programming mainstream",
                    "AI-First Development: Tools designed with AI integration from ground up", 
                    "Multi-Agent Systems: AI teams collaborating on complex development",
                    "Security-First DevOps: Security integrated into every development stage"
                ],
                "adoption_metrics": {
                    "ai_assisted_coding": "72% of developers",
                    "faster_completion": "55% faster project completion with AI",
                    "yc_ai_adoption": "25% of YC startups use AI for majority of codebase",
                    "automation_potential": "80% of routine coding tasks can be automated"
                }
            },
            "design_inspiration": [
                "Vercel: Clean, modern interface with excellent developer experience",
                "Linear: Elegant design with focus on speed and efficiency", 
                "Stripe: Beautiful documentation and developer-first design",
                "Notion: Flexible, component-based interface design"
            ],
            "weekly_focus": self.get_weekly_focus()
        }
    
    def get_weekly_focus(self) -> Dict[str, str]:
        """Determine this week's focus area based on day of week"""
        focus_schedule = {
            0: {"area": "Y Combinator Scouting", "description": "Latest YC companies and portfolio updates"},
            1: {"area": "VC Investment Tracking", "description": "Funding rounds, valuations, and market analysis"},
            2: {"area": "Product Hunt Analysis", "description": "Trending developer tools and community favorites"},
            3: {"area": "GitHub Repository Mining", "description": "New open-source tools and viral repositories"},
            4: {"area": "Community Feedback", "description": "Developer insights and tool recommendations"},
            5: {"area": "Market Trends Analysis", "description": "Industry trends and technology adoption patterns"},
            6: {"area": "Newsletter Preparation", "description": "Comprehensive weekly developer tools digest"}
        }
        
        day_of_week = datetime.datetime.now().weekday()
        return focus_schedule[day_of_week]
    
    def generate_comprehensive_newsletter(self, trending_data: Dict, highlights: Dict) -> str:
        """Generate comprehensive newsletter with all enhanced sections"""
        
        current_date = datetime.datetime.now()
        week_num = current_date.isocalendar()[1]
        
        # Enhanced prompt for AI generation
        prompt = f"""
        Create a comprehensive developer tools newsletter for Week {week_num}, 2025.
        
        Data to include:
        
        TRENDING TOOLS BY CATEGORY:
        {json.dumps(trending_data, indent=2)}
        
        FEATURED COMPANIES & MARKET DATA:
        {json.dumps(highlights, indent=2)}
        
        Format as a professional newsletter with these sections:
        
        1. **Engaging Subject Line** (under 50 characters)
        
        2. **Opening Hook** (2-3 sentences about the biggest news)
        
        3. **🌟 FEATURED SPOTLIGHT** (highlight the most important company/funding)
        
        4. **📈 TRENDING BY CATEGORY** (organize tools by category with 2-3 tools each)
        
        5. **🚀 Y COMBINATOR WATCH** (YC portfolio updates)
        
        6. **💰 MARKET INTELLIGENCE** (investment trends, adoption metrics)
        
        7. **🎨 DESIGN INSPIRATION** (UI/UX trends from top companies)
        
        8. **📊 WEEK'S FOCUS** (based on weekly focus area)
        
        9. **🎯 PREMIUM COMMUNITY** (call-to-action for newsletter + community)
        
        10. **🔗 QUICK LINKS** (repository links and resources)
        
        Make it engaging, data-driven, and valuable for developers, VCs, and tech enthusiasts.
        Target length: 500-700 words total.
        Use emojis strategically and include specific metrics when available.
        """
        
        # Try AI generation first
        if self.nvidia_api_key:
            try:
                return self.generate_with_nvidia_nim(prompt)
            except Exception as e:
                print(f"NVIDIA NIM API error: {e}, falling back to OpenAI...")
        
        if self.openai_key:
            try:
                return self.generate_with_openai(prompt)
            except Exception as e:
                print(f"OpenAI API error: {e}, using enhanced fallback...")
        
        # Enhanced fallback with comprehensive content
        return self.generate_enhanced_fallback(trending_data, highlights, week_num)
    
    def generate_enhanced_fallback(self, trending_data: Dict, highlights: Dict, week_num: int) -> str:
        """Enhanced fallback newsletter with comprehensive content"""
        
        featured = highlights['featured_companies'][0]
        weekly_focus = highlights['weekly_focus']
        
        newsletter = f"""**Subject: Developer Tools Revolution Week {week_num} - ${featured['valuation']} AI Editor + Market Intel**

Hey Developer Tools Community! 🚀

The developer tools landscape just hit another milestone! {featured['name']} secured {featured['funding']} at a {featured['valuation']} valuation, while AI-powered development tools are seeing record adoption across the industry.

## 🌟 FEATURED SPOTLIGHT: {featured['name']}

**Category**: {featured['category']}  
**Valuation**: {featured['valuation']} | **Funding**: {featured['funding']}  
**Why It's Hot**: {featured['why_hot']}  
**Traction**: {featured.get('users', 'High growth')}  

*Investors*: {', '.join(featured['investors'])}

## 📈 TRENDING BY CATEGORY
"""
        
        # Add trending tools by category
        for category, tools in trending_data.items():
            if tools:  # Only show categories with tools
                newsletter += f"\n### {category}\n"
                for i, tool in enumerate(tools[:2], 1):  # Top 2 per category
                    newsletter += f"**{i}. {tool['name']}** - {tool['stars']:,} ⭐\n"
                    newsletter += f"   {tool['description'][:80]}...\n"
                    newsletter += f"   *{tool['language']}* | [View on GitHub]({tool['url']})\n\n"
        
        newsletter += f"""
## 🚀 Y COMBINATOR PORTFOLIO WATCH

**Growing Fast**:
"""
        
        for yc_company in highlights['yc_portfolio'][:2]:
            newsletter += f"• **{yc_company['name']}** ({yc_company['batch']}) - {yc_company['description']}\n"
            newsletter += f"  *{yc_company['category']}* | Stage: {yc_company.get('stage', 'Growth')}\n\n"
        
        newsletter += f"""
## 💰 MARKET INTELLIGENCE

**2024 Investment Snapshot**:
• Total VC Investment: {highlights['market_insights']['total_investment_2024']} in developer tools
• Average Series A: {highlights['market_insights']['avg_series_a']}
• AI Adoption: {highlights['market_insights']['adoption_metrics']['ai_assisted_coding']} use AI-assisted coding

**Key Trends**:
"""
        
        for trend in highlights['market_insights']['top_trends'][:3]:
            newsletter += f"• {trend}\n"
        
        newsletter += f"""

## 🎨 DESIGN INSPIRATION THIS WEEK

Drawing inspiration from industry design leaders:
"""
        
        for inspiration in highlights['design_inspiration'][:2]:
            newsletter += f"• {inspiration}\n"
        
        newsletter += f"""

## 📊 THIS WEEK'S FOCUS: {weekly_focus['area']}

{weekly_focus['description']}

*Our systematic approach ensures comprehensive coverage of the developer tools ecosystem.*

## 🎯 PREMIUM DEVELOPER TOOLS COMMUNITY

**What You Get with Premium Access**:
• 🎤 **Founder Interviews**: 1-on-1s with creators of trending tools
• 📹 **Live Product Demos**: Monthly sessions with tool creators  
• 🎪 **Exclusive Webinars**: Q&As with industry leaders
• 💡 **Early Access**: Beta test tools before they hit trending
• 📊 **Deep Analysis**: Market insights you won't find elsewhere
• 💬 **Discord Community**: Connect with 1,000+ developers and VCs

**Current Stats**: 10,000+ subscribers | 72% developer audience | 18% VC/investor

👉 **[Join Premium Community - Free Trial](YOUR_NEWSLETTER_LINK)**

## 🔗 QUICK ACCESS

• **Full Directory**: [500+ Tools Catalog](https://github.com/haybaler/devtoolsmarketing)
• **AI Tools**: [75+ AI Development Tools](https://github.com/haybaler/devtoolsmarketing/tree/main/tools/ai-powered-development)
• **Editors & IDEs**: [85+ Development Environments](https://github.com/haybaler/devtoolsmarketing/tree/main/tools/editors-ides)
• **Market Analysis**: [Investment & Trend Data](https://github.com/haybaler/devtoolsmarketing/tree/main/analysis)
• **Y Combinator**: [50+ YC Portfolio Companies](https://github.com/haybaler/devtoolsmarketing/tree/main/analysis)

---

**Growing the Community**:
• ⭐ **Star our repository** to support the project
• 📧 **Share this newsletter** with fellow developers  
• 💬 **Join our Discord** for real-time discussions
• 📝 **Contribute tools** via GitHub issues

*Next edition*: Fresh tools, funding news, and exclusive founder insights!

Keep building! 🛠️  
*The Developer Tools Community*

---

*P.S. This GitHub issue preview contains ~50% of our full newsletter content. Premium subscribers get 2x more insights, exclusive interviews, and early access to trending tools.*
"""
        
        return newsletter
    
    def generate_with_nvidia_nim(self, prompt: str) -> str:
        """Generate content using NVIDIA NIM API"""
        import requests
        
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.nvidia_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta/llama-3.1-405b-instruct",
            "messages": [
                {"role": "system", "content": "You are an expert tech newsletter writer who creates comprehensive, data-driven content about developer tools, startups, and market trends. You write in an engaging, professional style that appeals to developers, VCs, and tech enthusiasts."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500,  # Increased for comprehensive content
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def generate_with_openai(self, prompt: str) -> str:
        """Generate content using OpenAI API"""
        try:
            import openai
        except ImportError:
            print("OpenAI package not installed. Using enhanced fallback.")
            raise ImportError("OpenAI package not available")
        
        openai.api_key = self.openai_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert tech newsletter writer who creates comprehensive, data-driven content about developer tools, startups, and market trends. You write in an engaging, professional style that appeals to developers, VCs, and tech enthusiasts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,  # Increased for comprehensive content
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def run_enhanced_automation(self):
        """Main enhanced automation function"""
        
        print("🤖 Starting Enhanced Developer Tools Automation...")
        print("=" * 50)
        
        # Step 1: Get comprehensive GitHub data by category
        print("📊 Fetching trending repositories by category...")
        trending_data = self.get_trending_repos_by_category()
        total_tools = sum(len(tools) for tools in trending_data.values())
        print(f"✅ Found {total_tools} trending tools across {len(trending_data)} categories")
        
        # Step 2: Get enhanced weekly highlights
        print("🎯 Loading enhanced weekly highlights...")
        highlights = self.get_enhanced_weekly_highlights()
        print("✅ Enhanced highlights loaded with market data")
        
        # Step 3: Generate comprehensive newsletter
        print("📝 Generating comprehensive newsletter content...")
        newsletter_content = self.generate_comprehensive_newsletter(trending_data, highlights)
        print("✅ Enhanced newsletter generated!")
        
        # Step 4: Save and display
        week_num = datetime.datetime.now().isocalendar()[1]
        filename = f"newsletter/enhanced-week-{week_num}-2025.md"
        
        try:
            os.makedirs("newsletter", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(newsletter_content)
            print(f"✅ Enhanced newsletter saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving newsletter: {e}")
            filename = f"enhanced-week-{week_num}-2025.md"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(newsletter_content)
                print(f"✅ Enhanced newsletter saved to: {filename}")
            except Exception as e2:
                print(f"❌ Error saving to alternative location: {e2}")
        
        print("\n" + "=" * 50)
        print("🎉 ENHANCED AUTOMATION COMPLETE!")
        print("=" * 50)
        print("\n📧 COMPREHENSIVE NEWSLETTER READY:")
        print("-" * 40)
        print(newsletter_content)
        print("-" * 40)
        print(f"\n✅ Ready for premium newsletter distribution!")
        print(f"📁 Saved to: {filename}")
        
        return newsletter_content

# Keep the original SimpleAutomation class for backwards compatibility
class SimpleAutomation:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY')
        
    def get_trending_repos(self) -> List[Dict]:
        """Get trending developer tools from GitHub (FREE API)"""
        queries = ["developer tools", "code editor", "IDE", "AI coding", "development automation"]
        trending_tools = []
        
        for query in queries:
            url = f"https://api.github.com/search/repositories"
            params = {
                'q': f'{query} created:>2024-01-01',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }
            
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            try:
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for repo in data.get('items', []):
                        trending_tools.append({
                            'name': repo['name'],
                            'full_name': repo['full_name'],
                            'description': repo['description'] or 'No description',
                            'stars': repo['stargazers_count'],
                            'url': repo['html_url'],
                            'language': repo['language'],
                            'created_at': repo['created_at']
                        })
            except Exception as e:
                print(f"Error fetching GitHub data: {e}")
        
        unique_tools = {tool['full_name']: tool for tool in trending_tools}.values()
        return sorted(unique_tools, key=lambda x: x['stars'], reverse=True)[:10]
    
    def get_manual_weekly_highlights(self) -> Dict[str, Any]:
        """Manual curation of weekly highlights (no API needed)"""
        return {
            "featured_tool": {
                "name": "Cursor",
                "description": "AI-native code editor that raised $900M",
                "valuation": "$9.9B",
                "why_hot": "Revolutionary AI-first approach to coding",
                "funding": "$900M Series C"
            },
            "funding_news": [
                {
                    "company": "Anysphere (Cursor)",
                    "amount": "$900M",
                    "round": "Series C",
                    "investors": ["Thrive Capital", "Andreessen Horowitz"]
                }
            ],
            "market_trends": [
                "AI-native development tools attracting record investments",
                "Traditional IDEs adding AI features to compete",
                "Cloud-based development environments gaining traction"
            ]
        }
    
    def generate_newsletter_with_ai(self, github_data: List[Dict], highlights: Dict) -> str:
        """Generate newsletter content using AI (OpenAI or NVIDIA NIM)"""
        prompt = f"""
        Create a weekly developer tools newsletter based on this data:
        
        GitHub Trending Tools:
        {json.dumps(github_data, indent=2)}
        
        Weekly Highlights:
        {json.dumps(highlights, indent=2)}
        
        Format it as:
        1. Catchy subject line
        2. Brief intro (2-3 sentences)
        3. Featured tool spotlight
        4. 3-4 trending GitHub discoveries
        5. Market insight (1-2 sentences)
        6. Call to action
        
        Keep it conversational and exciting. Target audience: developers, VCs, tech enthusiasts.
        Maximum 300 words total.
        """
        
        if self.nvidia_api_key:
            try:
                enhanced_automation = EnhancedAutomation()
                return enhanced_automation.generate_with_nvidia_nim(prompt)
            except Exception as e:
                print(f"NVIDIA NIM API error: {e}, falling back to OpenAI...")
        
        if self.openai_key:
            try:
                enhanced_automation = EnhancedAutomation()
                return enhanced_automation.generate_with_openai(prompt)
            except Exception as e:
                print(f"OpenAI API error: {e}, using fallback...")
        
        return self.generate_fallback_newsletter(github_data, highlights)
    
    def generate_fallback_newsletter(self, github_data: List[Dict], highlights: Dict) -> str:
        """Fallback newsletter if OpenAI fails"""
        week_num = datetime.datetime.now().isocalendar()[1]
        
        newsletter = f"""
🔥 Developer Tools Weekly - Week {week_num}

Hey there!

This week's developer tools scene is absolutely buzzing! {highlights['featured_tool']['name']} just raised {highlights['featured_tool']['funding']} at a {highlights['featured_tool']['valuation']} valuation - making it one of the most valuable dev tools ever! 🚀

🌟 FEATURED TOOL: {highlights['featured_tool']['name']}
{highlights['featured_tool']['description']}
Why it's hot: {highlights['featured_tool']['why_hot']}

📈 TRENDING ON GITHUB:
"""
        
        for i, tool in enumerate(github_data[:3], 1):
            newsletter += f"""
{i}. {tool['name']} - {tool['stars']} ⭐
   {tool['description'][:100]}...
   Language: {tool['language']} | {tool['url']}
"""
        
        newsletter += f"""
💡 MARKET INSIGHT:
{highlights['market_trends'][0]}

🎯 EXCLUSIVE NEWSLETTER CONTENT:
Want MORE than just the trending tools? Subscribe to our premium newsletter for:
• 🎤 FOUNDER INTERVIEWS: 1-on-1 with creators of trending tools
• 📹 LIVE DEMOS: Watch founders demo their latest features
• 🎪 WEBINARS & Q&As: Ask questions directly to dev tool leaders
• 💡 EARLY ACCESS: See tools before they hit GitHub trending
• 📊 DETAILED ANALYSIS: Deep dives you won't find anywhere else

📧 SUBSCRIBE FREE: [Your Newsletter Link Here]
📧 Join 10,000+ developers getting the inside scoop!

🔗 QUICK LINKS:
• Full Directory: https://github.com/haybaler/devtoolsmarketing
• AI Tools: https://github.com/haybaler/devtoolsmarketing/tree/main/tools/ai-powered-development
• Editors & IDEs: https://github.com/haybaler/devtoolsmarketing/tree/main/tools/editors-ides

❤️ Enjoying these discoveries? 
• ⭐ Star this repo to show support
• 📧 Subscribe to our newsletter for exclusive content
• 🔄 Share with fellow developers

Keep building! 🚀
[Your Name]

P.S. This GitHub issue is just a taste - our newsletter subscribers get 3x more content including exclusive founder interviews!
"""
        
        return newsletter
    
    def run_weekly_automation(self):
        """Run simple automation (backwards compatible)"""
        print("🤖 Starting Simple Developer Tools Automation...")
        print("=" * 50)
        
        # Try enhanced version first if possible
        try:
            enhanced_automation = EnhancedAutomation()
            return enhanced_automation.run_enhanced_automation()
        except Exception as e:
            print(f"Enhanced automation failed: {e}, falling back to simple version...")
        
        # Fallback to simple version
        print("📊 Fetching GitHub trending repositories...")
        github_trending = self.get_trending_repos()
        print(f"✅ Found {len(github_trending)} trending tools")
        
        print("🎯 Loading weekly highlights...")
        highlights = self.get_manual_weekly_highlights()
        print("✅ Weekly highlights loaded")
        
        print("📝 Generating newsletter content...")
        newsletter_content = self.generate_newsletter_with_ai(github_trending, highlights)
        print("✅ Newsletter generated!")
        
        week_num = datetime.datetime.now().isocalendar()[1]
        filename = f"newsletter/auto-generated-week-{week_num}-2025.md"
        
        try:
            os.makedirs("newsletter", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(newsletter_content)
            print(f"✅ Newsletter saved successfully to: {filename}")
        except Exception as e:
            print(f"❌ Error saving newsletter: {e}")
            filename = f"auto-generated-week-{week_num}-2025.md"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(newsletter_content)
                print(f"✅ Newsletter saved to alternative location: {filename}")
            except Exception as e2:
                print(f"❌ Error saving to alternative location: {e2}")
        
        print("\n" + "=" * 50)
        print("🎉 AUTOMATION COMPLETE!")
        print("=" * 50)
        print("\n📧 COPY-PASTE READY NEWSLETTER:")
        print("-" * 40)
        print(newsletter_content)
        print("-" * 40)
        print("\n✅ Ready to paste into your newsletter editor!")
        print(f"📁 Also saved to: {filename}")
        
        return newsletter_content

def setup_instructions():
    print("""
🚀 ENHANCED AUTOMATION SETUP (2 minutes)

1. Get GitHub Token (FREE):
   • Go to: https://github.com/settings/tokens
   • Generate token with 'public_repo' scope
   • Set: export GITHUB_TOKEN=your_token

2. Get AI API Key (optional, for enhanced content):
   
   OPTION A - NVIDIA NIM (Recommended - Fast & Cheap):
   • Go to: https://build.nvidia.com/
   • Sign up for free account
   • Get API key for Llama 3.1 405B
   • Set: export NVIDIA_API_KEY=your_key
   
   OPTION B - OpenAI (~$20/month):
   • Go to: https://platform.openai.com/api-keys
   • Create new key
   • Set: export OPENAI_API_KEY=your_key
   • Install: pip install openai

3. Run automation:
   • python automation/simple_automation.py        # Enhanced version
   • python automation/simple_automation.py simple # Original version

Features:
✅ 6 tool categories with trending analysis
✅ Y Combinator portfolio tracking  
✅ Market intelligence & investment data
✅ Design inspiration from top companies
✅ Weekly focus areas for comprehensive coverage
✅ Professional newsletter format ready for premium distribution

That's it! You'll get comprehensive newsletter content ready for scaling! 🎯
""")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "setup":
            setup_instructions()
        elif len(sys.argv) > 1 and sys.argv[1] == "simple":
            print("🤖 Starting Simple Developer Tools Automation...")
            automation = SimpleAutomation()
            automation.run_weekly_automation()
        else:
            print("🤖 Starting Enhanced Developer Tools Automation...")
            automation = EnhancedAutomation()
            automation.run_enhanced_automation()
            print("🎉 Enhanced automation completed successfully!")
    except Exception as e:
        print(f"❌ Error in automation: {e}")
        print("📝 Creating fallback newsletter...")
        
        fallback_content = """🔥 Developer Tools Weekly

Hey there!

Our automated newsletter system encountered an issue, but we're still here with updates!

🚀 Check out the latest trending developer tools on our GitHub repository:
https://github.com/haybaler/devtoolsmarketing

We'll have the full automated newsletter back up soon!

Keep building! 🛠️
[Your Name]
"""
        
        try:
            import datetime
            import os
            week_num = datetime.datetime.now().isocalendar()[1]
            os.makedirs("newsletter", exist_ok=True)
            filename = f"newsletter/fallback-week-{week_num}-2025.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(fallback_content)
            print(f"✅ Fallback newsletter created: {filename}")
        except Exception as e2:
            print(f"❌ Could not create fallback: {e2}")
        
        raise
