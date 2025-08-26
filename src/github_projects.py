import os
import requests
import json

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("GITHUB_PROJECT_ID", "11")  # Back to project number
ORG = os.getenv("GITHUB_ORG", "Noacodenoobe")
REPO = os.getenv("GITHUB_REPO", "projectBWS")

def get_project_info():
    """Pobiera informacje o projekcie GitHub używając REST API v1"""
    url = f"https://api.github.com/projects/{PROJECT_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }

    print(f"Querying project info with project ID: {PROJECT_ID}")
    response = requests.get(url, headers=headers)
    print(f"Project info response: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Project info result: {json.dumps(result, indent=2)}")
        return result
    else:
        print(f"Error getting project info: {response.text}")
        return None

def create_project_item(title, assignee=None, status="Todo"):
    """Tworzy nowy element w projekcie GitHub używając REST API v1"""
    url = f"https://api.github.com/projects/columns"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }

    # Najpierw pobierz informacje o projekcie
    project_info = get_project_info()
    if not project_info:
        print("Nie udało się pobrać informacji o projekcie")
        return False

    try:
        project_id = project_info["id"]
        print(f"Found project ID: {project_id}")
    except (KeyError, TypeError) as e:
        print(f"Error extracting project ID: {e}")
        print(f"Project info structure: {json.dumps(project_info, indent=2)}")
        return False

    # Pobierz kolumny projektu
    columns_url = f"https://api.github.com/projects/{project_id}/columns"
    columns_response = requests.get(columns_url, headers=headers)
    
    if columns_response.status_code != 200:
        print(f"Error getting project columns: {columns_response.text}")
        return False
    
    columns = columns_response.json()
    if not columns:
        print("No columns found in project")
        return False
    
    # Użyj pierwszej kolumny (zazwyczaj "To Do")
    first_column = columns[0]
    column_id = first_column["id"]
    print(f"Using column: {first_column['name']} (ID: {column_id})")

    # Utwórz kartę w kolumnie
    card_url = f"https://api.github.com/projects/columns/{column_id}/cards"
    card_data = {
        "note": title
    }

    print(f"Creating card with title: {title}")
    card_response = requests.post(card_url, headers=headers, json=card_data)
    print(f"Create card response: {card_response.status_code}")

    if card_response.status_code == 201:
        result = card_response.json()
        print(f"Successfully created card: {result}")
        return True
    else:
        print(f"Error creating card: {card_response.text}")
        return False

if __name__ == "__main__":
    print(f"Starting GitHub Projects import...")
    print(f"ORG: {ORG}")
    print(f"REPO: {REPO}")
    print(f"PROJECT_ID: {PROJECT_ID}")

    # Testowe zadania
    tasks = [
        {"title": "Przygotować środowisko Docker", "assignee": None, "status": "Todo"},
        {"title": "Skonfigurować Whisper.cpp", "assignee": "Noacodenoobe", "status": "In Progress"},
        {"title": "Naprawić GitHub Actions workflow", "assignee": None, "status": "Todo"}
    ]

    success_count = 0
    for task in tasks:
        if create_project_item(task["title"], task.get("assignee"), task.get("status")):
            success_count += 1

    print(f"Import completed. Successfully created {success_count}/{len(tasks)} items.")