# app/services/report_service.py
import csv
import io
from datetime import datetime
from app.db.models.m_wage import CanadaWage
from app.db.repo.repo_wage import WageRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update


class WageService:

    @staticmethod
    async def upload_csv(
        db: AsyncSession,
        file_bytes: bytes,
    ) -> None:
        text = file_bytes.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))

        reader.fieldnames = [h.strip().replace('\ufeff','') for h in reader.fieldnames]
        print("--------CSV Headers:", reader.fieldnames)
        
        wages: list[CanadaWage] = []
        
        for row in reader:
            # ---------- language-independent ----------
            shared_content = f"""
                NOC code: {row['NOC_CNP']}
                Province: {row['prov']}
                ER code: {row.get('ER_Code_Code_RE')}
                Reference period: {row.get('Reference_Period')}
                Low wage: {row.get('Low_Wage_Salaire_Minimum')}
                Median wage: {row.get('Median_Wage_Salaire_Median')}
                High wage: {row.get('High_Wage_Salaire_Maximal')}
                Average wage: {row.get('Average_Wage_Salaire_Moyen')}
                First quartile wage: {row.get('Quartile1_Wage_Salaire_Quartile1')}
                Third quartile wage: {row.get('Quartile3_Wage_Salaire_Quartile3')}
                Annual wage flag: {row.get('Annual_Wage_Flag_Salaire_annuel')}
                Non-wage benefit percentage: {row.get('EmployeesWithNonWageBenefit_Pct')}
            """.strip()

            # ---------- English ----------
            content_en = f"""
                Occupation title: {row['NOC_Title_eng']}
                Economic region: {row.get('ER_Name')}
                Data source: {row.get('Data_Source_E')}
                Wage comment: {row.get('Wage_Comment_E')}
                {shared_content}
            """.strip()

            # ---------- French ----------
            content_fr = f"""
                Titre de la profession: {row['NOC_Title_fra']}
                Région économique: {row.get('Nom_RE')}
                Source des données: {row.get('Data_Source_F')}
                Commentaire sur le salaire: {row.get('Wage_Comment_F')}
                {shared_content}
            """.strip()

            # ---------- Convert numeric / boolean fields ----------
            def to_int(val):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return None

            def to_float(val):
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return None

            def to_bool(val):
                if val is None:
                    return False
                return str(val).strip().lower() in ["true", "1", "yes"]

            wage = CanadaWage(
                noc_code=row["NOC_CNP"],
                noc_title_en=row["NOC_Title_eng"],
                noc_title_fr=row["NOC_Title_fra"],
                province=row["prov"],
                er_code=row.get("ER_Code_Code_RE"),
                er_name_en=row.get("ER_Name"),
                er_name_fr=row.get("Nom_RE"),
                low_wage=to_int(row.get("Low_Wage_Salaire_Minimum")),
                median_wage=to_int(row.get("Median_Wage_Salaire_Median")),
                high_wage=to_int(row.get("High_Wage_Salaire_Maximal")),
                average_wage=to_int(row.get("Average_Wage_Salaire_Moyen")),
                quartile1_wage=to_int(row.get("Quartile1_Wage_Salaire_Quartile1")),
                quartile3_wage=to_int(row.get("Quartile3_Wage_Salaire_Quartile3")),
                annual_wage_flag=to_bool(row.get("Annual_Wage_Flag_Salaire_annuel")),
                source_2025=row.get("Source2025_NHQ"),
                data_source_en=row.get("Data_Source_E"),
                data_source_fr=row.get("Data_Source_F"),
                reference_period=row.get("Reference_Period"),
                revision_date=(
                    datetime.strptime(row["Revision_Date_Date_revision"], "%Y-%m-%d").date()
                    if row.get("Revision_Date_Date_revision")
                    else None
                ),
                wage_comment_en=row.get("Wage_Comment_E"),
                wage_comment_fr=row.get("Wage_Comment_F"),
                non_wage_benefit_pct=to_float(row.get("EmployeesWithNonWageBenefit_Pct")),
                content_en=content_en,
                content_fr=content_fr,
            )

            wages.append(wage)

        await WageRepository.bulk_insert(db, wages)
        

    @staticmethod
    async def list_wages(
        db: AsyncSession,
    ):
        return await WageRepository.list_wages(db)

    @staticmethod
    async def list_paginated(
        db: AsyncSession,
        page: int,
        page_size: int,
    ):
        offset = max(page - 1, 0) * page_size

        stmt = (
            select(CanadaWage)
            .offset(offset)
            .limit(page_size + 1)
        )

        result = await db.execute(stmt)
        rows = result.scalars().all()

        has_next = len(rows) > page_size
        items = rows[:page_size]

        return {
            "items": items,
            "page": page,
            "has_prev": page > 1,
            "has_next": has_next,
        }