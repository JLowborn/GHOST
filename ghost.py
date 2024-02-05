import requests
from urllib.parse import urlencode, unquote
from bs4 import BeautifulSoup
import sys


class GoogleDorker:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.google_domains = [
            "maps.google.com",
            "support.google.com",
            "accounts.google.com",
            "/search?q=",
        ]

    def search(self, query):
        """
        Perform a Google search for the given query.

        Args:
        - query (str): The search query to be performed.

        Returns:
        - list: A list of relevant links extracted from the search results.
        """
        params = {"q": query}
        response = requests.get(
            f"https://www.google.com/search?{urlencode(params)}", headers=self.headers
        )

        if response.status_code == 429:
            # Code 429 means Google is worried about you.
            print("Too many requests. Please wait and try again later.")
            sys.exit()
        elif response.status_code == 200:
            # Parse HTML response and extract links from search results
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for a in soup.select('a[href^="/url?"]'):
                href = a["href"]
                if href.startswith("/url?"):
                    link = href.split("&")[0]
                    link = link.split("=")[1]
                    decoded_link = unquote(link)

                    # Filter out unimportant links based on popular Google domains
                    if not any(
                        domain in decoded_link for domain in self.google_domains
                    ):
                        links.append(decoded_link)
            return links
        else:
            print(f"Error {response.status_code} in request for: {query}")
            return []

    def print_results(self, dork, links):
        """
        Print any found search results based on given dork.

        Args:
        - dork (str): The search query or operator used.
        - links (list): A list of relevant links to be printed.
        """
        if links:
            print(f"\n\033[1mResults for {dork}:\033[0m")
            domain_groups = {}
            for link in links:
                domain = link.split("/")[2]
                domain_groups.setdefault(domain, []).append(link)

            for domain, group_links in domain_groups.items():
                print(f"\033[95m{domain}\033[0m")
                for link in group_links:
                    print(f"  - {link}")
            print("-" * 80)

    def run(self):
        """
        Run the GoogleDorker tool to perform searches based on user input.
        """
        search_term = input("Search query: ").strip()

        # Google dorks
        google_hacking_operators = ["intitle:", "inurl:", "intext:", "site:", "cache:"]

        # Sensitive file extensions
        sensitive_filetypes = [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "odt",
            "rtf",
            "csv",
            "txt",
            "sql",
            "xml",
            "conf",
            "dat",
            "ini",
            "key",
            "bak",
        ]

        # Adding quotes around the search term for exact search
        search_term_quoted = f'"{search_term}"'

        # Perform search for each Google hacking operator without filtering for sensitive file types
        for operator in google_hacking_operators:
            dork = f"{operator}{search_term_quoted}"
            links = self.search(dork)
            self.print_results(dork, links)

        # Perform search specifically for sensitive file types
        for filetype in sensitive_filetypes:
            dork = f"site:{search_term_quoted} filetype:{filetype}"
            links = self.search(dork)
            self.print_results(f"Sensitive Files ({filetype})", links)


# Instantiate GoogleDorker and run the script
dorker = GoogleDorker()
dorker.run()
