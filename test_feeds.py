#!/usr/bin/env python3
"""
RSS Feed Testing Script
Tests all RSS feeds in rss_feeds.json and reports which ones work/fail
"""

import requests
import xml.etree.ElementTree as ET
import json
import time
import sys
from datetime import datetime

def load_rss_feeds():
    """Load RSS feed URLs from JSON file"""
    try:
        with open('rss_feeds.json', 'r') as f:
            data = json.load(f)
            return data.get('feeds', [])
    except FileNotFoundError:
        print("❌ Error: rss_feeds.json not found")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in rss_feeds.json")
        return []

def test_rss_feed(url, timeout=10):
    """Test a single RSS feed URL"""
    start_time = time.time()

    try:
        # Try to fetch the RSS feed
        response = requests.get(url, timeout=timeout, headers={
            'User-Agent': 'MatrixRain-RSS-Checker/1.0'
        })
        response_time = time.time() - start_time

        if response.status_code != 200:
            return {
                'url': url,
                'status': 'HTTP_ERROR',
                'error': f'Status code: {response.status_code}',
                'response_time': response_time
            }

        # Try to parse the XML
        try:
            root = ET.fromstring(response.text)

            # Check if it has RSS structure
            if root.tag in ['rss', 'feed'] or root.find('.//channel') or root.find('.//item'):
                return {
                    'url': url,
                    'status': 'SUCCESS',
                    'response_time': response_time,
                    'content_length': len(response.text)
                }
            else:
                return {
                    'url': url,
                    'status': 'INVALID_XML',
                    'error': 'No RSS/feed structure found',
                    'response_time': response_time
                }

        except ET.ParseError as e:
            return {
                'url': url,
                'status': 'PARSE_ERROR',
                'error': f'XML parse error: {str(e)[:100]}',
                'response_time': response_time
            }

    except requests.RequestException as e:
        response_time = time.time() - start_time
        return {
            'url': url,
            'status': 'REQUEST_ERROR',
            'error': str(e),
            'response_time': response_time
        }

def main():
    """Main testing function"""
    print("🔍 RSS Feed Testing Script")
    print("=" * 50)

    # Load RSS feeds
    feeds = load_rss_feeds()
    if not feeds:
        print("❌ No RSS feeds found to test")
        return

    print("📋 Testing {} RSS feeds...".format(len(feeds)))
    print()

    # Test results
    results = {
        'SUCCESS': [],
        'HTTP_ERROR': [],
        'REQUEST_ERROR': [],
        'PARSE_ERROR': [],
        'INVALID_XML': []
    }

    working_count = 0
    total_response_time = 0

    # Test each feed
    for i, url in enumerate(feeds, 1):
        print("Testing {:2d}/{:2d}: {}".format(i, len(feeds), url))

        result = test_rss_feed(url)
        results[result['status']].append(result)

        if result['status'] == 'SUCCESS':
            working_count += 1
            total_response_time += result['response_time']
            print("  ✅ SUCCESS ({:.2f}s, {} chars)".format(result['response_time'], result['content_length']))
        else:
            print("  ❌ {}: {}".format(result['status'], result['error'][:60]))

        # Small delay to be respectful to servers
        time.sleep(0.1)

    # Print summary
    print()
    print("📊 SUMMARY RESULTS")
    print("=" * 50)

    total_feeds = len(feeds)
    success_rate = (working_count / total_feeds) * 100

    print("✅ Working feeds: {}/{} ({:.1f}%)".format(working_count, total_feeds, success_rate))

    if working_count > 0:
        avg_response_time = total_response_time / working_count
        print("⏱️  Average response time: {:.2f}s".format(avg_response_time))

    print()
    print("📋 DETAILED BREAKDOWN:")
    print("-" * 30)

    for status, feeds_list in results.items():
        if feeds_list:
            count = len(feeds_list)
            percentage = (count / total_feeds) * 100
            print("  {}: {} feeds ({:.1f}%)".format(status, count, percentage))

    # Save results to log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"feed_test_results_{timestamp}.log"

    with open(log_filename, 'w') as f:
        f.write("RSS Feed Test Results\n")
        f.write("Generated: {}\n".format(datetime.now().isoformat()))
        f.write("=" * 50 + "\n\n")

        f.write("Total feeds tested: {}\n".format(total_feeds))
        f.write("Working feeds: {} ({:.1f}%)\n".format(working_count, success_rate))

        if working_count > 0:
            avg_response = total_response_time / working_count
            f.write("Average response time: {:.2f}s\n".format(avg_response))

        f.write("\nDETAILED RESULTS:\n")
        f.write("-" * 30 + "\n\n")

        for status, feeds_list in results.items():
            if feeds_list:
                f.write("\n{} ({} feeds):\n".format(status, len(feeds_list)))
                for feed_result in feeds_list:
                    f.write("  URL: {}\n".format(feed_result['url']))
                    if 'error' in feed_result:
                        f.write("  Error: {}\n".format(feed_result['error']))
                    if 'response_time' in feed_result:
                        f.write("  Response time: {:.2f}s\n".format(feed_result['response_time']))
                    f.write("\n")

    print("\n💾 Results saved to: {}".format(log_filename))

    # Print working feeds for easy copying
    if results['SUCCESS']:
        print("\n✅ WORKING FEEDS (copy these to use only reliable feeds):")
        print("-" * 50)
        for feed_result in results['SUCCESS']:
            print('    "{}",'.format(feed_result["url"]))

    return working_count, total_feeds

if __name__ == "__main__":
    try:
        working, total = main()
        print("\n🎯 Test completed: {}/{} feeds working".format(working, total))

        if working == 0:
            print("⚠️  No working feeds found!")
            sys.exit(1)
        elif working < total * 0.5:
            print("⚠️  Less than 50% of feeds are working")
            sys.exit(1)
        else:
            print("✅ Feed testing completed successfully!")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Unexpected error: {}".format(e))
        sys.exit(1)
