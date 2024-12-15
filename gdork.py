import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

class GoogleDorkScanner:
    def __init__(self, output_file="sonuçlar.txt"):

        self.base_url = "https://www.google.com/search"
        self.output_file = output_file

    def search_dork(self, dork_query, num_results=10):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        params = {
            "q": dork_query,
            "num": num_results
        }

        # Encode URL parameters
        encoded_query = urllib.parse.urlencode(params)
        search_url = f"{self.base_url}?{encoded_query}"

        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for item in soup.select(".tF2Cxc a"):
                link = item["href"]
                links.append(link)
            return links
        else:
            return f"Error: {response.status_code} - {response.reason}"

    def save_results(self, results):
    
        with open(self.output_file, "a") as file:
            for link in results:
                file.write(f"{link}\n")

if __name__ == "__main__":
    # ANSI color code for green
    GREEN = "\033[92m"
    RESET = "\033[0m"

    # ASCII Banner with Creator Info in Green
    banner = f"""
{GREEN}
██████╗     ██████╗  ██████╗ ██████╗ ██╗  ██╗
██╔════╝     ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
██║  ███╗    ██║  ██║██║   ██║██████╔╝█████╔╝ 
██║   ██║    ██║  ██║██║   ██║██╔══██╗██╔═██╗ 
╚██████╔╝    ██████╔╝╚██████╔╝██║  ██║██║  ██╗
 ╚═════╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
              Bu Araç Taxo Tarafından Yapılmıştır 
            
{RESET}
"""
    print(banner)

    # Interactive prompts
    print("[+] Google Dork Scannerimize Hoş Geldiniz!")
    dork_query = input("[+] Aranacak Dorkunuzu Giriniz: ").strip()
    num_results = input("[+] Ne Kadar Web Sayfası Görüntüleyelim: ").strip()
    
    # Validate input
    try:
        num_results = int(num_results)
        if num_results <= 0:
            raise ValueError
    except ValueError:
        print("[-] Geçersiz sonuç sayısı. Lütfen pozitif bir tamsayı girin.")
        exit()

    # Create scanner instance
    scanner = GoogleDorkScanner()

    print(f"\n[+] Dork Aranıyor: {dork_query}")
    results = scanner.search_dork(dork_query, num_results=num_results)
    
    if isinstance(results, list):
        print("\n[+] Sonuçlar:")
        for link in results:
            print(link)
    else:
        print(results)

    # Save results to file
    scanner.save_results(results)
    print(f"\n[+] Sonuçlar sonuçlar.txt Dosyasına Kaydedildi Dizinin İçine Bakınız {scanner.output_file}.")
