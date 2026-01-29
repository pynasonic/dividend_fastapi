from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.openai_embedder import embed_fn
from app.db.models.m_div import Div, DivChunk
from app.db.repo.repo_div_embedding import DivEmbeddingRepository


class EmbeddingService:

    @staticmethod   
    async def embed_all_dummy(
        db: AsyncSession,
    ) -> int:
        rows = await DivEmbeddingRepository.get_all_unembedded(db)

        for r in rows:
            text = r.content  # or combine EN + FR if you want
            emb = await embed_fn(text)
            await DivEmbeddingRepository.update_embedding(db, r.id, emb)

        await db.commit()
        return len(rows)