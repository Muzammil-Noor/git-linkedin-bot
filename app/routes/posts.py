from fastapi import APIRouter

from app.services.github_service import (
    get_repositories,
    get_weekly_commits
)

from app.services.grouping_service import (
    group_commits_by_repo
)

router = APIRouter()


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