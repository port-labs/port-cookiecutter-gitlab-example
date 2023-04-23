import logging
from fastapi import APIRouter, Depends

from mappings import ACTION_ID_TO_CLASS_MAPPING
from api.deps import verify_webhook
from clients import port
from core.config import settings
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/service", dependencies=[Depends(verify_webhook)])
async def handle_create_service_webhook(webhook: Webhook):
    logger.info(f"Webhook body: {webhook}")
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    repo = properties.pop('repository_name')
    run_id = webhook.context.runId

    if action_type == 'CREATE':
        logger.info(f"{action_identifier} - create new service")
        action_status = ACTION_ID_TO_CLASS_MAPPING.get(
            action_identifier)().create(repo, properties)
        message = f"{action_identifier} - action status after creating service is {action_status}"

        if action_status == 'SUCCESS':
            entity_properties = {
                'description': next(iter([value for key, value in properties.items() if 'description' in key.lower()]),
                                    ''),
                'url': f"https://{settings.GITLAB_DOMAIN}/{settings.GITLAB_GROUP_NAME}/{repo}"
            }
            create_status = port.create_entity(blueprint=settings.PORT_SERVICE_BLUEPRINT,
                                               title=f"{settings.GITLAB_GROUP_NAME}/{repo}",
                                               properties=entity_properties, run_id=run_id)
            action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
            message = f"{message}, after creating entity is {action_status}"

        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
