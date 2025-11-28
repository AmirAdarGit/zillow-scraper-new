#!/usr/bin/env python3
"""
Zillow Multi-Page Scraper with Pagination
Automatically detects and fetches all available pages
"""

import json
from scraper import NimbleScraper, build_zillow_url
from parser import ZillowParser


def scrape_all_pages_and_parse(base_url, max_pages=10):
    """
    Scrape all Zillow pages and parse the listings
    
    Args:
        base_url (str): Starting URL for Zillow search
        max_pages (int): Maximum number of pages to scrape
        
    Returns:
        tuple: (all_listings, summary_stats)
    """
    print("🏠 Starting Zillow Multi-Page Scraper")
    print("="*60)
    
    # Initialize scraper
    scraper = NimbleScraper()
    
    # Fetch all pages
    print(f"\n📥 Fetching up to {max_pages} pages...")
    all_pages = scraper.fetch_all_pages(base_url, max_pages=max_pages)
    
    if not all_pages:
        print("❌ No pages were fetched")
        return [], {}
    
    print(f"\n✅ Fetched {len(all_pages)} pages")
    print("\n" + "="*60)
    print("📊 Parsing listings from all pages...")
    print("="*60)
    
    # Parse all pages and collect listings
    all_listings = []
    page_summaries = []
    
    for page_info in all_pages:
        page_num = page_info['page_number']
        page_url = page_info['url']
        page_data = page_info['data']
        
        print(f"\n📄 Parsing Page {page_num}...")
        
        # Extract HTML
        html = (
            page_data.get("html_content") or
            page_data.get("rendered_html") or
            page_data.get("browser_html") or
            page_data.get("html")
        )
        
        if not html:
            print(f"⚠️  No HTML found for page {page_num}")
            continue
        
        # Parse listings using static method
        listings = ZillowParser.parse_listings(html)
        
        # Add page number to each listing
        for listing in listings:
            listing['page_number'] = page_num
            listing['page_url'] = page_url
        
        all_listings.extend(listings)
        
        print(f"✅ Found {len(listings)} listings on page {page_num}")
        print(f"   Total so far: {len(all_listings)} listings")
        
        # Store page summary
        page_summaries.append({
            'page': page_num,
            'url': page_url,
            'listings_count': len(listings)
        })
    
    # Calculate summary statistics
    print("\n" + "="*60)
    print("📈 Calculating statistics...")
    print("="*60)
    
    summary_stats = {
        'total_pages': len(all_pages),
        'total_listings': len(all_listings),
        'pages': page_summaries
    }
    
    if all_listings:
        # Helper function to convert to numeric
        def to_number(val):
            """Convert value to number, handling strings and None"""
            if val is None:
                return None
            if isinstance(val, (int, float)):
                return val
            if isinstance(val, str):
                # Remove currency symbols and commas
                cleaned = val.replace('$', '').replace(',', '').strip()
                try:
                    return float(cleaned)
                except (ValueError, AttributeError):
                    return None
            return None
        
        # Price statistics
        prices = [to_number(l.get('price')) for l in all_listings]
        prices = [p for p in prices if p is not None and p > 0]
        if prices:
            summary_stats['price_stats'] = {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices)
            }
        
        # Beds statistics
        beds = [to_number(l.get('beds')) for l in all_listings]
        beds = [b for b in beds if b is not None and b > 0]
        if beds:
            summary_stats['beds_stats'] = {
                'min': min(beds),
                'max': max(beds),
                'average': sum(beds) / len(beds)
            }
        
        # Baths statistics
        baths = [to_number(l.get('baths')) for l in all_listings]
        baths = [b for b in baths if b is not None and b > 0]
        if baths:
            summary_stats['baths_stats'] = {
                'min': min(baths),
                'max': max(baths),
                'average': sum(baths) / len(baths)
            }
    
    return all_listings, summary_stats


def save_results(listings, stats, prefix="zillow_multi_page"):
    """Save results to JSON and CSV files"""
    import pandas as pd
    
    print(f"\n💾 Saving results...")
    
    # Save JSON
    json_file = f"output/{prefix}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(listings)} listings to {json_file}")
    
    # Save CSV
    if listings:
        csv_file = f"output/{prefix}.csv"
        df = pd.DataFrame(listings)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"✅ Saved to {csv_file}")
    
    # Save stats
    stats_file = f"output/{prefix}_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved statistics to {stats_file}")


def main():
    """Main execution function"""
    
    # Get the base URL
    base_url = build_zillow_url()
    
    print(f"\n🔗 Base URL: {base_url[:100]}...")
    print(f"\n⚙️  Configuration:")
    print(f"   - Max pages: 10")
    print(f"   - Wait time per page: 5 seconds")
    print(f"   - Auto-detect pagination: ON")
    
    # Scrape and parse all pages
    listings, stats = scrape_all_pages_and_parse(base_url, max_pages=10)
    
    # Print results
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    print(f"✅ Total Pages Scraped: {stats.get('total_pages', 0)}")
    print(f"✅ Total Listings Found: {stats.get('total_listings', 0)}")
    
    if 'price_stats' in stats:
        print(f"\n💰 Price Range:")
        print(f"   Min: ${stats['price_stats']['min']:,.0f}")
        print(f"   Max: ${stats['price_stats']['max']:,.0f}")
        print(f"   Avg: ${stats['price_stats']['average']:,.0f}")
    
    if 'beds_stats' in stats:
        print(f"\n🛏️  Bedrooms:")
        print(f"   Min: {stats['beds_stats']['min']}")
        print(f"   Max: {stats['beds_stats']['max']}")
        print(f"   Avg: {stats['beds_stats']['average']:.1f}")
    
    if listings:
        # Save results
        save_results(listings, stats)
        
        print("\n" + "="*60)
        print("🎉 Scraping Complete!")
        print("="*60)
        
        # Show sample listings
        print(f"\n📋 Sample Listings (first 3):")
        for i, listing in enumerate(listings[:3], 1):
            price = listing.get('price', 'N/A')
            price_str = f"${price:,}" if isinstance(price, (int, float)) else str(price)
            
            print(f"\n{i}. {listing.get('address', 'N/A')}")
            print(f"   💰 {price_str}/mo")
            print(f"   🛏️  {listing.get('beds', 'N/A')} bed | 🚿 {listing.get('baths', 'N/A')} bath | 📐 {listing.get('sqft', 'N/A')} sqft")
            print(f"   📄 Page: {listing.get('page_number', 'N/A')}")
    else:
        print("\n❌ No listings found")


if __name__ == "__main__":
    main()

