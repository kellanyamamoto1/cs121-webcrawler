import re
import os
from configparser import ConfigParser

def check_config():
    """Validate the configuration file"""
    print("=" * 80)
    print("PRE-FLIGHT CONFIGURATION CHECKER")
    print("=" * 80)
    
    errors = []
    warnings = []
    
    # Check if config.ini exists
    if not os.path.exists("config.ini"):
        errors.append("config.ini file not found!")
        return errors, warnings
    config = ConfigParser()
    config.read("config.ini")
    
    # Check USERAGENT
    print("\n[1] Checking USERAGENT...")
    useragent = config["IDENTIFICATION"]["USERAGENT"].strip()
    
    if useragent == "DEFAULT AGENT":
        errors.append("USERAGENT is still set to 'DEFAULT AGENT'")
        errors.append("You MUST change this to: IR UW26 studentID1,studentID2,studentID3")
    elif "IR UW26" not in useragent:
        warnings.append("USERAGENT should start with 'IR UW26'")
    elif not re.search(r'\d+', useragent):
        warnings.append("USERAGENT should contain student IDs (numbers)")
    else:
        print(f"   ✓ USERAGENT: {useragent}")
    
    # Check connection settings
    print("\n[2] Checking CONNECTION settings...")
    host = config["CONNECTION"]["HOST"]
    port = config["CONNECTION"]["PORT"]
    
    if host != "styx.ics.uci.edu":
        warnings.append(f"HOST is set to '{host}', expected 'styx.ics.uci.edu'")
    else:
        print(f"   ✓ HOST: {host}")
    
    if port != "9000":
        warnings.append(f"PORT is set to '{port}', expected '9000'")
    else:
        print(f"   ✓ PORT: {port}")
    
    print("\n[3] Checking SEED URLs...")
    seed_urls = config["CRAWLER"]["SEEDURL"].split(",")
    expected_seeds = [
        "https://www.ics.uci.edu",
        "https://www.cs.uci.edu",
        "https://www.informatics.uci.edu",
        "https://www.stat.uci.edu"
    ]
    
    for url in expected_seeds:
        if url in seed_urls:
            print(f"   ✓ {url}")
        else:
            warnings.append(f"Missing seed URL: {url}")
    
    print("\n[4] Checking POLITENESS...")
    politeness = config["CRAWLER"]["POLITENESS"]
    if float(politeness) < 0.5:
        errors.append(f"POLITENESS is {politeness}, must be at least 0.5 seconds")
    else:
        print(f"   ✓ POLITENESS: {politeness} seconds")
    
    # Check thread count
    print("\n[5] Checking THREADCOUNT...")
    thread_count = config["LOCAL PROPERTIES"]["THREADCOUNT"]
    if int(thread_count) > 1:
        warnings.append(f"THREADCOUNT is {thread_count}. Make sure you've implemented multithreading correctly!")
    else:
        print(f"   ✓ THREADCOUNT: {thread_count}")
    
    # Check dependencies
    print("\n[6] Checking dependencies...")
    try:
        import bs4
        print("   ✓ beautifulsoup4 installed")
    except ImportError:
        errors.append("beautifulsoup4 not installed. Run: pip install beautifulsoup4")
    
    try:
        import lxml
        print("   ✓ lxml installed")
    except ImportError:
        errors.append("lxml not installed. Run: pip install lxml")