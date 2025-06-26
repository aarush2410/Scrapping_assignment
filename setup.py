from setuptools import setup, find_packages

setup(
    name="net-zero-company-scraper",
    version="1.0.0",
    description="Web scraper for Net Zero companies data extraction",
    author="Data Engineer",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "pandas>=2.0.3",
        "openpyxl>=3.1.2",
        "lxml>=4.9.3"
    ],
    python_requires=">=3.8"
)