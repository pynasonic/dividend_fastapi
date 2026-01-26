from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
# from app.api.r_report import reportRou

from app.api.r_div import divRou

rou = APIRouter()

@rou.get("/")
def rouGet():
    return RedirectResponse(url="https://ainvoaice.com")


rou.include_router(divRou, prefix="/wages", tags=["Wages"])
