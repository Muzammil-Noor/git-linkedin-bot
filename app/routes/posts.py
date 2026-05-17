from fastapi import APIRouter

from app.services.github_service import (
    get_repositories,
    get_weekly_commits
)

from app.services.grouping_service import (
    group_commits_by_repo
)

from app.services.grouping_service import (
    auto_group_repos
)
from app.services.ai_service import generate_linkedin_post
import asyncio

router = APIRouter()

@router.get("/linkedin-posts")
async def linkedin_posts():
    commits = await get_weekly_commits()
    grouped_repos = group_commits_by_repo(commits)
    grouped_projects = auto_group_repos(grouped_repos)

    posts = {}

    tasks = [
        generate_linkedin_post(project_name, [c["message"] for c in commits])
        for project_name, commits in grouped_projects.items()
    ]
    results = await asyncio.gather(*tasks)

    for project_name, post_text in zip(grouped_projects.keys(), results):
        posts[project_name] = post_text

    return posts


@router.get("/repos")
async def repos():
    return await get_repositories()


@router.get("/weekly-commits")
async def weekly_commits():
    return await get_weekly_commits()


@router.get("/grouped-commits")
async def grouped_commits():
    commits = await get_weekly_commits()

    return group_commits_by_repo(commits)

@router.get("/dynamic-grouped-project-commits")
async def dynamic_grouped_project_commits():
    commits = await get_weekly_commits()
    grouped_repos = group_commits_by_repo(commits)
    grouped_projects = auto_group_repos(grouped_repos)
    return grouped_projects