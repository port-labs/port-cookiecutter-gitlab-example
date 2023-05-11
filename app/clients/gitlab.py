import logging

from gitlab import Gitlab

from core.config import settings

gl = Gitlab(url=f"https://{settings.GITLAB_DOMAIN}",
            private_token=settings.GITLAB_ACCESS_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_repo(repo_name: str, group_name: str):
    logger.info(f"Creating repo {repo_name}")
    logger.info(f"Getting Gitlab groups")
    group_ids = gl.groups.list(search=group_name)
    if not group_ids:
        logger.error(f"Group not found {group_ids}")
        raise Exception("Group not found")
    group_id = group_ids[0].id
    logger.info(f"Creating repo {repo_name} in group {group_id}")
    gl.projects.create({'name': repo_name, 'namespace_id': group_id})


def get_all_groups_and_sub_groups():
    logger.info(f"Getting Gitlab groups")
    groups = gl.groups.list(all=True)
    return groups
