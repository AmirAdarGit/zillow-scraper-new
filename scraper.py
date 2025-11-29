# scraper.py
"""
Handles communication with Nimble API
"""

import requests
import json
from config import NIMBLE_BASE64_TOKEN, NIMBLE_API_URL, ZILLOW_SEARCH_URL


class NimbleScraper:
    """Wrapper for Nimble Web API"""
    
    def __init__(self):
        self.api_url = NIMBLE_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {NIMBLE_BASE64_TOKEN}"
        }
    
    def fetch_page(self, url, render=True, wait_time=5000):
        """
        Fetch a webpage through Nimble API with page interactions
        
        Args:
            url (str): Target URL to scrape
            render (bool): Enable JavaScript rendering
            wait_time (int): Time to wait in milliseconds for page to load (default 5000ms = 5s)
            
        Returns:
            dict: Response containing HTML and metadata
        """
        payload = {
            "url": url,
            "render": render,
            "country": "US"
        }
        
        
        try:
            print(f"Fetching: {url[:100]}...")  # Print first 100 chars
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120  # Increased timeout for render_flow
            )
            
            print(f"Response Status Code: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            print(json.dumps(data, indent=2)[:2000])
            print(f"API Status: {data.get('status')}")
            
            # Print render_flow results if available
            if "render_flow" in data:
                print(f"Render Flow Status: {data['render_flow'].get('success')}")
            
            return data
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response text: {response.text[:500]}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return None
    
    def fetch_all_pages(self, base_url, max_pages=10):
        """
        Fetch all pages from Zillow SPA by manipulating searchQueryState pagination
        
        Args:
            base_url (str): Initial URL to start scraping
            max_pages (int): Maximum number of pages to fetch (safety limit)
            
        Returns:
            list: List of response dicts, one per page
        """
        from bs4 import BeautifulSoup
        
        all_pages = []
        
        for page_num in range(1, max_pages + 1):
            print(f"\n{'='*60}")
            print(f"📄 Fetching Page {page_num}")
            print(f"{'='*60}")
            
            # For page 1, just fetch normally
            # For page 2+, we'll use the SPA pagination approach
            if page_num == 1:
                result = self.fetch_page(base_url, render=True, wait_time=5000)
            else:
                # Try to manipulate the SPA state
                # Since we can't execute JS with Nimble's current render_flow,
                # we need to build the URL with the pagination state included
                result = self.fetch_page_with_url_state(base_url, page_num)
            
            if not result:
                print(f"❌ Failed to fetch page {page_num}")
                break
            
            all_pages.append({
                'page_number': page_num,
                'url': base_url,
                'data': result
            })
            
            # Extract HTML content
            html = (
                result.get("html_content") or
                result.get("rendered_html") or
                result.get("browser_html") or
                result.get("html")
            )
            
            if not html:
                print("❌ No HTML content found")
                break
            
            # Check if there's a next page button (to know when to stop)
            soup = BeautifulSoup(html, 'html.parser')
            next_link = soup.find('a', rel='next')
            
            if not next_link or next_link.get('aria-disabled') == 'true':
                print(f"✅ No more pages available. Total pages scraped: {page_num}")
                break
            
            print(f"➡️  Next page available, continuing to page {page_num + 1}")
        
        print(f"\n{'='*60}")
        print(f"✅ Completed scraping {len(all_pages)} pages")
        print(f"{'='*60}\n")
        
        return all_pages
    
    def fetch_page_with_url_state(self, base_url, page_number):
        """
        Fetch a specific page by modifying the searchQueryState in the URL
        
        Args:
            base_url (str): Base URL with searchQueryState
            page_number (int): Page number to fetch
            
        Returns:
            dict: Response from Nimble API
        """
        import json
        from urllib.parse import parse_qs, urlparse, urlencode, urlunparse
        
        # Parse the URL
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        
        # Get the searchQueryState
        if 'searchQueryState' in query_params:
            import urllib.parse
            state_json = urllib.parse.unquote(query_params['searchQueryState'][0])
            state = json.loads(state_json)
            
            # Add/update pagination
            state['pagination'] = {'currentPage': page_number}
            
            # Rebuild URL
            new_state_json = json.dumps(state)
            new_state_encoded = urllib.parse.quote(new_state_json)
            
            # Update path to include page number (cosmetic but matches Zillow's pattern)
            path_parts = parsed.path.rstrip('/').split('/')
            # Remove any existing pagination path (like /2_p/)
            path_parts = [p for p in path_parts if not p.endswith('_p')]
            
            if page_number > 1:
                # Add pagination path
                path_parts.append(f'{page_number}_p')
            
            new_path = '/'.join(path_parts) + '/'
            
            # Build new URL
            new_url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                new_path,
                '',
                f'searchQueryState={new_state_encoded}',
                ''
            ))
            
            print(f"🔗 Modified URL for page {page_number}")
            return self.fetch_page(new_url, render=True, wait_time=5000)
        else:
            print("⚠️  No searchQueryState found in URL")
            return self.fetch_page(base_url, render=True, wait_time=5000)


def build_zillow_url():
    """
    Use the exact working URL from browser
    """
    return ZILLOW_SEARCH_URL



# Test the scraper
if __name__ == "__main__":
    scraper = NimbleScraper()
    
    # Test with the actual Zillow URL
    print("=== Testing Zillow Scraper with Pagination ===\n")
    zillow_url = build_zillow_url()
    
    # Option 1: Fetch single page
    print("Option 1: Single page fetch")
    result = scraper.fetch_page(zillow_url, render=True)

    if result:
        html = (
            result.get("html_content") or
            result.get("rendered_html") or
            result.get("browser_html") or
            result.get("html")
        )

        if html:
            print("✅ Successfully fetched Zillow page!")
            print(f"HTML length: {len(html)} characters")

            with open("zillow_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("💾 Saved to zillow_page.html")
        else:
            print("❌ Nimble returned no usable HTML")
    else:
        print("❌ Failed to fetch Zillow page")
    
    print("\n" + "="*60)
    print("Option 2: Fetch all pages with pagination")
    print("="*60 + "\n")
    
    # Option 2: Fetch all pages with pagination
    all_pages = scraper.fetch_all_pages(zillow_url, max_pages=5)
    
    if all_pages:
        print(f"\n✅ Successfully fetched {len(all_pages)} pages!")
        
        # Save each page's HTML
        for page_info in all_pages:
            page_num = page_info['page_number']
            html = (
                page_info['data'].get("html_content") or
                page_info['data'].get("rendered_html") or
                page_info['data'].get("browser_html") or
                page_info['data'].get("html")
            )
            
            if html:
                filename = f"zillow_page_{page_num}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"💾 Saved page {page_num} to {filename}")
    else:
        print("❌ Failed to fetch pages")
