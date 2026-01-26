# app/repositories/wage_embedding_repository.py
# app/repositories/wage_embedding_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict
from app.db.models.m_wage import CanadaWage
from app.db.models.m_wage_embedding import CanadaWageEmbedding


class WageEmbeddingRepository:
    @staticmethod
    async def build_chunks(db: AsyncSession) -> List[Dict]:
        """
        Read all CanadaWage rows, combine English and French fields
        into separate chunks for embedding.
        Returns a list of dicts:
        {source_id, chunk_en, chunk_fr}
        """
        result = await db.execute(select(CanadaWage))
        # type: ignore[return-value]
        rows: List[CanadaWage] = result.scalars().all()

        chunks = []

        for row in rows:
            chunk_en = f"""
Region: {row.er_name}
Province: {row.prov}
NOC: {row.noc_cnp}
Title: {row.noc_title_eng}
Median wage: {row.median_wage_salaire_median}
Average wage: {row.average_wage_salaire_moyen}
Low wage: {row.low_wage_salaire_minimum}
High wage: {row.high_wage_salaire_maximal}
Quartile1 wage: {row.quartile1_wage_salaire_quartile1}
Quartile3 wage: {row.quartile3_wage_salaire_quartile3}
Reference year: {row.reference_period}
Annual flag: {row.annual_wage_flag_salaire_annuel}
Source: {row.data_source_e}
Notes: {row.wage_comment_e}
Employees with benefits (%): {row.employeeswithnonwagebenefit_pct}
""".strip()

            chunk_fr = f"""
Région: {row.nom_re}
Province: {row.prov}
NOC: {row.noc_cnp}
Titre: {row.noc_title_fra}
Salaire médian: {row.median_wage_salaire_median}
Salaire moyen: {row.average_wage_salaire_moyen}
Salaire minimum: {row.low_wage_salaire_minimum}
Salaire maximum: {row.high_wage_salaire_maximal}
1er quartile: {row.quartile1_wage_salaire_quartile1}
3e quartile: {row.quartile3_wage_salaire_quartile3}
Année de référence: {row.reference_period}
Flag annuel: {row.annual_wage_flag_salaire_annuel}
Source: {row.data_source_f}
Notes: {row.wage_comment_f}
Employés avec avantages (%): {row.employeeswithnonwagebenefit_pct}
""".strip()

            chunks.append(
                {"source_id": row.id, "chunk_en": chunk_en, "chunk_fr": chunk_fr}
            )

        return chunks

    @staticmethod
    async def bulk_insert_embeddings(
        db: AsyncSession,
        embeddings: List[Dict],
    ) -> None:
        """
        embeddings: list of dicts with keys: source_id, chunk, embedding (list[float])
        """
        # use raw insert for pgvector
        values = [
            {
                "source_id": e["source_id"],
                "chunk_en": e["chunk_en"],
                "chunk_fr": e["chunk_fr"],
                "embedding": e["embedding"],  # as float[]
            }
            for e in embeddings
        ]

        # raw insert example using SQLAlchemy Core
        from app.db.models.m_wage_embedding import CanadaWageEmbedding

        db.add_all([CanadaWageEmbedding(**v) for v in values])
        await db.commit()

    @staticmethod
    async def get_all_unembedded(db: AsyncSession):
        stmt = select(CanadaWageEmbedding).where(
            CanadaWageEmbedding.embedding == [0.0] * 384
        )
        stmt = stmt.limit(500)  # process in batches of 100
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def update_embedding(
        db: AsyncSession,
        row_id,
        embedding: list[float],
    ):
        row = await db.get(CanadaWageEmbedding, row_id)
        row.embedding = embedding    # type: ignore
        db.add(row)
