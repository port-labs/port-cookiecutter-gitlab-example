from git import Repo

from core.config import settings

remote_name = "origin"


def init_repo(path):
    return Repo.init(path)


def upload_all_files(repo: Repo, remote_repo: str, group_name: str, commit_msg="Initial Commit", head_branch="main"):
    repo.git.add('.')
    repo.index.commit(commit_msg)
    remote_org = group_name
    remote_url = f"https://oauth2:{settings.GITLAB_ACCESS_TOKEN}@{settings.GITLAB_DOMAIN}/{remote_org}/{remote_repo}"
    repo.create_remote(name=remote_name, url=remote_url)
    branch = repo.create_head(head_branch)
    repo.git.push("--set-upstream", remote_name, branch)
