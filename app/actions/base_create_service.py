import logging
import git
import shutil
from typing import Literal, Union

from clients import git, gitlab

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseCreateService:
    def create(self, repo_name: str, props: dict) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
        project_dir = None
        # try get group_name from props or settings
        group_name = props.get('group_name')
        if not group_name:
            group_name = gitlab.settings.GITLAB_GROUP_NAME

        try:
            logger.info(f"{self.__class__.__name__} - create cookiecutter")
            project_dir = self._create_cookiecutter(props)
            logger.info(f"{self.__class__.__name__} - create gitlab repo")
            gitlab.create_repo(repo_name, group_name)
            logger.info(f"{self.__class__.__name__} - init git repo")
            repo = git.init_repo(project_dir)
            logger.info(f"{self.__class__.__name__} - upload files to gitlab")
            git.upload_all_files(repo, repo_name, group_name)
            logger.info(f"{self.__class__.__name__} - success")
            return 'SUCCESS'
        except Exception as err:
            logger.error(f"{self.__class__.__name__} - error: {err}")
        finally:
            if project_dir:
                shutil.rmtree(project_dir)

        return 'FAILURE'

    def _create_cookiecutter(self, props: dict):
        raise NotImplementedError(
            "Subclasses should implement '_create_cookiecutter'")
