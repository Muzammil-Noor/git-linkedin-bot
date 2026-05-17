from collections import defaultdict


def group_commits_by_repo(commits):
    grouped = defaultdict(list)

    for commit in commits:
        if "Muzammil".lower() in commit["author"].lower():
            grouped[commit["repo"]].append(commit)

    return dict(grouped)