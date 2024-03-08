import os
import re
import time
from datetime import datetime
from github import Github, RateLimitExceededException
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class GithubRepoScraper:
    """Scrape GitHub repositories."""
    def __init__(self, repo_name, doc_link=None, selected_file_types=None):
        if selected_file_types is None:
            selected_file_types = []
        self.github_api_key = os.getenv("GITHUB_API_KEY")
        print(f"Using GitHub API Key: {self.github_api_key}")  # Debugging line, remove if necessary
        self.repo_name = repo_name
        self.doc_link = doc_link
        self.selected_file_types = selected_file_types

    def fetch_all_files(self, max_retries=5, delay=2, backoff=2):
        """Fetch all files from the GitHub repository with retry logic."""
        attempts = 0
        while attempts < max_retries:
            try:
                github_instance = Github(self.github_api_key)
                repo = github_instance.get_repo(self.repo_name)
                contents = repo.get_contents("/")
                return self.recursive_fetch_files(repo, contents)
            except RateLimitExceededException:
                attempts += 1
                sleep_time = delay * backoff ** (attempts - 1)
                print(f"Rate limit exceeded, retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            except Exception as e:
                print(f"Failed to fetch files: {e}")
                break  # If there's another type of exception, break out of loop
        raise Exception("Failed to fetch files after several attempts")

    def recursive_fetch_files(self, repo, contents):
        """Recursively fetch files from a GitHub repository."""
        files_data = []
        for content_file in contents:
            if content_file.type == "dir":
                # Recurse into directories
                more_files = self.recursive_fetch_files(repo, repo.get_contents(content_file.path))
                files_data.extend(more_files)  # Append the results from the directory
            else:
                # Check if the file is of a type we're interested in
                if any(content_file.name.endswith(file_type) for file_type in self.selected_file_types) or not self.selected_file_types:
                    file_content = "\n'''--- " + content_file.path + " ---\n"
                    if content_file.encoding == "base64":
                        try:
                            file_content += content_file.decoded_content.decode("utf-8")
                        except UnicodeDecodeError:
                            file_content += "[Content not decodable]"
                    elif content_file.encoding == "none":
                        print(f"Warning: Skipping {content_file.path} due to unsupported encoding 'none'.")
                        continue
                    else:
                        print(f"Warning: Skipping {content_file.path} due to unexpected encoding '{content_file.encoding}'.")
                        continue
                    file_content += "\n'''"
                    files_data.append(file_content)
        return files_data


    def scrape_doc(self):
        """Scrape documentation from a webpage."""
        print("scrape_doc")
        if not self.doc_link:
            return ""
        try:
            page = requests.get(self.doc_link, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup.get_text(separator="\n")
        except RequestException as e:
            print(f"Error fetching documentation: {e}")
            return ""

    def write_to_file(self, files_data):
        """Build a .txt file with all of the repository's files."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        directory = 'data'  # Define the directory
        if not os.path.exists(directory):  # Check if the directory exists
            os.makedirs(directory)  # Create the directory if it does not exist
        filename = os.path.join(directory, f"{self.repo_name.replace('/', '_')}_{timestamp}.txt")  # Adjust path as needed
        with open(filename, "w", encoding='utf-8') as f:
            doc_text = self.scrape_doc()
            if doc_text:
                f.write(f"Documentation Link: {self.doc_link}\n\n")
                f.write(doc_text + "\n\n")
            f.write(f"*GitHub Repository \"{self.repo_name}\"*\n")
            for file_data in files_data:
                f.write(file_data)
        return filename

    def clean_up_text(self, filename):
        """Remove excessive line breaks from the text."""
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        cleaned_text = re.sub('\n{3,}', '\n\n', text)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

    def run(self):
        """Execute the scraping process."""
        print("Fetching all files...")
        files_data = self.fetch_all_files()

        print("Writing to file...")
        filename = self.write_to_file(files_data)

        print("Cleaning up file...")
        self.clean_up_text(filename)

        print("Done.")
        return filename
