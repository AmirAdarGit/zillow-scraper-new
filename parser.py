# parser.py
"""
HTML parser for extracting property data from Zillow search results
"""

import json
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any


class ZillowParser:
    """Parse Zillow HTML to extract property listings"""
    
    @staticmethod
    def parse_listings(html_content: str) -> List[Dict]:
        """
        Quick static method to parse listings from HTML
        
        Args:
            html_content (str): Raw HTML from Zillow page
            
        Returns:
            List[Dict]: List of parsed property listings
        """
        parser = ZillowParser(html_content)
        return parser.parse_all_properties()
    
    def __init__(self, html_content: str = None):
        """
        Initialize parser with HTML content
        
        Args:
            html_content (str): Raw HTML from Zillow page (optional for helper methods)
        """
        self.html = html_content
        self.soup = BeautifulSoup(html_content, 'html') if html_content else None
        self.properties = []
        if html_content:
            self.export_soup_to_file()
    
    def export_soup_to_file(self, filename: str = 'parsed_soup.html') -> None:
        """
        Export the BeautifulSoup object to an HTML file
        
        Args:
            filename (str): Output filename (default: 'parsed_soup.html')
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.soup.prettify())
        print(f"✅ Exported soup to {filename}")

    def extract_json_data(self) -> Optional[Dict]:
        """
        Extract JSON data from __NEXT_DATA__ script tag
        
        Returns:
            dict: Parsed JSON data or None if not found
        """
        try:
            # Find the __NEXT_DATA__ script tag
            script_tag = self.soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
            
            if not script_tag:
                print("❌ Could not find __NEXT_DATA__ script tag")
                return None
            
            # Parse JSON content
            json_data = json.loads(script_tag.string)
            print("✅ Successfully extracted JSON data")
            return json_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Error extracting JSON data: {e}")
            return None
    
    def extract_search_results(self, json_data: Dict) -> Optional[Dict]:
        """
        Navigate through JSON structure to find search results
        
        Args:
            json_data (dict): Parsed __NEXT_DATA__ JSON
            
        Returns:
            dict: Search results data or None
        """
        try:
            # Navigate through the nested structure
            # Path: props -> pageProps -> searchPageState -> cat1 -> searchResults
            page_props = json_data.get('props', {}).get('pageProps', {})
            search_page_state = page_props.get('searchPageState', {})
            cat1 = search_page_state.get('cat1', {})
            search_results = cat1.get('searchResults', {})
            
            if not search_results:
                print("⚠️  No search results found in JSON structure")
                # Try alternative paths
                search_results = self._try_alternative_paths(json_data)
            
            return search_results
            
        except Exception as e:
            print(f"❌ Error extracting search results: {e}")
            return None
    
    def _try_alternative_paths(self, json_data: Dict) -> Optional[Dict]:
        """
        Try alternative JSON paths to find property data
        
        Args:
            json_data (dict): Full JSON data
            
        Returns:
            dict: Search results or None
        """
        # Common alternative paths in Zillow's structure
        alternative_paths = [
            ['props', 'pageProps', 'searchPageState', 'searchResults'],
            ['props', 'pageProps', 'componentProps', 'searchResults'],
            ['props', 'initialReduxState', 'searchPageState', 'cat1', 'searchResults'],
        ]
        
        for path in alternative_paths:
            try:
                data = json_data
                for key in path:
                    data = data.get(key, {})
                if data and isinstance(data, dict) and 'listResults' in data:
                    print(f"✅ Found data at alternative path: {' -> '.join(path)}")
                    return data
            except:
                continue
        
        return None
    
    def parse_property(self, prop_data: Dict) -> Optional[Dict]:
        """
        Parse individual property data
        
        Args:
            prop_data (dict): Raw property data from JSON
            
        Returns:
            dict: Cleaned property information
        """
        try:
            # Extract basic information
            zpid = prop_data.get('zpid')
            if not zpid:
                return None
            
            # Price information
            price = prop_data.get('price')
            price_str = prop_data.get('unformattedPrice', 0)
            
            # Address information (Zillow stores these as separate fields)
            address = prop_data.get('addressStreet', '')
            city = prop_data.get('addressCity', '')
            state = prop_data.get('addressState', '')
            zipcode = prop_data.get('addressZipcode', '')
            
            # Property details
            bedrooms = prop_data.get('beds')
            bathrooms = prop_data.get('baths')
            area = prop_data.get('area')
            property_type = prop_data.get('hdpData', {}).get('homeInfo', {}).get('homeType', '')
            
            # Listing information
            listing_type = prop_data.get('statusType', '')
            listing_status = prop_data.get('statusText', '')
            
            # URLs and images
            detail_url = prop_data.get('detailUrl', '')
            if detail_url and not detail_url.startswith('http'):
                detail_url = f"https://www.zillow.com{detail_url}"
            
            img_src = prop_data.get('imgSrc', '')
            
            # Additional details
            lot_area = prop_data.get('lotAreaValue')
            lot_area_unit = prop_data.get('lotAreaUnit', '')
            year_built = prop_data.get('hdpData', {}).get('homeInfo', {}).get('yearBuilt')
            
            # Rental specific information
            days_on_zillow = prop_data.get('variableData', {}).get('text', '')
            has_image = prop_data.get('hasImage', False)
            is_featured = prop_data.get('isFeatured', False)
            
            # Location coordinates
            lat_long = prop_data.get('latLong', {})
            latitude = lat_long.get('latitude')
            longitude = lat_long.get('longitude')
            
            # Broker information
            broker_name = prop_data.get('brokerName', '')
            
            # Build clean property dict
            property_info = {
                'zpid': zpid,
                'address': address,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'full_address': f"{address}, {city}, {state} {zipcode}",
                'price': price,
                'price_numeric': price_str,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqft': area,
                'property_type': property_type,
                'listing_type': listing_type,
                'listing_status': listing_status,
                'detail_url': detail_url,
                'image_url': img_src,
                'lot_area': lot_area,
                'lot_area_unit': lot_area_unit,
                'year_built': year_built,
                'days_on_zillow': days_on_zillow,
                'latitude': latitude,
                'longitude': longitude,
                'broker_name': broker_name,
                'has_image': has_image,
                'is_featured': is_featured,
            }
            
            return property_info
            
        except Exception as e:
            print(f"⚠️  Error parsing property {prop_data.get('zpid', 'unknown')}: {e}")
            return None
    
    def parse_all_properties(self) -> List[Dict]:
        """
        Parse all properties from the HTML
        
        Returns:
            list: List of property dictionaries
        """
        # Extract JSON data
        json_data = self.extract_json_data()
        if not json_data:
            print("❌ Failed to extract JSON data")
            return []
        
        # Extract search results
        search_results = self.extract_search_results(json_data)
        if not search_results:
            print("❌ Failed to extract search results")
            return []
        
        # Get list of properties
        list_results = search_results.get('listResults', [])
        
        if not list_results:
            print("⚠️  No properties found in listResults")
            # Try alternative key names
            list_results = search_results.get('results', [])
            list_results = list_results or search_results.get('mapResults', [])
        
        print(f"📊 Found {len(list_results)} properties")
        
        # Parse each property
        properties = []
        for i, prop_data in enumerate(list_results, 1):
            prop_info = self.parse_property(prop_data)
            if prop_info:
                properties.append(prop_info)
                print(f"  ✓ Parsed property {i}/{len(list_results)}: {prop_info['address']}")
            else:
                print(f"  ✗ Failed to parse property {i}/{len(list_results)}")
        
        self.properties = properties
        print(f"\n✅ Successfully parsed {len(properties)} out of {len(list_results)} properties")
        
        return properties
    
    def get_pagination_info(self) -> Dict[str, Any]:
        """
        Extract pagination information from JSON data
        
        Returns:
            dict: Pagination info (current_page, total_pages, total_results)
        """
        try:
            json_data = self.extract_json_data()
            if not json_data:
                return {}
            
            search_results = self.extract_search_results(json_data)
            if not search_results:
                return {}
            
            # Try multiple possible pagination paths
            total_results = (
                search_results.get('totalResultCount') or
                search_results.get('totalResults') or
                search_results.get('resultCount') or
                0
            )
            
            # Zillow shows 20 results per page
            results_per_page = 20
            total_pages = (total_results + results_per_page - 1) // results_per_page  # Ceiling division
            
            # Try to get current page
            pagination = (
                search_results.get('searchList', {}).get('pagination', {}) or
                search_results.get('pagination', {}) or
                {}
            )
            
            current_page = pagination.get('currentPage', 1)
            
            return {
                'current_page': current_page,
                'total_pages': total_pages,
                'total_results': total_results,
            }
            
        except Exception as e:
            print(f"⚠️  Error extracting pagination info: {e}")
            return {}
            """
            Extract pagination information from JSON data
            
            Returns:
                dict: Pagination info (current_page, total_pages, total_results)
            """
            try:
                json_data = self.extract_json_data()
                if not json_data:
                    return {}
                
                search_results = self.extract_search_results(json_data)
                if not search_results:
                    return {}
                
                # Try multiple possible pagination paths
                total_results = (
                    search_results.get('totalResultCount') or
                    search_results.get('totalResults') or
                    search_results.get('resultCount') or
                    0
                )
                
                # Zillow shows 20 results per page
                results_per_page = 20
                total_pages = (total_results + results_per_page - 1) // results_per_page  # Ceiling division
                
                # Try to get current page
                pagination = (
                    search_results.get('searchList', {}).get('pagination', {}) or
                    search_results.get('pagination', {}) or
                    {}
                )
                
                current_page = pagination.get('currentPage', 1)
                
                return {
                    'current_page': current_page,
                    'total_pages': total_pages,
                    'total_results': total_results,
                }
                
            except Exception as e:
                print(f"⚠️  Error extracting pagination info: {e}")
                return {}
                """
                Extract pagination information from JSON data
                
                Returns:
                    dict: Pagination info (current_page, total_pages, total_results)
                """
                try:
                    json_data = self.extract_json_data()
                    if not json_data:
                        return {}
                    
                    search_results = self.extract_search_results(json_data)
                    if not search_results:
                        return {}
                    
                    pagination = search_results.get('searchList', {}).get('pagination', {})
                    
                    return {
                        'current_page': pagination.get('currentPage', 1),
                        'total_pages': pagination.get('totalPages', 1),
                        'total_results': search_results.get('totalResultCount', 0),
                    }
                    
                except Exception as e:
                    print(f"⚠️  Error extracting pagination info: {e}")
                    return {}
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics from parsed properties
        
        Returns:
            dict: Summary statistics
        """
        if not self.properties:
            return {}
        
        prices = [p['price_numeric'] for p in self.properties if p.get('price_numeric')]
        areas = [p['area_sqft'] for p in self.properties if p.get('area_sqft')]
        bedrooms = [p['bedrooms'] for p in self.properties if p.get('bedrooms')]
        
        stats = {
            'total_properties': len(self.properties),
            'with_images': sum(1 for p in self.properties if p.get('has_image')),
            'featured': sum(1 for p in self.properties if p.get('is_featured')),
        }
        
        if prices:
            stats['avg_price'] = sum(prices) / len(prices)
            stats['min_price'] = min(prices)
            stats['max_price'] = max(prices)
        
        if areas:
            stats['avg_area'] = sum(areas) / len(areas)
        
        if bedrooms:
            stats['avg_bedrooms'] = sum(bedrooms) / len(bedrooms)
        
        return stats


