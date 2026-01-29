# app/api/routes/reports.py
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_db
from app.service.ser_div_chunk import DividendChunkService
from app.service.ser_div_embedding import EmbeddingService

divRagRou = APIRouter()


@divRagRou.post("/rebuild-chunks",summary="Rebuild dividend_chunks from dividends",)
async def rebuild_dividend_chunks(
    db: AsyncSession = Depends(get_db),
):
    service = DividendChunkService(db)
    return await service.rebuild_chunks()



@divRagRou.post("/embed-all")
async def embed_all_wages(
    db: AsyncSession = Depends(get_db),
):
    count = EmbeddingService.embed_all_dummy(db)
    return {"embedded": count}