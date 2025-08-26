import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("GITHUB_PROJECT_ID")
ORG = os.getenv("GITHUB_ORG")
REPO = os.getenv("GITHUB_REPO")

def create_project_item(title, assignee=None, status="Todo"):
    url = f"https://api.github.com/projects/columns/{PROJECT_ID}/cards"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }
    data = {
        "note": title
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)

if __name__ == "__main__":
    # TODO: Załaduj zadania z pliku JSON lub wygenerowane przez LLM
    tasks = [
        {"title": "Przygotować środowisko Docker", "assignee": None, "status": "Todo"},
        {"title": "Skonfigurować Whisper.cpp", "assignee": "Noacodenoobe", "status": "In Progress"}
    ]
    for task in tasks:
        create_project_item(task["title"], task.get("assignee"), task.get("status"))