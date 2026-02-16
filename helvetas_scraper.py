#!/usr/bin/env python3
"""
Helvetas Job Scraper
Scrapes job listings from Helvetas Switzerland and generates RSS feed
Format: ADB-compatible for cinfoposte portal
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import hashlib
import xml.sax.saxutils as saxutils

BASE_URL = "https://www.helvetas.org"
JOBS_URL = f"{BASE_URL}/de/schweiz/wer-wir-sind/jobs"

def setup_driver():
    """Set up Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # CRITICAL: Use system chromedriver for GitHub Actions
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def generate_numeric_id(url):
    """Generate unique numeric ID from URL for guid"""
    hash_object = hashlib.md5(url.encode())
    hex_dig = hash_object.hexdigest()
    # Use 12 characters to reduce collisions
    numeric_id = int(hex_dig[:12], 16) % 100000000
    return str(numeric_id)

def get_existing_job_links(feed_file='helvetas_jobs.xml'):
    """Extract job links from existing RSS feed to avoid duplicates"""
    existing_links = set()
    
    if not os.path.exists(feed_file):
        print("No existing feed found - all jobs will be considered new")
        return existing_links
    
    try:
        tree = ET.parse(feed_file)
        root = tree.getroot()
        
        for item in root.findall('.//item'):
            link_elem = item.find('link')
            if link_elem is not None and link_elem.text:
                existing_links.add(link_elem.text.strip())
        
        print(f"Found {len(existing_links)} existing jobs in previous feed")
        
    except Exception as e:
        print(f"Error reading existing feed: {str(e)}")
        print("Will treat all jobs as new")
    
    return existing_links

def scrape_jobs():
    """Scrape job listings from Helvetas website"""
    print(f"Starting scraper for: {JOBS_URL}")
    driver = setup_driver()
    jobs = []

    try:
        driver.get(JOBS_URL)
        print("Page loaded, waiting for content...")
        time.sleep(5)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all job headings (h3 elements that contain job titles)
        job_headings = soup.find_all('h3')
        
        print(f"Processing {len(job_headings)} potential job listings...")
        
        for heading in job_headings:
            try:
                # Find the link within or near the heading
                link = heading.find('a')
                
                if not link:
                    continue
                
                # Get job title
                title = link.get_text(strip=True)
                
                # Skip if title is empty or too short
                if not title or len(title) < 5:
                    continue
                
                # Get job URL
                href = link.get('href')
                if not href:
                    continue
                    
                # Make URL absolute
                if href.startswith('/'):
                    job_url = BASE_URL + href
                elif not href.startswith('http'):
                    job_url = BASE_URL + '/' + href
                else:
                    job_url = href
                
                # Only process if it's a job posting link
                if '/jobs/' not in job_url or '_job_' not in job_url:
                    continue
                
                # Try to find location and date
                location = "Zürich, Schweiz"  # Default location
                date_posted = ""
                
                # Look at previous siblings (location is typically before the heading)
                parent = heading.find_parent()
                if parent:
                    # Location is often in a text element before the h3
                    prev_elements = parent.find_previous_siblings()
                    for elem in prev_elements[:3]:
                        text = elem.get_text(strip=True)
                        # Check if it looks like a location (contains comma or country name)
                        if text and (',' in text or 'Switzerland' in text or 'Schweiz' in text):
                            location = text
                            break
                    
                    # Date is often in a text element before the heading
                    for elem in prev_elements[:5]:
                        text = elem.get_text(strip=True)
                        # Check if it's a date (contains year)
                        if any(year in text for year in ['2024', '2025', '2026', '2027']):
                            date_posted = text
                            break
                
                # Build description with HTML escaping
                description = f"Helvetas has a vacancy for the position of {title}."
                if location and location != "Zürich, Schweiz":
                    description += f" Location: {location}."
                if date_posted:
                    description += f" Posted: {date_posted}."
                
                # Escape HTML characters
                description = saxutils.escape(description)
                
                jobs.append({
                    'title': title,
                    'link': job_url,
                    'description': description
                })
                
                print(f"  [OK] {title}")
                
            except Exception as e:
                print(f"  [ERROR] Error processing heading: {str(e)}")
                continue
        
        print(f"\nSuccessfully scraped {len(jobs)} jobs")
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    
    finally:
        driver.quit()
    
    return jobs

def generate_rss_feed(jobs, output_file='helvetas_jobs.xml'):
    """Generate RSS 2.0 feed in ADB-compatible format"""
    
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xml:base', BASE_URL)
    
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = 'Helvetas Job Vacancies'
    ET.SubElement(channel, 'link').text = JOBS_URL
    ET.SubElement(channel, 'description').text = 'List of vacancies at Helvetas Swiss Intercooperation'
    ET.SubElement(channel, 'language').text = 'de'
    
    # CRITICAL: Use RFC-822 format for pubDate
    current_time = datetime.utcnow()
    ET.SubElement(channel, 'pubDate').text = current_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    for job in jobs:
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = job['title']
        ET.SubElement(item, 'link').text = job['link']
        ET.SubElement(item, 'description').text = job['description']
        
        # CRITICAL: guid must have isPermaLink="false" and be numeric
        guid = ET.SubElement(item, 'guid')
        guid.set('isPermaLink', 'false')
        guid.text = generate_numeric_id(job['link'])
        
        # CRITICAL: Use RFC-822 format
        ET.SubElement(item, 'pubDate').text = current_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # CRITICAL: source tag with url attribute
        source = ET.SubElement(item, 'source')
        source.set('url', JOBS_URL)
        source.text = 'Helvetas Job Vacancies'
    
    # Pretty print XML
    xml_string = ET.tostring(rss, encoding='unicode')
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # Remove extra blank lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"\n[SUCCESS] RSS feed generated: {output_file}")
    print(f"  Total jobs in feed: {len(jobs)}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("Helvetas Job Scraper")
    print("=" * 60)
    
    # Get existing jobs to avoid duplicates
    existing_links = get_existing_job_links()
    
    # Scrape all jobs
    all_jobs = scrape_jobs()
    
    # Filter for new jobs only
    new_jobs = [job for job in all_jobs if job['link'] not in existing_links]
    
    print("\n" + "=" * 60)
    print(f"Total jobs found: {len(all_jobs)}")
    print(f"New jobs (not in previous feed): {len(new_jobs)}")
    print(f"Existing jobs (skipped): {len(all_jobs) - len(new_jobs)}")
    print("=" * 60)
    
    if new_jobs:
        generate_rss_feed(new_jobs)
        print("\n[SUCCESS] Feed updated with new jobs!")
        
        print("\nNew jobs added to feed:")
        for i, job in enumerate(new_jobs, 1):
            print(f"  {i}. {job['title']}")
    else:
        print("\n[INFO] No new jobs found - feed not updated")
        if not os.path.exists('helvetas_jobs.xml'):
            print("[INFO] Creating empty feed file")
            generate_rss_feed([])
    
    print("=" * 60)

if __name__ == "__main__":
    main()
