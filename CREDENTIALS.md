# Security & Credentials Setup Guide

## ⚠️ Important: Protecting Sensitive Credentials

This repository uses APIs that require authentication:
- **NASA Earthdata** - For SWOT satellite data
- **Google Earth Engine** - For Sentinel-2 imagery

Your credentials should **NEVER** be committed to the repository.

## NASA Earthdata Setup

### Step 1: Create Account
1. Go to https://urs.earthdata.nasa.gov/
2. Create a free account
3. Note your username and password

### Step 2: Setup .netrc File

Create `~/.netrc` in your home directory:

```bash
# Linux/Mac
nano ~/.netrc
```

Add this content (replace YOUR_USERNAME and YOUR_PASSWORD):
```
machine urs.earthdata.nasa.gov
    login YOUR_USERNAME
    password YOUR_PASSWORD
```

Set proper permissions (IMPORTANT!):
```bash
chmod 600 ~/.netrc
```

### Step 3: Verify
```bash
# Test authentication
python -c "import earthaccess; auth = earthaccess.login(strategy='netrc'); print('✓ Authenticated!');"
```

## Google Earth Engine Setup

### Option A: Service Account (Recommended for Automation)

**Step 1: Create Google Cloud Project**
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable Earth Engine API

**Step 2: Create Service Account**
1. Go to "Service Accounts" in IAM & Admin
2. Create a new service account
3. Create a JSON key
4. Download the JSON file

**Step 3: Place Credentials**
```bash
# Copy the downloaded JSON to your repository
# Rename it to one of these (they're in .gitignore):
cp ~/Downloads/YOUR_KEY.json /path/to/SWOT_CooperFlood/gee-credentials.json
```

**Step 4: Update Notebook**
In cell 7 of the notebook, update the path:
```python
credentials_path = '/path/to/gee-credentials.json'
```

### Option B: Interactive Authentication (One-time per machine)

Run in the notebook:
```python
import ee
ee.Authenticate()
ee.Initialize()
```

This opens a browser to authenticate and saves credentials locally.

## File Locations

### NASA Earthdata
- **File**: `~/.netrc`
- **Location**: Your home directory (Linux/Mac)
- **Windows**: `C:\Users\YOUR_USER\_netrc`

### Google Earth Engine
- **File**: `gee-credentials.json` (your choice of name)
- **Location**: Anywhere on your machine (update path in notebook)
- **Recommended**: Keep in a secure location, NOT in the repository

## Security Best Practices

### ✅ DO
- Store credentials outside the repository
- Use strong, unique passwords
- Regularly rotate API keys
- Keep credentials in `~/.netrc` or `~` directory
- Set file permissions to 600 for `.netrc`

### ❌ DON'T
- Commit `.netrc` or JSON credentials to Git
- Share credentials publicly
- Use credentials in code strings
- Post credentials in issues or discussions
- Commit credentials "by mistake"

## Template Files

This repository includes templates to help setup:
- `_netrc.template` - Template for NASA Earthdata credentials
- `gee-credentials.template.json` - Template for GEE service account

Use these as reference when setting up your own credentials.

## Troubleshooting

### "No .netrc found" Error
```bash
# Create the file
touch ~/.netrc
chmod 600 ~/.netrc
# Add credentials (see above)
```

### "Permission denied" for .netrc
```bash
# Fix permissions
chmod 600 ~/.netrc
```

### GEE Authentication Failed
```python
# Authenticate interactively
import ee
ee.Authenticate()
ee.Initialize()
```

### Credentials in Git History

If you accidentally committed credentials:

1. **Remove from current version**:
   ```bash
   git rm --cached .netrc gee-credentials.json
   ```

2. **Remove from history** (careful!):
   ```bash
   git filter-branch --tree-filter 'rm -f .netrc gee-credentials.json' HEAD
   git push origin --force-with-lease
   ```

3. **Rotate credentials immediately**:
   - Change NASA Earthdata password
   - Create new GEE service account and delete old one

## Need Help?

- NASA Earthdata Support: https://urs.earthdata.nasa.gov/
- GEE Sign Up: https://earthengine.google.com/
- GEE Documentation: https://developers.google.com/earth-engine

---

**Remember**: Credentials = Keys to your data. Protect them! 🔐
