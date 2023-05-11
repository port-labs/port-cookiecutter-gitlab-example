import logging
import time
from core.config import settings
from clients import port, gitlab

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_groups_by_period():
    period = settings.GITLAB_SYNC_GROUPS_PERIOD
    logger.info(f"Checking if needed to sync groups by period {period}")
    if period > 0:
        logger.info(f"Syncing groups by period {period}")
        # every period of time get the gitlab groups and sync them to port
        logger.info(f"Syncing groups every {period} seconds")
        while True:
            sync_groups_to_port()
            time.sleep(period)


def sync_groups_to_port():
    logger.info(f"Syncing groups")
    groups = gitlab.get_all_groups_and_sub_groups()
    for group in groups:
        logger.info(f"Syncing group {group}")
        logger.info(f"Syncing group {group.name}")
        port.create_entity('gitlab_groups', title=group.name,
                           identifier=group.full_path.replace('/', '___'), properties={'url': group.web_url}, run_id=None)
        logger.info(f"Syncing groups finished")
