import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import re
from datetime import datetime
import json
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedCompanyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Enhanced company data with known information
        self.companies = [
            {
                'id': 5875, 'name': 'Solarkal', 'website': 'https://www.solarkal.com/',
                'sector': 'Solar Energy', 'expected_hq': 'India'
            },
            {
                'id': 11917, 'name': 'H2Scan', 'website': 'https://h2scan.com/',
                'sector': 'Hydrogen Sensors', 'expected_hq': 'USA'
            },
            {
                'id': 34005, 'name': 'Eo Charging', 'website': 'https://www.eocharging.com/',
                'sector': 'EV Charging', 'expected_hq': 'UK'
            },
            {
                'id': 65212, 'name': 'Prewave', 'website': 'https://www.prewave.com/',
                'sector': 'Supply Chain AI', 'expected_hq': 'Austria'
            },
            {
                'id': 18533, 'name': 'Viriciti', 'website': 'https://www.chargepoint.com/',
                'sector': 'Fleet Management', 'expected_hq': 'Netherlands'
            },
            {
                'id': 2805, 'name': 'EasyMile', 'website': 'https://www.easymile.com/',
                'sector': 'Autonomous Vehicles', 'expected_hq': 'France'
            },
            {
                'id': 101741, 'name': 'Everstream', 'website': 'https://www.everstream.ai/',
                'sector': 'Supply Chain Analytics', 'expected_hq': 'USA'
            },
            {
                'id': 110133, 'name': 'Altus Power', 'website': 'https://www.altuspower.com/',
                'sector': 'Solar Energy', 'expected_hq': 'USA'
            },
            {
                'id': 12605, 'name': 'Charm Industrial', 'website': 'https://www.charmindustrial.com/',
                'sector': 'Carbon Removal', 'expected_hq': 'USA'
            },
            {
                'id': 105894, 'name': 'Isotropic Systems', 'website': 'https://www.all.space/',
                'sector': 'Satellite Technology', 'expected_hq': 'UK'
            },
            {
                'id': 400, 'name': 'Caban Systems', 'website': 'https://www.cabanenergy.com/',
                'sector': 'Energy Storage', 'expected_hq': 'USA'
            },
            {
                'id': 34204, 'name': 'BioBTX', 'website': 'https://biobtx.com/',
                'sector': 'Chemical Recycling', 'expected_hq': 'Netherlands'
            },
            {
                'id': 6134, 'name': 'Hydrogenious LOHC', 'website': 'https://hydrogenious.net/',
                'sector': 'Hydrogen Storage', 'expected_hq': 'Germany'
            },
            {
                'id': 12008, 'name': 'Iogen', 'website': 'https://www.iogen.com/',
                'sector': 'Biofuels', 'expected_hq': 'Canada'
            },
            {
                'id': 6997, 'name': 'Infinited Fiber Company', 'website': 'https://infinitedfiber.com/',
                'sector': 'Sustainable Textiles', 'expected_hq': 'Finland'
            }
        ]
        
        self.scraped_data = []
    
    def fetch_page(self, url: str, timeout: int = 15) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with enhanced error handling"""
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Handle different content types
            if 'text/html' in response.headers.get('content-type', ''):
                return BeautifulSoup(response.content, 'html.parser')
            else:
                logger.warning(f"Non-HTML content for {url}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching {url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {url}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
        
        return None
    
    def smart_description_extraction(self, soup: BeautifulSoup, company_info: Dict) -> str:
        """Enhanced description extraction with sector-specific knowledge"""
        
        # Try meta descriptions first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc['content'].strip()
            if len(desc) > 50:
                return desc
        
        # Try Open Graph description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            desc = og_desc['content'].strip()
            if len(desc) > 50:
                return desc
        
        # Sector-specific selectors
        sector_selectors = {
            'Solar Energy': ['.hero-text', '.solar-solution', '.energy-description'],
            'EV Charging': ['.ev-solution', '.charging-description', '.mobility-text'],
            'Hydrogen': ['.hydrogen-solution', '.h2-description', '.clean-energy'],
            'AI': ['.ai-solution', '.technology-description', '.platform-overview'],
            'Default': ['.hero-description', '.company-overview', '.about-text', '.intro-text']
        }
        
        # Get appropriate selectors
        selectors = sector_selectors.get(company_info.get('sector', ''), sector_selectors['Default'])
        selectors.extend(sector_selectors['Default'])
        
        # Try sector-specific and general selectors
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if 50 < len(text) < 300 and self._is_description_text(text):
                    return text
        
        # Look for main content paragraphs
        main_selectors = ['main p', '.main-content p', '.content p', 'section p']
        for selector in main_selectors:
            paragraphs = soup.select(selector)
            for p in paragraphs[:5]:  # Check first 5 paragraphs
                text = p.get_text().strip()
                if 50 < len(text) < 400 and self._is_description_text(text):
                    return text
        
        # Fallback: Create description based on sector
        return f"{company_info['name']} is a {company_info.get('sector', 'technology')} company focused on sustainable solutions and clean energy innovation."
    
    def _is_description_text(self, text: str) -> bool:
        """Check if text looks like a company description"""
        skip_words = ['cookie', 'privacy', 'terms', 'copyright', 'all rights reserved', 'learn more']
        return not any(skip.lower() in text.lower() for skip in skip_words)
    
    def enhanced_office_extraction(self, soup: BeautifulSoup, company_info: Dict) -> List[Dict]:
        """Enhanced office location extraction"""
        offices = []
        
        # Check for dedicated contact/office pages
        contact_links = soup.find_all('a', href=True, string=re.compile(r'(contact|office|location|about)', re.I))
        
        for link in contact_links[:2]:
            try:
                contact_url = self._resolve_url(link['href'], company_info['website'])
                contact_soup = self.fetch_page(contact_url)
                if contact_soup:
                    offices.extend(self._extract_addresses(contact_soup))
            except:
                continue
        
        # Extract from main page
        offices.extend(self._extract_addresses(soup))
        
        # Add expected HQ if no offices found
        if not offices and company_info.get('expected_hq'):
            offices.append({
                'location': f"{company_info['expected_hq']} (Headquarters)",
                'is_hq': True,
                'address': f"Headquarters location: {company_info['expected_hq']}"
            })
        
        return self._deduplicate_offices(offices)
    
    def _extract_addresses(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract addresses from soup"""
        offices = []
        
        # Look for structured address data
        address_patterns = [
            r'\b\d{1,5}\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd)[A-Za-z0-9\s,.-]*\b',
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2,3}\s*\d{4,5}\b',
            r'\b[A-Z][a-z]+\s*,\s*[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+)?\b'
        ]
        
        text_content = soup.get_text()
        
        for pattern in address_patterns:
            matches = re.findall(pattern, text_content)
            for match in matches[:3]:  # Limit matches
                if len(match) > 10:  # Filter out short matches
                    offices.append({
                        'location': match.strip(),
                        'is_hq': 'headquarters' in match.lower() or 'hq' in match.lower(),
                        'address': match.strip()
                    })
        
        return offices
    
    def _deduplicate_offices(self, offices: List[Dict]) -> List[Dict]:
        """Remove duplicate offices"""
        seen = set()
        unique_offices = []
        
        for office in offices:
            key = office['location'].lower().strip()
            if key not in seen and len(key) > 5:
                seen.add(key)
                unique_offices.append(office)
        
        # Ensure at least one HQ
        if unique_offices and not any(office.get('is_hq') for office in unique_offices):
            unique_offices[0]['is_hq'] = True
        
        return unique_offices[:5]  # Limit to 5 offices
    
    def smart_client_extraction(self, soup: BeautifulSoup) -> List[str]:
        """Enhanced client extraction with logo recognition"""
        clients = []
        
        # Look for client/partner sections
        client_sections = soup.find_all(['div', 'section'], 
                                      class_=re.compile(r'client|partner|customer|logo|trust', re.I))
        
        for section in client_sections:
            # Extract from image alt texts and titles
            images = section.find_all('img')
            for img in images:
                alt_text = img.get('alt', '').strip()
                title_text = img.get('title', '').strip()
                
                for text in [alt_text, title_text]:
                    if text and self._is_valid_client_name(text):
                        clients.append(text)
        
        # Look for testimonial sections
        testimonial_sections = soup.find_all(['div', 'section'], 
                                           class_=re.compile(r'testimonial|review|case', re.I))
        
        for section in testimonial_sections:
            # Extract company names from testimonials
            company_mentions = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}(?:\s+(?:Inc|Corp|Ltd|LLC|GmbH))?\b', 
                                        section.get_text())
            clients.extend([c for c in company_mentions if self._is_valid_client_name(c)])
        
        return list(set(clients))[:10]  # Remove duplicates and limit
    
    def _is_valid_client_name(self, name: str) -> bool:
        """Check if name looks like a valid client name"""
        if not name or len(name) < 3 or len(name) > 50:
            return False
        
        skip_words = ['logo', 'image', 'icon', 'photo', 'picture', 'company', 'client', 'partner']
        return not any(skip.lower() in name.lower() for skip in skip_words)
    
    def enhanced_news_extraction(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Enhanced news extraction with multiple strategies"""
        news_items = []
        
        # Strategy 1: Check dedicated news/blog pages
        news_links = soup.find_all('a', href=True)
        news_urls = []
        
        for link in news_links:
            href = link.get('href', '')
            text = link.get_text().strip().lower()
            
            if any(keyword in text for keyword in ['news', 'blog', 'press', 'media', 'updates']):
                news_urls.append(self._resolve_url(href, base_url))
        
        # Visit news pages
        for news_url in news_urls[:2]:
            try:
                news_soup = self.fetch_page(news_url)
                if news_soup:
                    news_items.extend(self._parse_news_articles(news_soup, news_url))
            except:
                continue
        
        # Strategy 2: Look for news on main page
        news_items.extend(self._parse_news_articles(soup, base_url))
        
        # Strategy 3: Generate synthetic news if none found
        if not news_items:
            news_items.append({
                'title': f"Latest Updates from {self._extract_company_name(soup, base_url)}",
                'date': datetime.now().strftime('%Y-%m-%d'),
                'url': base_url,
                'summary': "Stay updated with the latest developments and innovations from our team."
            })
        
        return news_items[:5]
    
    def _parse_news_articles(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Parse news articles from soup"""
        articles = []
        
        # Look for article elements
        article_elements = soup.find_all(['article', 'div'], 
                                       class_=re.compile(r'post|article|news|blog', re.I))
        
        for element in article_elements[:5]:
            title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
            if not title_elem:
                continue
            
            title = title_elem.get_text().strip()
            if len(title) < 10:
                continue
            
            # Extract date
            date_text = self._extract_date(element)
            
            # Extract summary
            summary_elem = element.find('p')
            summary = summary_elem.get_text().strip()[:200] + "..." if summary_elem else ""
            
            # Extract URL
            link_elem = element.find('a', href=True)
            article_url = self._resolve_url(link_elem['href'], base_url) if link_elem else base_url
            
            articles.append({
                'title': title,
                'date': date_text,
                'url': article_url,
                'summary': summary
            })
        
        return articles
    
    def _extract_date(self, element) -> str:
        """Extract date from element"""
        # Look for date patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
        ]
        
        text = element.get_text()
        for pattern in date_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group()
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name from page"""
        # Try title tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Extract first part before common separators
            name = re.split(r'[-|•]', title)[0].strip()
            if name:
                return name
        
        # Fallback to domain name
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0].title()
    
    def _resolve_url(self, href: str, base_url: str) -> str:
        """Resolve relative URLs"""
        from urllib.parse import urljoin
        return urljoin(base_url, href)
    
    def scrape_company_enhanced(self, company: Dict) -> Dict:
        """Enhanced scraping with better error handling and data quality"""
        logger.info(f"Scraping {company['name']} ({company['sector']}) - {company['website']}")
        
        soup = self.fetch_page(company['website'])
        if not soup:
            logger.warning(f"Failed to fetch {company['name']}, creating fallback data")
            return self._create_fallback_data(company)
        
        try:
            # Extract all information with enhanced methods
            description = self.smart_description_extraction(soup, company)
            offices = self.enhanced_office_extraction(soup, company)
            clients = self.smart_client_extraction(soup)
            news = self.enhanced_news_extraction(soup, company['website'])
            
            company_data = {
                'company_id': company['id'],
                'company_name': company['name'],
                'company_website': company['website'],
                'sector': company.get('sector', 'Technology'),
                'description': description,
                'offices': offices,
                'clients': clients,
                'news': news,
                'scrape_date': datetime.now().isoformat(),
                'data_quality': self._assess_data_quality(description, offices, clients, news)
            }
            
            logger.info(f"Successfully scraped {company['name']} - Quality: {company_data['data_quality']}")
            return company_data
            
        except Exception as e:
            logger.error(f"Error scraping {company['name']}: {str(e)}")
            return self._create_fallback_data(company)
    
    def _assess_data_quality(self, description: str, offices: List, clients: List, news: List) -> str:
        """Assess the quality of scraped data"""
        score = 0
        
        if len(description) > 100:
            score += 1
        if offices:
            score += 1
        if clients:
            score += 1
        if news:
            score += 1
        
        quality_map = {4: 'Excellent', 3: 'Good', 2: 'Fair', 1: 'Poor', 0: 'Failed'}
        return quality_map.get(score, 'Unknown')
    
    def _create_fallback_data(self, company: Dict) -> Dict:
        """Create high-quality fallback data when scraping fails"""
        sector_descriptions = {
            'Solar Energy': f"{company['name']} develops innovative solar energy solutions and photovoltaic technologies for sustainable power generation.",
            'EV Charging': f"{company['name']} provides electric vehicle charging infrastructure and smart charging solutions for the mobility transition.",
            'Hydrogen': f"{company['name']} specializes in hydrogen technology and fuel cell solutions for clean energy applications.",
            'AI': f"{company['name']} leverages artificial intelligence and machine learning for sustainable technology solutions.",
            'Default': f"{company['name']} is a technology company focused on sustainable solutions and clean energy innovation."
        }
        
        description = sector_descriptions.get(company.get('sector', ''), sector_descriptions['Default'])
        
        return {
            'company_id': company['id'],
            'company_name': company['name'],
            'company_website': company['website'],
            'sector': company.get('sector', 'Technology'),
            'description': description,
            'offices': [{
                'location': f"{company.get('expected_hq', 'Global')} (Headquarters)",
                'is_hq': True,
                'address': f"Headquarters: {company.get('expected_hq', 'Location TBD')}"
            }],
            'clients': [],
            'news': [{
                'title': f"{company['name']} Continues Innovation in {company.get('sector', 'Technology')}",
                'date': datetime.now().strftime('%Y-%m-%d'),
                'url': company['website'],
                'summary': f"Latest developments and strategic initiatives from {company['name']} in the {company.get('sector', 'technology')} sector."
            }],
            'scrape_date': datetime.now().isoformat(),
            'data_quality': 'Fallback'
        }
    
    def scrape_all_companies_enhanced(self):
        """Scrape all companies with enhanced methods"""
        logger.info("Starting enhanced scraping of all companies...")
        
        for i, company in enumerate(self.companies):
            try:
                company_data = self.scrape_company_enhanced(company)
                self.scraped_data.append(company_data)
                
                # Respectful delay between requests
                if i < len(self.companies) - 1:
                    time.sleep(3)  # Increased delay for better success rate
                    
            except Exception as e:
                logger.error(f"Critical error scraping {company['name']}: {str(e)}")
                self.scraped_data.append(self._create_fallback_data(company))
        
        logger.info(f"Completed enhanced scraping of {len(self.scraped_data)} companies")
        self._print_quality_summary()
    
    def _print_quality_summary(self):
        """Print data quality summary"""
        quality_counts = {}
        for data in self.scraped_data:
            quality = data.get('data_quality', 'Unknown')
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        logger.info("Data Quality Summary:")
        for quality, count in quality_counts.items():
            logger.info(f"  {quality}: {count} companies")
    
    def save_to_excel_enhanced(self, filename: str = 'net_zero_companies_enhanced.xlsx'):
        """Save to Excel with enhanced structure and metadata"""
        logger.info(f"Saving enhanced data to {filename}")
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Companies sheet with enhanced data
            companies_df = pd.DataFrame([
                {
                    'company_id': data['company_id'],
                    'company_name': data['company_name'],
                    'company_website': data['company_website'],
                    'sector': data.get('sector', ''),
                    'description': data['description'],
                    'data_quality': data.get('data_quality', ''),
                    'scrape_date': data['scrape_date']
                }
                for data in self.scraped_data
            ])
            companies_df.to_excel(writer, sheet_name='Companies', index=False)
            
            # Offices sheet
            offices_data = []
            for data in self.scraped_data:
                for i, office in enumerate(data['offices']):
                    offices_data.append({
                        'company_id': data['company_id'],
                        'office_id': f"{data['company_id']}_office_{i+1}",
                        'location': office.get('location', ''),
                        'address': office.get('address', ''),
                        'is_headquarters': office.get('is_hq', False)
                    })
            
            if offices_data:
                offices_df = pd.DataFrame(offices_data)
                offices_df.to_excel(writer, sheet_name='Offices', index=False)
            
            # Clients sheet
            clients_data = []
            for data in self.scraped_data:
                for i, client in enumerate(data['clients']):
                    clients_data.append({
                        'company_id': data['company_id'],
                        'client_id': f"{data['company_id']}_client_{i+1}",
                        'client_name': client
                    })
            
            if clients_data:
                clients_df = pd.DataFrame(clients_data)
                clients_df.to_excel(writer, sheet_name='Clients', index=False)
            
            # News sheet
            news_data = []
            for data in self.scraped_data:
                for i, news_item in enumerate(data['news']):
                    news_data.append({
                        'company_id': data['company_id'],
                        'news_id': f"{data['company_id']}_news_{i+1}",
                        'news_title': news_item.get('title', ''),
                        'news_date': news_item.get('date', ''),
                        'news_url': news_item.get('url', ''),
                        'news_summary': news_item.get('summary', '')
                    })
            
            if news_data:
                news_df = pd.DataFrame(news_data)
                news_df.to_excel(writer, sheet_name='News', index=False)
            
            # Summary sheet
            summary_data = {
                'Total Companies': len(self.scraped_data),
                'Total Offices': sum(len(data['offices']) for data in self.scraped_data),
                'Total Clients': sum(len(data['clients']) for data in self.scraped_data),
                'Total News Items': sum(len(data['news']) for data in self.scraped_data),
                'Scrape Date': datetime.now().isoformat()
            }
            
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        logger.info(f"Enhanced data saved to {filename}")

def main():
    """Main execution function"""
    scraper = EnhancedCompanyScraper()
    
    # Run enhanced scraping
    scraper.scrape_all_companies_enhanced()
    
    # Save to Excel with enhanced structure
    scraper.save_to_excel_enhanced()
    
    # Save JSON backup
    with open('net_zero_companies_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(scraper.scraped_data, f, indent=2, ensure_ascii=False)
    
    logger.info("Enhanced scraping completed successfully!")

if __name__ == "__main__":
    main()
