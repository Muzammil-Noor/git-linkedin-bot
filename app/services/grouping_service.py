import re
from collections import defaultdict

def group_commits_by_repo(commits):
    grouped = defaultdict(list)

    for commit in commits:
        if "Muzammil".lower() in commit["author"].lower():
            grouped[commit["repo"]].append(commit)

    return dict(grouped)

def flatten_commit_messages(commits):
    """
    Input: list of commits
    Output: list of commit messages
    """
    return [commit["message"] for commit in commits]

def auto_group_repos(grouped_by_repo: dict):
    project_groups = defaultdict(list)

    for repo_name, commits in grouped_by_repo.items():
        # Extract prefix before dash or underscore
        match = re.match(r"([a-zA-Z0-9]+)[-_]?", repo_name)
        project_name = match.group(1).capitalize() if match else repo_name
        project_groups[project_name].extend(commits)

    return dict(project_groups)