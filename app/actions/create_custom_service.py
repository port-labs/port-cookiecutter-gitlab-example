from cookiecutter.main import cookiecutter

from actions.base_create_service import BaseCreateService
from utils import get_unique_output_dir
from core.config import settings


class CreateCustomService(BaseCreateService):

    def _create_cookiecutter(self, props: dict):
        cookiecutter_template_url = add_token_to_url(
            props.pop("cookiecutter_template_url"), settings.GITLAB_ACCESS_TOKEN)

        return cookiecutter(cookiecutter_template_url, extra_context=props,
                            no_input=True, output_dir=get_unique_output_dir())


def add_token_to_url(url: str, token: str) -> str:
    if settings.PRIVATE_REPOSITORY == False:
        return url

    oauth2_token = f"oauth2:{token}"
    url_parts = url.split("://")
    if len(url_parts) != 2:
        raise ValueError("Invalid URL format")
    protocol, path = url_parts
    return f"{protocol}://{oauth2_token}@{path}"
