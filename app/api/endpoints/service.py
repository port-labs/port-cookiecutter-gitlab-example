import logging
from fastapi import APIRouter, Depends

from api.deps import verify_webhook
from clients import port
from core.config import settings
from schemas.webhook import Webhook
from actions.create_custom_service import CreateCustomService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

should_verify_webhook = settings.VERIFY_WEBHOOK
print(f"should_verify_webhook: {should_verify_webhook}")
deps = [Depends(verify_webhook)] if should_verify_webhook else None


@router.post("/service", dependencies=deps)
async def handle_create_service_webhook(webhook: Webhook):
    logger.info(f"Webhook body: {webhook}")
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    repo = properties.pop('repository_name')
    run_id = webhook.context.runId
    performed_on_bp = webhook.context.blueprint

    if action_type == 'CREATE':
        group_name_from_user_input = properties.pop('group_name')
        group_name = group_name_from_user_input
        if not group_name:
            group_name = settings.group_NAME
        else:
            group_name = group_name.replace('___', '/')

        logger.info(f"{action_identifier} - create new service")
        action_status = CreateCustomService().create(repo, group_name, properties)
        message = f"{action_identifier} - action status after creating service is {action_status}"

        if action_status == 'SUCCESS':
            entity_properties = {
                'description': next(iter([value for key, value in properties.items() if 'description' in key.lower()]),
                                    ''),
                'url': f"https://{settings.GITLAB_DOMAIN}/{group_name}/{repo}"
            }

            create_status = port.create_entity(blueprint=performed_on_bp,
                                               title=f"{group_name}/{repo}",
                                               properties=entity_properties, run_id=run_id, relations={"group": group_name_from_user_input})
            action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
            message = f"{message}, after creating entity is {action_status}"

        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