def parse_html_file(filepath: str) -> List[Dict]:
    """
    Convenience function to parse HTML from file
    
    Args:
        filepath (str): Path to HTML file
        
    Returns:
        list: List of parsed properties
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = ZillowParser(html_content)
        properties = parser.parse_all_properties()
        
        return properties
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []


# Test the parser
if __name__ == "__main__":
    import pandas as pd
    import os
    
    print("=" * 60)
    print("ZILLOW HTML PARSER TEST")
    print("=" * 60)
    
    # Test with saved HTML file
    html_file = "zillow_page.html"
    
    print(f"\n📄 Parsing: {html_file}")
    print("-" * 60)
    
    properties = parse_html_file(html_file)
    
    if properties:
        print("\n" + "=" * 60)
        print("PARSING RESULTS")
        print("=" * 60)
        
        # Display first 3 properties
        for i, prop in enumerate(properties[:3], 1):
            print(f"\n🏠 Property {i}:")
            print(f"  Address: {prop['full_address']}")
            print(f"  Price: ${prop['price_numeric']:,.0f}/month" if prop['price_numeric'] else "  Price: N/A")
            print(f"  Beds: {prop['bedrooms']} | Baths: {prop['bathrooms']} | Sqft: {prop['area_sqft']}")
            print(f"  Type: {prop['property_type']}")
            print(f"  URL: {prop['detail_url']}")
        
        if len(properties) > 3:
            print(f"\n... and {len(properties) - 3} more properties")
        
        # Get parser instance for stats
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        parser = ZillowParser(html_content)
        parser.properties = properties
        
        # Display summary stats
        stats = parser.get_summary_stats()
        pagination = parser.get_pagination_info()
        
        print("\n" + "=" * 60)
        print("SUMMARY STATISTICS")
        print("=" * 60)
        print(f"Total Properties: {stats.get('total_properties', 0)}")
        print(f"With Images: {stats.get('with_images', 0)}")
        print(f"Featured Listings: {stats.get('featured', 0)}")
        
        if 'avg_price' in stats:
            print(f"\nPrice Range: ${stats['min_price']:,.0f} - ${stats['max_price']:,.0f}")
            print(f"Average Price: ${stats['avg_price']:,.0f}")
        
        if 'avg_area' in stats:
            print(f"Average Area: {stats['avg_area']:,.0f} sqft")
        
        if pagination:
            print(f"\nPage: {pagination.get('current_page', 1)} of {pagination.get('total_pages', 1)}")
            print(f"Total Results: {pagination.get('total_results', 0)}")
        
        # ========== NEW: AUTO-SAVE TO FILES ==========
        print("\n" + "=" * 60)
        print("EXPORTING DATA")
        print("=" * 60)
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Export to CSV
        df = pd.DataFrame(properties)
        csv_file = 'output/zillow_rentals.csv'
        df.to_csv(csv_file, index=False)
        print(f"✅ Saved CSV: {csv_file} ({len(properties)} properties)")
        
        # Export to JSON
        import json
        json_file = 'output/zillow_rentals.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(properties, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_file}")
        
        # Export summary stats
        stats_file = 'output/summary_stats.json'
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                'statistics': stats,
                'pagination': pagination,
                'total_properties': len(properties)
            }, f, indent=2)
        print(f"✅ Saved Stats: {stats_file}")
        
        print(f"\n🎉 All data exported to 'output/' directory!")
        
    else:
        print("\n❌ No properties found or parsing failed")