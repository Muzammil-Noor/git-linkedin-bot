import httpx
from datetime import datetime, timedelta, UTC

from app.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }


async def get_repositories():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user/repos",
            headers=get_headers(),
            params={
                "per_page": 100
            }
        )

    response.raise_for_status()

    return response.json()

async def get_repo_commits(owner: str, repo: str):
    one_week_ago = (
        datetime.now(UTC) - timedelta(days=7)
    ).isoformat()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/repos/{owner}/{repo}/commits",
            headers=get_headers(),
            params={
                "since": one_week_ago,
                "per_page": 100
            }
        )

    response.raise_for_status()

    return response.json()

def normalize_commit(repo_name: str, commit_data):
    commit = commit_data["commit"]

    return {
        "repo": repo_name,
        "message": commit["message"],
        "author": commit["author"]["name"],
        "date": commit["author"]["date"],
        "sha": commit_data["sha"]
    }

async def get_weekly_commits():
    repos = await get_repositories()
    print("Repos Fetched")

    all_commits = []

    for repo in repos:
        repo_name = repo["name"]
        owner = repo["owner"]["login"]
        print("Fetching",repo_name,"commits")

        try:
            commits = await get_repo_commits(
                owner,
                repo_name
            )

            normalized = [
                normalize_commit(repo_name, commit)
                for commit in commits
            ]

            all_commits.extend(normalized)

        except Exception as e:
            print(f"Error fetching {repo_name}: {e}")

    return all_commits