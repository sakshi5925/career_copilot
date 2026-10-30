from sqlalchemy.orm import Session

from app.resume.chunk_model import ResumeChunk


class ResumeChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, chunks: list[ResumeChunk]):
        self.db.add_all(chunks)
        self.db.commit()

        for chunk in chunks:
            self.db.refresh(chunk)

        return chunks


    def delete_by_version_id(self, resume_version_id: int):
        self.db.query(ResumeChunk).filter(
            ResumeChunk.resume_version_id == resume_version_id
        ).delete()

        self.db.commit()

    def get_all_by_version_id(self, resume_version_id: int):
        return (
            self.db.query(ResumeChunk)
            .filter(
                ResumeChunk.resume_version_id == resume_version_id
            )
            .order_by(ResumeChunk.chunk_index.asc())
            .all()
        )

    def search_similar(
        self,
        resume_version_id: int,
        query_embedding: list[float],
        limit: int = 5
    ):
        return (
            self.db.query(ResumeChunk)
            .filter(
                ResumeChunk.resume_version_id == resume_version_id
            )
            .order_by(
                ResumeChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
            .all()
        )

    