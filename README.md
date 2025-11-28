# Zillow Multi-Page Scraper

A Python-based scraper for extracting rental property listings from Zillow using the Nimble API with automatic pagination support.

## 🚀 Features

- 🔄 Automatic pagination - scrapes multiple pages
- 📊 Exports data to CSV and JSON formats
- 📈 Generates summary statistics
- 🏠 Extracts comprehensive property details (price, beds, baths, sqft, location, etc.)

## 📋 Prerequisites

- Python 3.8 or higher
- Nimble API account and credentials ([Sign up here](https://nimbleway.com))

## 🛠️ Installation

### 1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/zillow_scraper.git
cd zillow_scraper### 2. Install Python

**macOS/Linux:**

# Check if Python is installed

python3 --version

# If not installed, install via package manager:

# macOS (using Homebrew)

brew install python3

# Ubuntu/Debian

sudo apt update
sudo apt install python3 python3-pip python3-venv**Windows:**

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
   python --version### 3. Create Virtual Environment (Recommended)

# Create virtual environment

python3 -m venv venv

# Activate virtual environment

# macOS/Linux:

source venv/bin/activate

# Windows:

venv\Scripts\activate### 4. Install Dependencies

pip install -r requirements.txt## ⚙️ Configuration

### 1. Get Nimble API Credentials

1. Sign up at [Nimbleway](https://nimbleway.com)
2. Get your Base64 API token from the dashboard

### 2. Configure API Credentials

Edit `config.py` and add your Nimble API token:

NIMBLE_BASE64_TOKEN = "your_base64_token_here"

# Install requirements

**pip install -r requirements.txt**


# 🏃 Usage

Go to https://www.zillow.com and search for any locations of rental homes.

Copy and past the full url of the browser and past it in `config.py`

ZILLOW_SEARCH_URL="your_full_zillow_search_url_here"

### Run the Multi-Page Scraper

**python scrape_with_pagination.py**

This will:

1. Fetch up to 10 pages of Zillow listings
2. Parse all property data
3. Save results to the `output/` directory:
   - `zillow_multi_page.json` - Raw property data
   - `zillow_multi_page.csv` - Spreadsheet format
   - `zillow_multi_page_stats.json` - Summary statistics

# Output Example

🔗 Base URL: https://www.zillow.com/denver-co/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBoun...

⚙️  Configuration:

- Max pages: 10
- Wait time per page: 5 seconds
- Auto-detect pagination: ON
  🏠 Starting Zillow Multi-Page Scraper
  =====================================

📥 Fetching up to 10 pages...

##### ============================================================

📄 Fetching Page 1

Fetching: https://www.zillow.com/denver-co/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBoun...
Response Status Code: 200
{
  "url": "https://www.zillow.com/denver-co/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A39.914247%2C%22south%22%3A39.623862%2C%22east%22%3A-104.600296%2C%22west%22%3A-105.081455%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22personalizedsort%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22beds%22%3A%7B%22min%22%3A5%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22category%22%3A%22cat1%22%2C%22curatedCollection%22%3Anull%2C%22usersSearchTerm%22%3A%22Denver%20CO%22%2C%22listPriceActive%22%3Atrue%2C%22pagination%22%3A%7B%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A11093%2C%22regionType%22%3A6%7D%5D%7D",
  "task_id": "75073f71-62e8-435c-be6f-8fcb89d48e4f",
  "status": "success",
  "query_time": "2025-11-27T16:54:07.891Z",
  "html_content": "`<!DOCTYPE html>`<html lang=\"en\">`<head><style>`.gm-style-moc{background-color:rgba(0,0,0,.59);pointer-events:none;text-align:center;-webkit-transition:opacity ease-in-out;transition:opacity ease-in-out}.gm-style-mot{color:white;font-family:Roboto,Arial,sans-serif;font-size:22px;margin:0;position:relative;top:50%;transform:translateY(-50%);-webkit-transform:translateY(-50%);-ms-transform:translateY(-50%)}sentinel{}\n `</style><style>`.gm-style img{max-width: none;}.gm-style {font: 400 11px Roboto, Arial, sans-serif; text-decoration: none;}`</style>`<script async=\"\" src=\"//www.google-analytics.com/analytics.js\">`</script>`<script async=\"\" src=\"//www.google-analytics.com/analytics.js\">`</script>`<script id=\"google-1-tap\" src=\"https://accounts.google.com/gsi/client\">`</script>`<script async=\"\" src=\"/HYx10rg3/init.js
API Status: success
Render Flow Status: True
➡️  Next page available, continuing to page 2

##### ============================================================

📄 Fetching Page 2

🔗 Modified URL for page 2
Fetching: https://www.zillow.com/denver-co/rentals/2_p/?searchQueryState=%7B%22isMapVisible%22%3A%20true%2C%20...
Response Status Code: 200
{
  "url": "https://www.zillow.com/denver-co/rentals/2_p/?searchQueryState=%7B%22isMapVisible%22%3A%20true%2C%20%22mapBounds%22%3A%20%7B%22north%22%3A%2039.914247%2C%20%22south%22%3A%2039.623862%2C%20%22east%22%3A%20-104.600296%2C%20%22west%22%3A%20-105.081455%7D%2C%20%22filterState%22%3A%20%7B%22sort%22%3A%20%7B%22value%22%3A%20%22personalizedsort%22%7D%2C%20%22fsba%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fsbo%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22nc%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22cmsn%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22auc%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fore%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fr%22%3A%20%7B%22value%22%3A%20true%7D%2C%20%22beds%22%3A%20%7B%22min%22%3A%205%7D%2C%20%22land%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22manu%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22mf%22%3A%20%7B%22value%22%3A%20false%7D%7D%2C%20%22isListVisible%22%3A%20true%2C%20%22category%22%3A%20%22cat1%22%2C%20%22curatedCollection%22%3A%20null%2C%20%22usersSearchTerm%22%3A%20%22Denver%20CO%22%2C%20%22listPriceActive%22%3A%20true%2C%20%22pagination%22%3A%20%7B%22currentPage%22%3A%202%7D%2C%20%22regionSelection%22%3A%20%5B%7B%22regionId%22%3A%2011093%2C%20%22regionType%22%3A%206%7D%5D%7D",
  "task_id": "7c82742c-0c08-4d96-835a-778ab7a6fe6f",
  "status": "success",
  "query_time": "2025-11-27T16:54:39.321Z",
  "html_content": "`<!DOCTYPE html>`<html lang=\"en\">`<head><style>`.LGLeeN-keyboard-shortcuts-view{display:-webkit-box;display:-webkit-flex;display:-moz-box;display:-ms-flexbox;display:flex}.LGLeeN-keyboard-shortcuts-view table,.LGLeeN-keyboard-shortcuts-view tbody,.LGLeeN-keyboard-shortcuts-view td,.LGLeeN-keyboard-shortcuts-view tr{background:inherit;border:none;margin:0;padding:0}.LGLeeN-keyboard-shortcuts-view table{display:table}.LGLeeN-keyboard-shortcuts-view tr{display:table-row}.LGLeeN-keyboard-shortcuts-view td{-moz-box-sizing:border-box;box-sizing:border-box;display:table-cell;color:light-dark(#000,#fff);paddi
API Status: success
Render Flow Status: True
✅ No more pages available. Total pages scraped: 2

##### ============================================================

✅ Completed scraping 2 pages

✅ Fetched 2 pages

##### ============================================================

📊 Parsing listings from all pages...

📄 Parsing Page 1...
/Users/amiradar/SHITS/zillow_scraper/parser.py:37: GuessedAtParserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

The code that caused this warning is on line 37 of the file /Users/amiradar/SHITS/zillow_scraper/parser.py. To get rid of this warning, pass the additional argument 'features="lxml"' to the BeautifulSoup constructor.

  self.soup = BeautifulSoup(html_content, 'html') if html_content else None
✅ Exported soup to parsed_soup.html
✅ Successfully extracted JSON data
📊 Found 41 properties
  ✓ Parsed property 1/41: 8231 E Lehigh Dr
  ✓ Parsed property 2/41: 4141 Madison St
  ✓ Parsed property 3/41: 7972 Grace Ct
  ✓ Parsed property 4/41: 1658 Colorado Blvd
  ✓ Parsed property 5/41: 4704 W Dakota Ave
  ✓ Parsed property 6/41: 1905 S Logan St
  ✓ Parsed property 7/41: 4094 S Willow Way
  ✓ Parsed property 8/41: 4090 W Wagon Trail Dr
  ✓ Parsed property 9/41: 1626 N High St
  ✓ Parsed property 10/41: 2462 S Ogden St
  ✓ Parsed property 11/41: 9163 E 24th Pl
  ✓ Parsed property 12/41: 794 Oneida St
  ✓ Parsed property 13/41: 3527 N Clay St
  ✓ Parsed property 14/41: 3070 Ash St
  ✓ Parsed property 15/41: 4498 W 9th Ave
  ✓ Parsed property 16/41: 4501 E Utah Pl
  ✓ Parsed property 17/41: 5992 N Fulton St
  ✓ Parsed property 18/41: 5440 Perth St
  ✓ Parsed property 19/41: 5542 Scranton St
  ✓ Parsed property 20/41: 2471 S Quitman St
  ✓ Parsed property 21/41: 701 S Milwaukee St
  ✓ Parsed property 22/41: 12345 E 55th Ave
  ✓ Parsed property 23/41: 1801 E 33rd Ave
  ✓ Parsed property 24/41: 2342 N Xenia St
  ✓ Parsed property 25/41: 1346 N Williams St
  ✓ Parsed property 26/41: 3700 N Jackson St
  ✓ Parsed property 27/41: 803 Uinta Way
  ✓ Parsed property 28/41: 1804 E 35th Ave
  ✓ Parsed property 29/41: 3349 Zuni St
  ✓ Parsed property 30/41: 4760 E Dartmouth Ave
  ✓ Parsed property 31/41: 5521 Lewiston Ct
  ✓ Parsed property 32/41: 3953 W Eldorado Pl
  ✓ Parsed property 33/41: 4904 Wheeling St
  ✓ Parsed property 34/41: 3030 S University Blvd
  ✓ Parsed property 35/41: 1730 Gaylord St
  ✓ Parsed property 36/41: 3921 N Colorado Blvd
  ✓ Parsed property 37/41: 1815 Grove St
  ✓ Parsed property 38/41: 1514 S Locust St
  ✓ Parsed property 39/41: 2356 S Gilpin St
  ✓ Parsed property 40/41: 75 Albion St
  ✓ Parsed property 41/41: 940 N Logan St

✅ Successfully parsed 41 out of 41 properties
✅ Found 41 listings on page 1
   Total so far: 41 listings

📄 Parsing Page 2...
✅ Exported soup to parsed_soup.html
✅ Successfully extracted JSON data
📊 Found 28 properties
  ✓ Parsed property 1/28: 2833 E 8th Ave
  ✓ Parsed property 2/28: 2455 S Garfield St
  ✓ Parsed property 3/28: 2434 S Ogden St #2436
  ✓ Parsed property 4/28: 17951 E 47th Dr
  ✓ Parsed property 5/28: 2004 S Galapago St
  ✓ Parsed property 6/28: 3600 E Virginia Ave
  ✓ Parsed property 7/28: 3035 S Beeler St
  ✓ Parsed property 8/28: 1665 Jasmine St
  ✓ Parsed property 9/28: 2082 Cherry St
  ✓ Parsed property 10/28: 20411 E 42nd Ave
  ✓ Parsed property 11/28: 500 Jackson St
  ✓ Parsed property 12/28: 1000 Monaco Pkwy
  ✓ Parsed property 13/28: 4350 E Utah Pl
  ✓ Parsed property 14/28: 4665 Gaylord St APT A
  ✓ Parsed property 15/28: 8201 E 6th Ave
  ✓ Parsed property 16/28: 911 Tennyson St
  ✓ Parsed property 17/28: 1000 N Monaco Pkwy
  ✓ Parsed property 18/28: 2900 Locust St
  ✓ Parsed property 19/28: 6121 Chester St
  ✓ Parsed property 20/28: 510 N High St
  ✓ Parsed property 21/28: 1486 S Garfield St
  ✓ Parsed property 22/28: 2675 S Josephine St
  ✓ Parsed property 23/28: 4930 E Ellsworth Ave
  ✓ Parsed property 24/28: 70 S Canosa Way
  ✓ Parsed property 25/28: 1600 N Logan St
  ✓ Parsed property 26/28: 2062 Glenarm Pl
  ✓ Parsed property 27/28: (undisclosed Address)
  ✓ Parsed property 28/28: 565 Winona Ct

✅ Successfully parsed 28 out of 28 properties
✅ Found 28 listings on page 2
   Total so far: 69 listings

##### ============================================================

📈 Calculating statistics...

##### ============================================================

📊 RESULTS SUMMARY

✅ Total Pages Scraped: 2
✅ Total Listings Found: 69

💾 Saving results...
✅ Saved 69 listings to output/zillow_multi_page.json
✅ Saved to output/zillow_multi_page.csv
✅ Saved statistics to output/zillow_multi_page_stats.json

##### ============================================================

🎉 Scraping Complete!

📋 Sample Listings (first 3):

1. 8231 E Lehigh Dr
   💰 $3,695/mo/mo
   🛏️  N/A bed | 🚿 N/A bath | 📐 N/A sqft
   📄 Page: 1
2. 4141 Madison St
   💰 $4,900/mo/mo
   🛏️  N/A bed | 🚿 N/A bath | 📐 N/A sqft
   📄 Page: 1
3. 7972 Grace Ct
   💰 $3,000/mo/mo
   🛏️  N/A bed | 🚿 N/A bath | 📐 N/A sqft
   📄 Page: 1
