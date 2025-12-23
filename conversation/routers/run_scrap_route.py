from fastapi import APIRouter

from common.response import success_response, error_response
from core.tasks import web_scrapping_task

router = APIRouter()

@router.post("/run-web-scraping")
async def run_web_scraping():
    try:
        await web_scrapping_task()
        return success_response(message="Web scraping task executed successfully.")
    except Exception as e:
        return error_response(message=f"Manual execution failed: {e}", status_code=500)
