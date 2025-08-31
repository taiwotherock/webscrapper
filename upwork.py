import asyncio
import json
from playwright.async_api import async_playwright

COVER_LETTER_FILE = "cover_letter.txt"
NUM_JOBS_TO_SCRAPE = 20  # number of jobs you want to scrape

async def scrape_and_prefill():
    url = "https://www.upwork.com/nx/find-work/most-recent"
    results = []

    # Load cover letter
    with open(COVER_LETTER_FILE, "r", encoding="utf-8") as f:
        cover_letter_text = f.read().strip()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser = p.chromium.launch_persistent_context(
            channel="chrome", user_data_dir=r"C:\\Users\\Home\\AppData\\Local\\Google\\Chrome\\User Data", headless=False)

        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to Upwork Jobs
        await page.goto(url)
        '''
        await page.wait_for_timeout(5000)

        # Scroll to load more jobs
        previous_height = None
        while len(await page.query_selector_all('section.up-card-section')) < NUM_JOBS_TO_SCRAPE:
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break  # stop if no more content is loading
            previous_height = current_height

        # Select jobs
        jobs = await page.query_selector_all('section.up-card-section')
        print(f"Found {len(jobs)} jobs on page.")

        for i, job in enumerate(jobs[:NUM_JOBS_TO_SCRAPE]):
            try:
                title = await job.query_selector_eval('h4 a', "el => el.textContent.trim()")
                link = await job.query_selector_eval('h4 a', "el => el.href")

                # Open job detail
                await job.click()
                await page.wait_for_timeout(4000)

                # Scrape full description, country, skills
                description = await page.locator("section[data-test='job-description']").inner_text()
                country = await page.locator("strong[data-test='client-country']").inner_text()
                skills = await page.locator("li[data-test='skill'] >> text=*").all_inner_texts()

                results.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "country": country,
                    "skills": skills
                })

                print(f"✅ Scraped job {i+1}: {title} ({country})")

                # Click Apply Now and prefill cover letter
                apply_btn = await page.locator("a[data-test='job-apply-button']")
                if await apply_btn.is_visible():
                    await apply_btn.click()
                    await page.wait_for_timeout(4000)

                    textarea = page.locator("textarea[name='coverLetter']")
                    if await textarea.is_visible():
                        await textarea.fill(cover_letter_text)
                        print("📝 Cover letter pre-filled. Please review and click Submit manually.")

                # Go back to job list
                await page.go_back()
                await page.wait_for_timeout(2000)

            except Exception as e:
                print(f"Error scraping/applying job {i+1}: {e}")

        #ßawait browser.close()

    # Save job data
    with open("latest_jobs.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"🎯 Finished scraping {len(results)} jobs. Data saved to latest_jobs.json")
    '''
if __name__ == "__main__":
    asyncio.run(scrape_and_prefill())
