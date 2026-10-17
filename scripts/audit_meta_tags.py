#!/usr/bin/env python3
"""
SEO Meta Tags Auditor
Analyzes HTML files or URLs for meta tag completeness and quality.
Usage: python3 audit_meta_tags.py <url_or_file_path>
"""
import sys
import re
import json
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 required. Install: pip3 install beautifulsoup4")
    sys.exit(1)


def load_html(source: str) -> str:
    if source.startswith("http"):
        import urllib.request
        req = urllib.request.Request(source, headers={
            "User-Agent": "Mozilla/5.0 (compatible; SEOAuditor/1.0)"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")
    return Path(source).read_text(encoding="utf-8", errors="replace")


def audit(html: str, url: str = "") -> dict:
    soup = BeautifulSoup(html, "html.parser")
    results = {"url": url, "score": 0, "max_score": 0, "issues": [], "passed": [], "warnings": []}

    def check(condition, points, pass_msg, fail_msg, severity="issue"):
        results["max_score"] += points
        if condition:
            results["score"] += points
            results["passed"].append(pass_msg)
        else:
            (results["issues"] if severity == "issue" else results["warnings"]).append(fail_msg)

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    check(bool(title), 10, f"Title present: \"{title}\"", "Missing <title> tag")
    check(30 <= len(title) <= 60, 5, f"Title length OK ({len(title)} chars)", f"Title length {len(title)} chars (ideal: 30-60)", "warning" if title else "issue")

    # Meta Description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag.get("content", "") if desc_tag else ""
    check(bool(desc), 10, f"Meta description present ({len(desc)} chars)", "Missing meta description")
    check(50 <= len(desc) <= 160, 5, f"Description length OK ({len(desc)} chars)", f"Description length {len(desc)} chars (ideal: 50-160)", "warning" if desc else "issue")

    # Meta Keywords
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    keywords = kw_tag.get("content", "") if kw_tag else ""
    check(bool(keywords), 3, f"Keywords present: {keywords[:80]}...", "Missing meta keywords (low priority but helps)", "warning")

    # Canonical
    canonical = soup.find("link", attrs={"rel": "canonical"})
    check(bool(canonical), 5, f"Canonical URL: {canonical.get('href', '')}" if canonical else "", "Missing canonical URL")

    # Open Graph
    og_title = soup.find("meta", attrs={"property": "og:title"})
    og_desc = soup.find("meta", attrs={"property": "og:description"})
    og_image = soup.find("meta", attrs={"property": "og:image"})
    og_type = soup.find("meta", attrs={"property": "og:type"})
    check(bool(og_title), 5, "OG Title present", "Missing og:title")
    check(bool(og_desc), 5, "OG Description present", "Missing og:description")
    check(bool(og_image), 5, "OG Image present", "Missing og:image (critical for social sharing)")
    check(bool(og_type), 3, "OG Type present", "Missing og:type", "warning")

    # Twitter Card
    tw_card = soup.find("meta", attrs={"name": "twitter:card"})
    check(bool(tw_card), 3, "Twitter Card present", "Missing twitter:card", "warning")

    # Viewport
    viewport = soup.find("meta", attrs={"name": "viewport"})
    check(bool(viewport), 5, "Viewport meta present (mobile-friendly)", "Missing viewport meta tag")

    # Charset
    charset = soup.find("meta", attrs={"charset": True}) or soup.find("meta", attrs={"http-equiv": "Content-Type"})
    check(bool(charset), 3, "Charset declared", "Missing charset declaration", "warning")

    # Robots
    robots = soup.find("meta", attrs={"name": "robots"})
    if robots:
        content = robots.get("content", "")
        check("noindex" not in content, 5, "Page is indexable", f"Page has noindex: {content}")
    else:
        results["max_score"] += 5
        results["score"] += 5
        results["passed"].append("No robots restriction (indexable by default)")

    # Headings
    h1_tags = soup.find_all("h1")
    check(len(h1_tags) == 1, 8, f"Single H1 found: \"{h1_tags[0].get_text(strip=True)[:60]}\"" if h1_tags else "", f"{'No' if not h1_tags else 'Multiple'} H1 tags found ({len(h1_tags)})")
    h2_tags = soup.find_all("h2")
    check(len(h2_tags) >= 1, 3, f"{len(h2_tags)} H2 tags found", "No H2 tags found (add subheadings)", "warning")

    # Images alt text
    images = soup.find_all("img")
    imgs_without_alt = [img.get("src", "?")[:50] for img in images if not img.get("alt")]
    check(len(imgs_without_alt) == 0, 5, f"All {len(images)} images have alt text", f"{len(imgs_without_alt)} images missing alt text: {imgs_without_alt[:3]}")

    # Structured Data
    ld_json = soup.find_all("script", attrs={"type": "application/ld+json"})
    check(bool(ld_json), 8, f"{len(ld_json)} structured data block(s) found", "No structured data (Schema.org) found")

    # Language
    html_tag = soup.find("html")
    lang = html_tag.get("lang", "") if html_tag else ""
    check(bool(lang), 3, f"Language declared: {lang}", "Missing lang attribute on <html>")

    # Hreflang
    hreflang = soup.find_all("link", attrs={"hreflang": True})
    if hreflang:
        results["passed"].append(f"{len(hreflang)} hreflang tags found")

    # Performance hints
    preconnect = soup.find_all("link", attrs={"rel": "preconnect"})
    if preconnect:
        results["passed"].append(f"{len(preconnect)} preconnect hints found")

    # Final score
    results["percentage"] = round(results["score"] / results["max_score"] * 100) if results["max_score"] > 0 else 0
    return results


def print_report(results: dict):
    pct = results["percentage"]
    grade = "A+" if pct >= 95 else "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"

    print(f"\n{'='*60}")
    print(f"  SEO META TAGS AUDIT REPORT")
    print(f"  URL: {results['url'] or 'local file'}")
    print(f"  Score: {results['score']}/{results['max_score']} ({pct}%) — Grade: {grade}")
    print(f"{'='*60}")

    if results["issues"]:
        print(f"\n❌ ISSUES ({len(results['issues'])})")
        for i in results["issues"]:
            print(f"   • {i}")

    if results["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])})")
        for w in results["warnings"]:
            print(f"   • {w}")

    if results["passed"]:
        print(f"\n✅ PASSED ({len(results['passed'])})")
        for p in results["passed"]:
            print(f"   • {p}")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 audit_meta_tags.py <url_or_file_path>")
        sys.exit(1)

    source = sys.argv[1]
    html = load_html(source)
    results = audit(html, source)
    print_report(results)

    if "--json" in sys.argv:
        print("\n--- JSON Output ---")
        print(json.dumps(results, indent=2, ensure_ascii=False))
