
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')