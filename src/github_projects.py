import os
import requests
import json

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("GITHUB_PROJECT_ID", "11")  # Default to project 11
ORG = os.getenv("GITHUB_ORG", "Noacodenoobe")
REPO = os.getenv("GITHUB_REPO", "projectBWS")

def get_project_info():
    """Pobiera informacje o projekcie GitHub"""
    url = f"https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v4+json"
    }
    
    # Ensure PROJECT_ID is not empty
    project_number = PROJECT_ID if PROJECT_ID else "11"
    
    query = """
    query($org: String!, $projectNumber: Int!) {
      organization(login: $org) {
        projectV2(number: $projectNumber) {
          id
          title
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "org": ORG,
        "projectNumber": int(project_number)
    }
    
    print(f"Querying project info with org: {ORG}, projectNumber: {project_number}")
    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    print(f"Project info response: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Project info result: {json.dumps(result, indent=2)}")
        
        # Check if project exists
        if result.get("data", {}).get("organization", {}).get("projectV2") is None:
            print(f"Project {project_number} not found in organization {ORG}")
            return None
            
        return result
    else:
        print(f"Error getting project info: {response.text}")
        return None

def create_project_item(title, assignee=None, status="Todo"):
    """Tworzy nowy element w projekcie GitHub"""
    url = f"https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v4+json"
    }
    
    # Najpierw pobierz informacje o projekcie
    project_info = get_project_info()
    if not project_info:
        print("Nie udało się pobrać informacji o projekcie")
        return False
    
    try:
        project_id = project_info["data"]["organization"]["projectV2"]["id"]
        print(f"Found project ID: {project_id}")
    except (KeyError, TypeError) as e:
        print(f"Error extracting project ID: {e}")
        print(f"Project info structure: {json.dumps(project_info, indent=2)}")
        return False
    
    # Mutacja do dodania elementu do projektu
    mutation = """
    mutation($projectId: ID!, $title: String!) {
      addProjectV2DraftIssue(input: {
        projectId: $projectId
        title: $title
      }) {
        projectItem {
          id
        }
      }
    }
    """
    
    variables = {
        "projectId": project_id,
        "title": title
    }
    
    print(f"Creating item with title: {title}")
    response = requests.post(url, headers=headers, json={"query": mutation, "variables": variables})
    print(f"Create item response: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Successfully created item: {result}")
        return True
    else:
        print(f"Error creating item: {response.text}")
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