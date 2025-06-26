# Scraping Assignment for Net Zero Insights

**Author:** Aarush Kumar

## 📋 Project Overview

This project is an enhanced web scraping solution designed to extract comprehensive company information from clean energy and sustainability-focused companies. The scraper targets 15 companies across various sectors including solar energy, EV charging, hydrogen technology, AI, and more.

## 🎯 Features

- **Enhanced Company Data Extraction**: Intelligent scraping of company descriptions, office locations, client information, and news updates
- **Sector-Specific Intelligence**: Tailored extraction strategies based on company sectors
- **Robust Error Handling**: Comprehensive fallback mechanisms and retry logic
- **Data Quality Assessment**: Automatic evaluation of scraped data quality
- **Multiple Output Formats**: Excel with multiple sheets and JSON backup
- **Respectful Scraping**: Built-in delays and session management to avoid overwhelming target servers

## 🏢 Target Companies

The scraper processes 15 companies across different sectors:

| Company | Sector | Expected HQ | Website |
|---------|---------|-------------|---------|
| Solarkal | Solar Energy | India | https://www.solarkal.com/ |
| H2Scan | Hydrogen Sensors | USA | https://h2scan.com/ |
| Eo Charging | EV Charging | UK | https://www.eocharging.com/ |
| Prewave | Supply Chain AI | Austria | https://www.prewave.com/ |
| Viriciti | Fleet Management | Netherlands | https://www.chargepoint.com/ |
| EasyMile | Autonomous Vehicles | France | https://www.easymile.com/ |
| Everstream | Supply Chain Analytics | USA | https://www.everstream.ai/ |
| Altus Power | Solar Energy | USA | https://www.altuspower.com/ |
| Charm Industrial | Carbon Removal | USA | https://www.charmindustrial.com/ |
| Isotropic Systems | Satellite Technology | UK | https://www.all.space/ |
| Caban Systems | Energy Storage | USA | https://www.cabanenergy.com/ |
| BioBTX | Chemical Recycling | Netherlands | https://biobtx.com/ |
| Hydrogenious LOHC | Hydrogen Storage | Germany | https://hydrogenious.net/ |
| Iogen | Biofuels | Canada | https://www.iogen.com/ |
| Infinited Fiber Company | Sustainable Textiles | Finland | https://infinitedfiber.com/ |

## 🔧 Technical Requirements

### Dependencies

```python
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
openpyxl==3.1.2
lxml==4.9.3
```

### Python Version
- Python 3.8 or higher

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd scraping-assignment-net-zero-insights
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

Run the scraper with default settings:

```bash
python main.py
```

### Programmatic Usage

```python
from enhanced_company_scraper import EnhancedCompanyScraper

# Initialize scraper
scraper = EnhancedCompanyScraper()

# Run scraping process
scraper.scrape_all_companies_enhanced()

# Save results
scraper.save_to_excel_enhanced('output_filename.xlsx')
```

## 📊 Output Structure

The scraper generates two output files:

### 1. Excel File (`net_zero_companies_enhanced.xlsx`)
- **Companies Sheet**: Main company information (ID, name, website, sector, description, data quality)
- **Offices Sheet**: Office locations and headquarters information
- **Clients Sheet**: Extracted client and partner information
- **News Sheet**: Recent news articles and updates
- **Summary Sheet**: Overall statistics and metadata

### 2. JSON File (`net_zero_companies_enhanced.json`)
- Complete raw data backup in JSON format
- Includes all extracted information with nested structures

## 🔍 Data Extraction Features

### Smart Description Extraction
- Meta tag analysis (description, og:description)
- Sector-specific content selectors
- Intelligent text filtering and validation

### Enhanced Office Location Detection
- Address pattern recognition
- Contact page exploration
- Headquarters identification
- Geographic data normalization

### Client and Partner Recognition
- Logo alt-text analysis
- Testimonial section parsing
- Company name pattern matching
- Duplicate removal and validation

### News and Media Extraction
- Dedicated news page discovery
- Article metadata extraction
- Date parsing and normalization
- Summary generation

## 📈 Data Quality Assessment

The scraper automatically assesses data quality based on:
- Description completeness (>100 characters)
- Office location availability
- Client information presence
- News content extraction

Quality levels:
- **Excellent**: All data types successfully extracted
- **Good**: 3/4 data types extracted
- **Fair**: 2/4 data types extracted
- **Poor**: 1/4 data types extracted
- **Fallback**: Scraping failed, synthetic data generated

## ⚙️ Configuration

### Customizing Target Companies

Modify the company list in the `EnhancedCompanyScraper.__init__()` method:

```python
self.companies = [
    {
        'id': 12345,
        'name': 'Your Company',
        'website': 'https://example.com',
        'sector': 'Technology',
        'expected_hq': 'Country'
    },
    # Add more companies...
]
```

### Adjusting Scraping Behavior

- **Request Delay**: Modify `time.sleep(3)` in `scrape_all_companies_enhanced()`
- **Timeout Settings**: Adjust `timeout=15` in `fetch_page()`
- **User Agent**: Update headers in `__init__()`

## 🛡️ Ethical Considerations

This scraper is designed with ethical web scraping practices:
- Respectful request delays (3 seconds between requests)
- Proper User-Agent identification
- Timeout handling to avoid hanging connections
- Graceful error handling
- No aggressive retry mechanisms

## 🐛 Error Handling

The scraper includes comprehensive error handling:
- **Network Errors**: Timeout and connection error recovery
- **Parsing Errors**: Graceful HTML parsing fallbacks
- **Data Validation**: Content quality checks and filtering
- **Fallback Data**: High-quality synthetic data when scraping fails

## 📝 Logging

The application provides detailed logging:
- Progress tracking for each company
- Error reporting with specific details
- Data quality summaries
- Performance metrics

## 📊 Project Statistics

- **Target Companies**: 15
- **Sectors Covered**: 10+
- **Data Points Extracted**: 4 main categories per company
- **Output Formats**: 2 (Excel + JSON)
- **Error Recovery**: Comprehensive fallback system

---

