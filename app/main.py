import threading
import uvicorn
from fastapi import FastAPI

from api.endpoints.service import router
from sync_groups import sync_groups_by_period
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(router, prefix=settings.API_STR)

sync_thread = threading.Thread(target=sync_groups_by_period)
sync_thread.start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
