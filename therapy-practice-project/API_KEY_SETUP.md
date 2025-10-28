# API Key Setup Guide

## Overview

Your Anthropic API key has been configured and is ready to use! This guide explains how the API key system works and how to manage it.

---

## Current Status

✅ **API Key Configured**

Your API key is stored in the `.env` file and will be automatically loaded by all scripts that need it.

**Location:** `/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project/.env`

**Key (masked):** `sk-ant-a...Of8RdQAA`

---

## How It Works

### 1. Configuration File (`.env`)

Your API key is stored in a `.env` file in the project directory:

```
ANTHROPIC_API_KEY=your-actual-api-key-here
```

### 2. Config Module (`config.py`)

The `config.py` module automatically loads the API key from `.env` when imported:

- Scripts import `from config import ensure_api_key`
- Config module loads `.env` file
- API key is available to all scripts

### 3. Security

- ✅ `.env` file is in `.gitignore` (won't be committed to git)
- ✅ `.env.example` provides template without actual key
- ✅ Config test shows only masked version of key
- ✅ API key is never printed in full in logs

---

## Testing Your Configuration

### Test 1: Check Configuration
```bash
python config.py
```

**Expected output:**
```
Configuration Test
============================================================
✓ API Key configured: sk-ant-a...Of8RdQAA

You're ready to use the content creation tools!
```

### Test 2: Create Sample Content
```bash
python request_social_post.py \
  --topic "Test post about mindfulness" \
  --platform Instagram \
  --use-api
```

**Expected output:**
```
SOCIAL MEDIA POST REQUEST
======================================================================

Loading content creator agent...
✓ Loaded: Mental Health Content Creator & SEO Blog Specialist

Generating prompt...
✓ Generated prompt (X,XXX characters)

Calling Claude API...

GENERATED SOCIAL MEDIA POST
======================================================================

[Your generated post content here]

Saving to content library...

✓ Content saved:
  📄 social-media-content/instagram/feed-posts/drafts/...
  📋 social-media-content/instagram/feed-posts/drafts/..._meta.json

📝 Saved as draft - use manage_content_library.py to schedule
```

---

## Files Involved

### `.env` (Your actual API key - DO NOT SHARE)
```
ANTHROPIC_API_KEY=your-api-key-here
```

### `.env.example` (Template - safe to share)
```
ANTHROPIC_API_KEY=your-api-key-here
```

### `.gitignore` (Prevents .env from being committed)
```
# API Keys and Secrets
.env
...
```

### `config.py` (Loads API key automatically)
```python
from config import ensure_api_key

api_key = ensure_api_key()  # Automatically loads from .env
```

---

## Scripts That Use the API Key

All these scripts will automatically use your configured API key:

1. **[request_social_post.py](request_social_post.py)** - Create social media posts
   ```bash
   python request_social_post.py --topic "Your topic" --use-api
   ```

2. **Future blog post creation** - When implemented
3. **Any script with `--use-api` flag**

---

## Alternative: Environment Variable

You can also set the API key as an environment variable instead of using `.env`:

### macOS/Linux:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Windows (Command Prompt):
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**Note:** Environment variable takes precedence over `.env` file.

---

## Updating Your API Key

### Method 1: Edit .env file
```bash
nano .env
# Or use any text editor
```

Change the line:
```
ANTHROPIC_API_KEY=your-new-key-here
```

### Method 2: Run setup script
```bash
python setup_api_key.py
```

Follow the prompts to update your key.

---

## Troubleshooting

### Error: "Anthropic API key not found"

**Cause:** `.env` file not found or API key not set

**Solution 1:** Check if `.env` exists
```bash
ls -la .env
```

**Solution 2:** Run setup script
```bash
python setup_api_key.py
```

**Solution 3:** Create `.env` manually
```bash
echo "ANTHROPIC_API_KEY=your-key" > .env
```

### Error: "anthropic package not installed"

**Cause:** Anthropic Python SDK not installed

**Solution:**
```bash
pip install anthropic
```

### Error: "Invalid API key"

**Cause:** API key is incorrect or expired

**Solution:**
1. Get new API key from https://console.anthropic.com/settings/keys
2. Update `.env` file with new key
3. Test with `python config.py`

### Config test shows "✗ API Key not configured"

**Possible causes:**
1. `.env` file doesn't exist
2. `.env` file is empty
3. API key format is wrong in `.env`

**Check .env format:**
```bash
cat .env
```

Should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**No spaces around `=` sign!**

---

## Security Best Practices

### ✅ DO:
- Keep `.env` file private (it's in `.gitignore`)
- Use environment variables in production
- Rotate API keys periodically
- Use separate keys for development and production
- Keep backups of your API key in a secure location

### ❌ DON'T:
- Commit `.env` to git
- Share your API key in chat/email
- Hard-code API keys in scripts
- Push API keys to GitHub/GitLab
- Store API keys in plain text in shared locations

---

## Checking API Usage

Monitor your API usage at:
https://console.anthropic.com/settings/usage

---

## Key Location Summary

| Method | Location | Priority |
|--------|----------|----------|
| Environment variable | System environment | 1st (highest) |
| .env file | Project directory | 2nd |
| Hard-coded | Not recommended | Never use |

**The config system checks in this order:**
1. Environment variable `ANTHROPIC_API_KEY`
2. `.env` file in project directory
3. Error if neither found

---

## Quick Reference

### Test configuration:
```bash
python config.py
```

### Create content with API:
```bash
python request_social_post.py --topic "Your topic" --use-api
```

### Update API key:
```bash
python setup_api_key.py
```

### View .env contents:
```bash
cat .env
```

### Edit .env:
```bash
nano .env
```

---

## Support

If you encounter issues:

1. Run configuration test: `python config.py`
2. Check `.env` file exists: `ls -la .env`
3. Verify API key format (starts with `sk-ant-`)
4. Check Anthropic console for key validity
5. Review error messages carefully

---

**Status: ✅ Your API key is configured and ready to use!**

You can now create content with:
```bash
python request_social_post.py --topic "Mindfulness techniques" --use-api
```
