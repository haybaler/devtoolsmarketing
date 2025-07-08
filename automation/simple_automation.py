#!/usr/bin/env python3
"""
Simple Developer Tools Directory Automation
Requires only 2 API keys: GitHub (free) + OpenAI (cheap)
Generates copy-paste ready newsletter content
"""

import os
import sys
import json
import requests
import datetime
from typing import Dict, List, Any

class SimpleAutomation:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')  # Free GitHub API
        self.openai_key = os.getenv('OPENAI_API_KEY')   # OpenAI API (~$20/month)
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY')  # NVIDIA NIM API
        
    def get_trending_repos(self) -> List[Dict]:
        """Get trending developer tools from GitHub (FREE API)"""
        
        # Search for trending developer tools repositories
        queries = [
            "developer tools",
            "code editor",
            "IDE",
            "AI coding",
            "development automation"
        ]
        
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
        
        # Remove duplicates and sort by stars
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
        
        # Simple prompt for AI
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
        
        # Try NVIDIA NIM first (often faster and cheaper)
        if self.nvidia_api_key:
            try:
                return self.generate_with_nvidia_nim(prompt)
            except Exception as e:
                print(f"NVIDIA NIM API error: {e}, falling back to OpenAI...")
        
        # Try OpenAI if NVIDIA NIM fails or not available
        if self.openai_key:
            try:
                return self.generate_with_openai(prompt)
            except Exception as e:
                print(f"OpenAI API error: {e}, using fallback...")
        
        # Use fallback if no AI APIs available
        return self.generate_fallback_newsletter(github_data, highlights)
    
    def generate_with_nvidia_nim(self, prompt: str) -> str:
        """Generate content using NVIDIA NIM API"""
        import requests
        
        # NVIDIA NIM API endpoint (you can use various models)
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.nvidia_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta/llama-3.1-405b-instruct",  # Fast and good model
            "messages": [
                {"role": "system", "content": "You are a tech newsletter writer who creates engaging, concise content about developer tools."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
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
            print("OpenAI package not installed. Using fallback newsletter generation.")
            raise ImportError("OpenAI package not available")
        
        openai.api_key = self.openai_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cheaper than GPT-4
            messages=[
                {"role": "system", "content": "You are a tech newsletter writer who creates engaging, concise content about developer tools."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
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

🔗 QUICK LINKS:
• Full Directory: https://github.com/haybaler/devtoolsmarketing
• AI Tools: https://github.com/haybaler/devtoolsmarketing/tree/main/tools/ai-powered-development
• Editors & IDEs: https://github.com/haybaler/devtoolsmarketing/tree/main/tools/editors-ides

What's your favorite new tool this week? Hit reply and let me know! 

Keep building! 🚀
[Your Name]

P.S. Forward this to a fellow developer who'd love these discoveries!
"""
        
        return newsletter
    
    def run_weekly_automation(self):
        """Main automation function - run this weekly"""
        
        print("🤖 Starting Simple Developer Tools Automation...")
        print("=" * 50)
        
        # Step 1: Get GitHub trending data (FREE)
        print("📊 Fetching GitHub trending repositories...")
        github_trending = self.get_trending_repos()
        print(f"✅ Found {len(github_trending)} trending tools")
        
        # Step 2: Get manual highlights (NO API)
        print("🎯 Loading weekly highlights...")
        highlights = self.get_manual_weekly_highlights()
        print("✅ Weekly highlights loaded")
        
        # Step 3: Generate newsletter (CHEAP - ~$0.05)
        print("📝 Generating newsletter content...")
        if self.openai_key:
            newsletter_content = self.generate_newsletter_with_ai(github_trending, highlights)
        else:
            newsletter_content = self.generate_fallback_newsletter(github_trending, highlights)
        print("✅ Newsletter generated!")
        
        # Step 4: Save and display
        week_num = datetime.datetime.now().isocalendar()[1]
        filename = f"newsletter/auto-generated-week-{week_num}-2025.md"
        
        os.makedirs("newsletter", exist_ok=True)
        with open(filename, 'w') as f:
            f.write(newsletter_content)
        
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

# Simple setup instructions
def setup_instructions():
    print("""
🚀 SIMPLE AUTOMATION SETUP (2 minutes)

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
   • python automation/simple_automation.py

That's it! You'll get copy-paste ready newsletter content! 🎯
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_instructions()
    else:
        automation = SimpleAutomation()
        automation.run_weekly_automation()