from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "port-cookiecutter-gitlab-example"

    VERIFY_WEBHOOK: bool = False

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    GITLAB_ACCESS_TOKEN: str
    GITLAB_DOMAIN: str = "gitlab.com"
    GITLAB_GROUP_NAME: str
    PRIVATE_REPOSITORY: bool = True

    COOKIECUTTER_OUTPUT_DIR: str = "cookiecutter_output/{uuid}"

    class Config:
        case_sensitive = True


settings = Settings()
