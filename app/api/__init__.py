from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.api.r_div_inject import injRou
from app.api.r_div_show import divRou
from app.api.r_reserve import reserveRou
from app.api.r_div_rag import divRagRou

rou = APIRouter()

@rou.get("/")
def rouGet():
    return RedirectResponse(url="https://ainvoaice.com")


rou.include_router(divRagRou, prefix="/divrag", tags=["Rag"])
rou.include_router(injRou, prefix="/div2pg", tags=["From Nasdaq to Postgres"])
rou.include_router(divRou, prefix="/div_show", tags=["Div Table"])




rou.include_router(reserveRou, prefix="/reserve", tags=["Reserve"])
