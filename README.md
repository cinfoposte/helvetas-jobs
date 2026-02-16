# Helvetas Job Feed

Automated RSS feed for job vacancies at Helvetas Swiss Intercooperation.

## 📰 RSS Feed

**Feed URL:** `https://[your-username].github.io/helvetas-jobs/helvetas_jobs.xml`

Subscribe to this feed in your RSS reader to get automatic updates when new Helvetas jobs are posted.

## 🔄 Update Schedule

The feed updates automatically **twice per week**:
- Mondays at 6:00 AM UTC
- Thursdays at 6:00 AM UTC

You can also trigger an update manually via GitHub Actions.

## 🎯 What's Included

This feed includes job postings from:
- https://www.helvetas.org/de/schweiz/wer-wir-sind/jobs

Only **new jobs** (not in the previous feed) are added to prevent duplicates.

## 🛠️ Technical Details

- **Scraper:** Python + Selenium + BeautifulSoup
- **Hosting:** GitHub Actions + GitHub Pages
- **Format:** RSS 2.0 (ADB-compatible)
- **Cost:** $0 (completely free)

## 📖 Feed Format

The feed follows the ADB-compatible format for easy import into job portals:

```xml
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Helvetas Job Vacancies</title>
    <item>
      <title>Job Title</title>
      <link>https://www.helvetas.org/...</link>
      <description>Job description with location</description>
      <guid isPermaLink="false">12345678</guid>
      <pubDate>Mon, 16 Feb 2026 10:00:00 GMT</pubDate>
      <source url="...">Helvetas Job Vacancies</source>
    </item>
  </channel>
</rss>
```

## 🚀 Manual Update

To manually trigger an update:

1. Go to the **Actions** tab
2. Click **Update Helvetas Job Feed**
3. Click **Run workflow**
4. Click the green **Run workflow** button

## 📝 Maintenance

The scraper automatically:
- ✅ Detects new job postings
- ✅ Avoids duplicates
- ✅ Generates valid RSS XML
- ✅ Commits changes to the repository

No manual intervention required!

## 🔗 Related Feeds

Part of the cinfoposte job feed collection:
- IFAD Jobs
- World Bank Jobs
- Green Climate Fund Jobs
- AIIB Jobs
- IADB Jobs
- EBRD Jobs
- Helvetas Jobs (this feed)

---

**Maintained by:** cinfoposte  
**Last updated:** Check the commit history
