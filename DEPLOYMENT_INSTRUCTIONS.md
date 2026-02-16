# Helvetas Job Scraper - Deployment Instructions

## Step-by-Step Setup

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `helvetas-jobs`
3. Description: `Automated RSS feed for Helvetas job vacancies`
4. **Visibility:** Public (required for free GitHub Actions)
5. ✅ Initialize with README (optional - we have our own)
6. Click "Create repository"

### 2. Configure Repository Settings

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **"Workflow permissions"**
3. Select: ☑️ **"Read and write permissions"**
4. Click **"Save"**

### 3. Upload Files

Upload these 4 files to your repository:

**File 1:** `helvetas_scraper.py`
- Location: Root directory
- Content: The Python scraper script

**File 2:** `.github/workflows/update-helvetas-feed.yml`
- Location: Create folder `.github/workflows/` first
- Content: The GitHub Actions workflow

**File 3:** `requirements.txt`
- Location: Root directory
- Content: Python dependencies

**File 4:** `README.md`
- Location: Root directory
- Content: Documentation

### 4. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under "Source", select: **Deploy from a branch**
3. Branch: **master** (or **main**)
4. Folder: **/ (root)**
5. Click **"Save"**

### 5. First Test Run

1. Go to **Actions** tab
2. You should see "Update Helvetas Job Feed" workflow
3. Click on it
4. Click **"Run workflow"** (top right)
5. Click the green **"Run workflow"** button
6. Wait 30-60 seconds
7. Click on the running workflow to see logs

### 6. Verify Success

**Check 1: Workflow succeeded**
- Should show green checkmark ✅
- No red X ❌

**Check 2: XML file created**
- Go to repository main page
- You should see `helvetas_jobs.xml` file
- Click on it to view contents

**Check 3: GitHub Pages deployed**
- Go to **Settings** → **Pages**
- You should see: "Your site is live at https://[username].github.io/helvetas-jobs/"
- Click the link
- Add `/helvetas_jobs.xml` to the URL
- You should see the RSS feed XML

### 7. Get Your Feed URL

Your RSS feed URL will be:
```
https://[your-github-username].github.io/helvetas-jobs/helvetas_jobs.xml
```

Replace `[your-github-username]` with your actual GitHub username.

### 8. Validate Feed

1. Go to https://validator.w3.org/feed/
2. Paste your feed URL
3. Click "Check"
4. Should show: "This is a valid RSS feed"

### 9. Import into Portal

Use the feed URL to import into your cinfoposte portal:

**Field Mappings:**
- CHANNEL → channel
- TITLE → title
- LINK → link
- DESCRIPTION → description
- ITEMS → item

**Item Mappings:**
- Title → title
- Link → link
- Description → description
- Date → pubDate
- Unique ID → guid

## Troubleshooting

### Error: Permission denied (Exit code 128)

**Fix:**
1. Settings → Actions → General
2. Workflow permissions → "Read and write permissions"
3. Save

### Error: ChromeDriver not found

**Fix:** Make sure workflow YAML includes:
```yaml
- name: Set up Chrome
  uses: browser-actions/setup-chrome@latest
```

### Feed shows 0 jobs

**Check:**
1. View workflow logs (Actions tab)
2. Look for "Successfully scraped X jobs"
3. If 0 jobs found, Helvetas page structure may have changed

### Feed validation fails

**Common issues:**
- pubDate format must be RFC-822
- guid must have `isPermaLink="false"`
- HTML characters must be escaped

## Maintenance

### Update Schedule

Automatic runs:
- Mondays at 6 AM UTC
- Thursdays at 6 AM UTC

Manual trigger:
- Actions → Update Helvetas Job Feed → Run workflow

### Monitoring

Check workflow runs:
1. Go to Actions tab
2. View recent runs
3. Green ✅ = success
4. Red ❌ = failure (click to see logs)

## Next Steps

After successful deployment:

1. ✅ Test feed in RSS reader
2. ✅ Import into cinfoposte portal
3. ✅ Monitor first few automatic runs
4. ✅ Share feed URL with team

---

**Questions?** Check the logs in the Actions tab or consult the Scraper Manual.
