from django.shortcuts import render
from .reptotext import GithubRepoScraper
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def main(request):
    return render(request, 'Parser/scrape.html') 

@csrf_exempt
def scrape(request):
    print('Scraping...')
    print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        repo_url = data.get('repoUrl')
        doc_url = data.get('docUrl')
        print(repo_url)
        selected_file_types = data.get('selectedFileTypes', [])
        if not repo_url:
            return JsonResponse({"error": "Repo URL not provided."}, status=400)
        repo_name = repo_url.split('github.com/')[-1]
        scraper = GithubRepoScraper(repo_name, doc_url, selected_file_types)
        filename = scraper.run()

        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()

        return JsonResponse({"response": file_content})