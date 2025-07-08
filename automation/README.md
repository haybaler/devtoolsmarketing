# 🤖 Simple Developer Tools Automation

> Get **copy-paste ready** newsletter content every Monday morning with minimal setup!

## 🎯 What You Get

Every **other day at 10 AM UTC** (Mon, Wed, Fri, Sun), you'll automatically receive:
- 📧 **Copy-paste ready newsletter content** 
- 🔥 **Trending developer tools** from GitHub
- 💰 **Latest funding news** and market insights
- 📊 **Real data** from live GitHub repositories

## 🚀 Super Simple Setup (2 minutes)

### Step 1: Optional AI Enhancement
Choose your preferred AI service (or use both for redundancy):

#### Option A: NVIDIA NIM (Recommended - Fast & Cheap)
1. Go to [NVIDIA Build](https://build.nvidia.com/)
2. Sign up for free account
3. Get API key for Llama 3.1 405B model
4. In your GitHub repository, go to **Settings > Secrets and Variables > Actions**
5. Add secret: `NVIDIA_API_KEY` with your key

**Cost**: Often cheaper than OpenAI, great free tier

#### Option B: OpenAI (Classic Choice)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new key
3. In your GitHub repository, go to **Settings > Secrets and Variables > Actions**
4. Add secret: `OPENAI_API_KEY` with your key

**Cost**: ~$5-20/month depending on usage

### Step 2: That's It!
The automation runs automatically every other day. No other setup needed!

## 📅 How It Works

### Every Other Day at 10 AM UTC (Mon, Wed, Fri, Sun):
1. **🤖 Automation runs** - Finds trending developer tools
2. **🧠 AI generates content** - Uses NVIDIA NIM or OpenAI for enhanced content
3. **📧 Issue created** - GitHub issue with copy-paste ready content
4. **🔔 You get notified** - Check your GitHub notifications

### Your Action (30 seconds):
1. **Open** the GitHub issue labeled "Newsletter Ready"
2. **Copy** the content from the issue
3. **Paste** into your newsletter editor
4. **Send** to your subscribers!

## 🎨 What the Content Looks Like

```
🔥 Developer Tools Weekly - Week 28

Hey there!

This week's developer tools scene is absolutely buzzing! Cursor just raised $900M Series C at a $9.9B valuation - making it one of the most valuable dev tools ever! 🚀

🌟 FEATURED TOOL: Cursor
AI-native code editor that raised $900M
Why it's hot: Revolutionary AI-first approach to coding

📈 TRENDING ON GITHUB:
1. Cline - 47,174 ⭐ - Autonomous coding agent
2. Daytona - 20,927 ⭐ - Secure infrastructure for AI-generated code
3. Onlook - 20,479 ⭐ - Visual editor for designers

💡 MARKET INSIGHT:
AI-native development tools attracting record investments

Keep building! 🚀
[Your Name]
```

## 🛠️ Manual Testing

Want to test it right now? Run:

```bash
python3 automation/simple_automation.py
```

## 🔧 Files Created

- `newsletter/auto-generated-week-X-2025.md` - Full newsletter content
- GitHub Issue - Copy-paste ready version with formatting

## 💰 Costs

- **GitHub Actions**: FREE
- **GitHub API**: FREE  
- **NVIDIA NIM API**: FREE tier available, very cheap paid tiers
- **OpenAI API**: ~$5-20/month (optional alternative)
- **Total**: $0-20/month (often $0 with NVIDIA NIM free tier)

## 🎯 Benefits

- **95% time savings** - From 15 hours/week to 30 seconds/week
- **Never miss trending tools** - Automatic discovery
- **Consistent quality** - Same format every week
- **Real data** - Live GitHub metrics
- **Professional content** - Ready for your audience

## 🔄 Customization

Want to customize the content? Edit:
- `automation/simple_automation.py` - Main script
- `get_manual_weekly_highlights()` - Weekly featured tools
- `.github/workflows/weekly-newsletter.yml` - Automation schedule

## 📞 Support

If something breaks:
1. Check GitHub Actions tab for errors
2. Manual run: `python3 automation/simple_automation.py`
3. Check the generated content quality

---

**🎉 You're all set!** Your first automated newsletter will be ready on the next scheduled day (Mon, Wed, Fri, or Sun) at 10 AM UTC!