# app/api/routes/wage.py
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_db
from app.service.ser_wage import WageService

divRou = APIRouter()


@divRou.post("/upload")
async def upload_reports(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    await WageService.upload_csv(db, content)
    return {"status": "ok"}


@divRou.get("/")
async def list_reports(
    db: AsyncSession = Depends(get_db),
):
    return await WageService.list_wages(db)



@divRou.get("/pagination")
async def list_wages(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    return await WageService.list_paginated(
        db=db,
        page=page,
        page_size=page_size,
    )
    
    
