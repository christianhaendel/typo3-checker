import requests
from bs4 import BeautifulSoup
import csv
from colorama import init, Fore, Style

init(autoreset=True)

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text, response.headers
    except requests.RequestException as e:
        raise Exception(f"Error fetching URL: {e}")
    return "", {}

def detect_typo3_in_html(html):
    return 'typo3' in html.lower()

def detect_typo3_in_resources(html):
    soup = BeautifulSoup(html, 'html.parser')
    resource_urls = []
    for tag in soup.find_all(['script', 'link', 'img']):
        src = tag.get('src') or tag.get('href')
        if src:
            resource_urls.append(src.lower())
    for url in resource_urls:
        if 'typo3' in url or 'fileadmin' in url:
            return True
    return False

def detect_typo3_in_robots(domain):
    try:
        if not domain.startswith("http"):
            domain = "http://" + domain
        robots_url = domain.rstrip('/') + "/robots.txt"
        response = requests.get(robots_url, timeout=5)
        if "typo3" in response.text.lower():
            return True
    except requests.RequestException:
        pass
    return False

def detect_typo3_in_headers(headers):
    for key, value in headers.items():
        if 'typo3' in key.lower() or 'typo3' in value.lower():
            return True
    return False

def detect_typo3_in_meta(html):
    soup = BeautifulSoup(html, 'html.parser')
    generator = soup.find("meta", attrs={"name": "generator"})
    if generator and 'typo3' in generator.get("content", "").lower():
        return True
    return False

def process_urls(input_path, output_path):
    with open(input_path, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    results = []
    count_yes = 0
    count_no = 0
    count_error = 0

    for url in urls:
        result = "No"
        note = "No TYPO3 indicator found"
        try:
            html, headers = fetch_html(url)
            if detect_typo3_in_headers(headers):
                result = "Yes"
                note = "Detected in HTTP header"
            elif detect_typo3_in_meta(html):
                result = "Yes"
                note = "Detected in meta tag 'generator'"
            elif detect_typo3_in_html(html):
                result = "Yes"
                note = "Detected in HTML content"
            elif detect_typo3_in_resources(html):
                result = "Yes"
                note = "Detected in resource paths"
            elif detect_typo3_in_robots(url):
                result = "Yes"
                note = "Detected in robots.txt"

            if result == "Yes":
                print(f"{url}: {Fore.GREEN}Yes{Style.RESET_ALL} – {note}")
                count_yes += 1
            else:
                print(f"{url}: {Fore.YELLOW}No{Style.RESET_ALL} – {note}")
                count_no += 1
        except Exception as e:
            result = "Error"
            note = str(e)
            print(f"{url}: {Fore.RED}Error{Style.RESET_ALL} – {note}")
            count_error += 1

        results.append({
            'URL': url,
            'TYPO3 detected': result,
            'Comment': note
        })

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'TYPO3 detected', 'Comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    input_path = input("Source file (.txt): ").strip()
    output_path = input("Output file name (.csv): ").strip()
    if not output_path.lower().endswith('.csv'):
        output_path += '.csv'
    print("===========================================")
    print("Start URL-Checking")
    process_urls(input_path, output_path)
    print("===========================================")
    print("Done. Results saved to:", output_path)
    print("===========================================")
    print("Summary:")
    print(f"  TYPO3 websites detected: {count_yes}")
    print(f"  Non-TYPO3 websites: {count_no}")
    print(f"  Errors encountered: {count_error}")
