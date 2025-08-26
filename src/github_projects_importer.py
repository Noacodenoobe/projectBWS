"""
Imports tasks from JSON into GitHub Projects (Classic or Beta).
Requires: GITHUB_TOKEN, PROJECT_ID, and optional COLUMN_ID (Classic) in .env file.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
COLUMN_ID = os.getenv("COLUMN_ID")  # Only for classic Projects
IS_BETA = os.getenv("PROJECTS_BETA", "true").lower() == "true"

# For Projects Beta (v2) – requires GraphQL API
def github_projects_beta_create_issue(title, note):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    query = """
    mutation($projectId:ID!, $title:String!, $note:String!) {
      addProjectV2ItemByTitle(input: {projectId: $projectId, title: $title, note: $note}) {
        item { id }
      }
    }
    """
    variables = {"projectId": PROJECT_ID, "title": title, "note": note}
    r = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    return r.status_code, r.text

# For Classic Projects
def github_projects_classic_create_card(title):
    url = f"https://api.github.com/projects/columns/{COLUMN_ID}/cards"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }
    data = {"note": title}
    r = requests.post(url, headers=headers, json=data)
    return r.status_code, r.text

def import_tasks(json_path):
    with open(json_path, "r", encoding='utf-8') as f:
        tasks = json.load(f)
    for task in tasks:
        title = task["title"]
        note = f"Assignee: {task.get('assignee')}\nDue: {task.get('due_date')}\nPriority: {task.get('priority')}"
        if IS_BETA:
            code, resp = github_projects_beta_create_issue(title, note)
        else:
            code, resp = github_projects_classic_create_card(f"{title}\n{note}")
        print(f"Task '{title}': HTTP {code} -> {resp}")

if __name__ == "__main__":
    import_tasks("data/sample_tasks.json")