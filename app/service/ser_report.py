# app/services/report_service.py
import csv
import io
from datetime import datetime
from app.db.models.m_div import Report
from app.db.repo.repo_report import ReportRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update


class ReportService:

    @staticmethod
    async def upload_csv(
        db: AsyncSession,
        file_bytes: bytes,
    ) -> None:
        text = file_bytes.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))

        reports: list[Report] = []

        for row in reader:
            content = f"""
                        Lead owner is {row['Lead Owner']}.
                        Source is {row['Source']}.
                        Deal stage is {row['Deal Stage']}.
                        Account ID is {row['Account Id']}.
                        Contact name is {row['First Name']} {row['Last Name']}.
                        Company name is {row['Company']}.
                    """.strip()
            report = Report(
                mdate=datetime.strptime(row["Date"], "%m/%d/%Y").date(),
                lead_owner=row["Lead Owner"],
                source=row["Source"],
                deal_stage=row["Deal Stage"],
                account_id=row["Account Id"],
                first_name=row["First Name"],
                last_name=row["Last Name"],
                company=row["Company"],
                content=content,
            )
            reports.append(report)

        await ReportRepository.bulk_insert(db, reports)

    @staticmethod
    async def list_reports(
        db: AsyncSession,
    ):
        return await ReportRepository.list_reports(db)

    @staticmethod
    async def reports_pagination(
        db: AsyncSession,
        page: int,
        page_size: int,
        query: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):
        stmt = select(Report)

        if query:
            stmt = stmt.where(Report.source.ilike(f"%{query}%"))

        column = getattr(Report, sort_by, Report.created_at)
        stmt = stmt.order_by(column.desc() if sort_order == "desc" else column.asc())

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(total_stmt)).scalar()

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        items = (await db.execute(stmt)).scalars().all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }

    @staticmethod
    async def update_partial(
        db: AsyncSession,
        report_id: str,
        payload: dict,
    ):
        # allow only real columns (security)
        allowed_fields = {
            "first_name",
            "last_name",
            "company",
            "lead_owner",
            "source",
            "deal_stage",
            "account_id",
        }

        update_data = {k: v for k, v in payload.items() if k in allowed_fields}

        if not update_data:
            return {"updated": False, "reason": "no valid fields"}

        stmt = (
            update(Report)
            .where(Report.id == report_id)
            .values(**update_data)
            .returning(Report)
        )

        result = await db.execute(stmt)
        await db.commit()

        updated = result.scalar_one_or_none()

        if not updated:
            return {"updated": False, "reason": "not found"}

        return {
            "updated": True,
            "id": updated.id,
            "fields": update_data,
        }

    @staticmethod
    async def create(db: AsyncSession, payload: dict):
        if payload.get("mdate"):
            payload["mdate"] = datetime.fromisoformat(payload["mdate"])
        report = Report(**payload)
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def list_filtered_reports(
        db: AsyncSession,
        page: int,
        page_size: int,
        sort_by: str | None,
        sort_order: str | None,
        source: str | None,
        deal_stage: str | None,
        lead_owner: str | None,
        first_name: str | None = None,
        last_name: str | None = None,
        company: str | None = None,
    ):
        stmt = select(Report).where(Report.is_deleted.is_(False))

        if source:
            stmt = stmt.where(Report.source.ilike(f"{source}%"))

        if deal_stage:
            stmt = stmt.where(Report.deal_stage.ilike(f"{deal_stage}%"))

        if lead_owner:
            stmt = stmt.where(Report.lead_owner.ilike(f"{lead_owner}%"))

        if first_name:
            stmt = stmt.where(Report.first_name.ilike(f"{first_name}%"))

        if last_name:
            stmt = stmt.where(Report.last_name.ilike(f"{last_name}%"))

        if company:
            stmt = stmt.where(Report.company.ilike(f"{company}%"))


        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await db.execute(count_stmt)
        total_items = total_result.scalar() or 0
        total_pages = (total_items + page_size - 1) // page_size  # ceil division

        if sort_by:
            col = getattr(Report, sort_by, None)
            if col is not None:
                stmt = stmt.order_by(col.desc() if sort_order == "desc" else col.asc())

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await db.execute(stmt)
        items = result.scalars().all()

        return {
            "items": items,
            "page": page,
            "total_pages": total_pages,
            "page_size": page_size,
            "total_items": total_items,
        }
