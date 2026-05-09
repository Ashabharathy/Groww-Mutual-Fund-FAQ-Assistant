import asyncio
import json
import os
from playwright.async_api import async_playwright

URLS_FILE = os.path.join(os.path.dirname(__file__), 'subphase1_1_urls.json')
RAW_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'phase1_raw')

async def scrape_url(page, url):
    print(f"[Subphase 1.2] Scraping: {url}")
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(3000) # Wait for React render
        
        # Extract title for scheme name
        title = await page.title()
        scheme_name = title.split('-')[0].strip() if '-' in title else title
        
        # Get the fully rendered HTML
        html_content = await page.content()
        return html_content, scheme_name, url
    except Exception as e:
        print(f"[Subphase 1.2] Failed to scrape {url}: {e}")
        return None, "Unknown Scheme", url

async def extract_all():
    print("[Subphase 1.2] Starting Raw Data Extraction...")
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(URLS_FILE, 'r', encoding='utf-8') as f:
        urls = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        for url in urls:
            html_content, scheme_name, source_url = await scrape_url(page, url)
            if html_content:
                safe_name = scheme_name.replace(' ', '_').replace('/', '_').replace(':', '_')
                file_path = os.path.join(RAW_DIR, f"{safe_name}.html")
                
                # Save both html and a metadata file for the next phase
                with open(file_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(html_content)
                with open(file_path.replace('.html', '_meta.json'), 'w', encoding='utf-8') as meta_f:
                    json.dump({"source_url": source_url, "scheme_name": scheme_name}, meta_f)
                    
                print(f"[Subphase 1.2] Saved {file_path}")
            await asyncio.sleep(1)
            
        await browser.close()
    print("[Subphase 1.2] Extraction Complete.\n")

if __name__ == "__main__":
    asyncio.run(extract_all())
