import json
import os
import time
from collections import Counter

def load_analytics():
    if os.path.exists("analytics.json"):
        with open("analytics.json", 'r') as f:
            return json.load(f)
    return None

def display_stats():
    analytics = load_analytics()
    
    if not analytics:
        print("No analytics file found. Crawler hasn't started yet.")
        return
    
    print("\n" + "=" * 80)
    print("CRAWLER PROGRESS MONITOR")
    print("=" * 80)
    
    # Basic stats
    unique_pages = len(analytics.get('unique_pages', []))
    print(f"\nUnique pages crawled: {unique_pages}")
    
    # Longest page
    longest = analytics.get('longest_page', {})
    if longest.get('url'):
        print(f"\nLongest page so far:")
        print(f"  URL: {longest['url']}")
        print(f"  Words: {longest['word_count']}")
    
    all_words = Counter(analytics.get('all_words', {}))
    print(f"\nTop 10 most common words:")
    for i, (word, count) in enumerate(all_words.most_common(10), 1):
        print(f"  {i:2}. {word:20} - {count:6} occurrences")
    
    # Subdomains
    subdomains = analytics.get('subdomains', {})
    print(f"\nSubdomains discovered: {len(subdomains)}")
    sorted_subs = sorted(subdomains.items(), key=lambda x: x[1], reverse=True)[:10]
    for subdomain, count in sorted_subs:
        print(f"  {subdomain:40} - {count:5} pages")
    
    if os.path.exists("frontier.shelve.db") or os.path.exists("frontier.shelve"):
        print(f"\nFrontier file exists (crawler has progress saved)")
    
    print("\n" + "=" * 80)
    print(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

def monitor_continuous():
    """Monitor continuously with updates every 10 seconds"""
    print("Starting continuous monitoring (Ctrl+C to stop)...")
    try:
        while True:
            os.system('clear' if os.name != 'nt' else 'cls')
            display_stats()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        monitor_continuous()
    else:
        display_stats()
        print("\nTip: Run 'python3 monitor.py --continuous' for live updates every 10 seconds")