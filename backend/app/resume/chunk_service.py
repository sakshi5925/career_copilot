import re

from app.resume.chunk_model import ResumeChunk
from app.resume.chunk_repository import ResumeChunkRepository
from app.resume.version_repository import ResumeVersionRepository
from app.embeddings.service import EmbeddingService
from app.ai.service import AIService



class ResumeChunkService:

    def __init__(
        self,
        chunk_repository: ResumeChunkRepository,
        version_repository: ResumeVersionRepository,
        embedding_service: EmbeddingService,
        ai_service: AIService
    ):
        self.chunk_repository = chunk_repository
        self.version_repository = version_repository
        self.embedding_service = embedding_service
        self.ai_service = ai_service

    def create_chunks_for_version(
        self,
        resume_version_id: int,
        user_id: int
    ):

        # Get resume version
        version = self.version_repository.get_by_id_for_user(
            resume_version_id,
            user_id
        )

        if version is None:
            raise ValueError("Resume version not found")

        # Delete previously generated chunks
        self.chunk_repository.delete_by_version_id(resume_version_id)

        # Split resume into meaningful chunks
        sections = self._split_into_sections(version.raw_text)

        chunks = []

        for index, section in enumerate(sections):

            content = section["content"]

            embedding = self.embedding_service.generate_embedding(content)

            chunk = ResumeChunk(
                resume_version_id=resume_version_id,
                chunk_index=index,
                content=section["content"],
                chunk_metadata={
                    "section": section["section"],
                    "subsection": section["subsection"],
                    "chunk_type": section["chunk_type"],
                },
                embedding=embedding

            )

            chunks.append(chunk)

        return self.chunk_repository.create_many(chunks)

    def _split_into_sections(self, text: str):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        sections = []

        current_section = None
        current_subsection = None
        current_content = []

        section_headers = {
            "professional summary",
            "summary",
            "profile",
            "objective",
            "career objective",
            "education",
            "experience",
            "projects",
            "achievements",
            "technical skills",
            "skills",
        }

        def save_current_chunk():

            if not current_content:
                return

            content = "\n".join(current_content).strip()

            if not content:
                return

            sections.append({
                "section": current_section or "Other",
                "subsection": current_subsection,
                "chunk_type": self._get_chunk_type(current_section),
                "content": content,
            })

        for line in lines:

            normalized = re.sub(r"\s+", " ", line.lower()).strip()

            # --------------------------------
            # Major section heading
            # --------------------------------

            if normalized in section_headers:

                # Save the previous chunk before
                # starting a new major section.
                save_current_chunk()

                # The section heading itself is metadata,
                # so we don't put it inside the content.
                current_section = line
                current_subsection = None
                current_content = []

                continue

            # --------------------------------
            # Experience
            # --------------------------------

            if self._is_experience_entry(line, current_section):

                save_current_chunk()

                current_subsection = line
                current_content = [line]

                continue

            # --------------------------------
            # Project
            # --------------------------------

            if self._is_project_heading(line, current_section):

                save_current_chunk()

                current_subsection = line
                current_content = [line]

                continue

            # --------------------------------
            # Normal content
            # --------------------------------

            current_content.append(line)

        # Save final chunk
        save_current_chunk()

        return sections

    def _is_experience_entry(
        self,
        line: str,
        current_section: str | None
    ) -> bool:

        if current_section is None:
            return False

        if current_section.lower() != "experience":
            return False

        # Normalize different dash characters that PDFs
        # may produce.
        normalized_line = (
            line
            .replace("–", "-")
            .replace("—", "-")
            .replace("−", "-")
        )

        months = (
            "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
        )

        pattern = (
            rf"(?:{months})\s+(?:19|20)\d{{2}}"
            rf"\s*-\s*"
            rf"(?:{months})\s+(?:19|20)\d{{2}}"
        )

        return bool(re.search(pattern, normalized_line))

    def _is_project_heading(
        self,
        line: str,
        current_section: str | None
    ) -> bool:

        if current_section is None:
            return False

        if current_section.lower() != "projects":
            return False

        # Project headings contain "|"
        # between project name and technologies.
        return "|" in line

    def _get_chunk_type(
        self,
        section: str | None
    ) -> str:

        if section is None:
            return "other"

        section_lower = section.lower()

        if section_lower in {
            "professional summary",
            "summary",
            "profile",
            "objective",
            "career objective",
        }:
            return "summary"

        if section_lower == "education":
            return "education"

        if section_lower == "experience":
            return "experience"

        if section_lower == "projects":
            return "project"

        if section_lower == "achievements":
            return "achievement"

        if section_lower in {"technical skills", "skills"}:
            return "skills"

        return "other"

    def search_similar_chunks(
        self,
        resume_version_id: int,
        user_id: int,
        query: str,
        limit: int = 5
    ):
        query_embedding = self.embedding_service.generate_embedding(query)

        return self.chunk_repository.search_similar(
            resume_version_id=resume_version_id,
            query_embedding=query_embedding,
            limit=limit
        )

    
    def answer_question(
        self,
        resume_version_id: int,
        user_id: int,
        question: str,
        limit: int = 5,
        conversation_history: list[dict[str, str]] | None = None
    ):
        version = self.version_repository.get_by_id_for_user(
            resume_version_id,
            user_id
        )

        if version is None:
            raise ValueError("Resume version not found")

        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        chunks = self.chunk_repository.search_similar(
            resume_version_id=resume_version_id,
            query_embedding=query_embedding,
            limit=limit
        )

        if not chunks:
            return {
                "answer": "I couldn't find relevant information in the resume. Please try rephrasing your question."
               
            }

        print("Question:", question)
        print("Retrieved chunks:", len(chunks))

        for chunk in chunks:
            print("Chunk:", chunk.chunk_index)
            print("Content:", chunk.content)
            print("Metadata:", chunk.chunk_metadata)

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        answer = self.ai_service.generate_resume_answer(
            question=question,
            context=context,
            conversation_history=conversation_history
        )

        return {
            "answer": answer
            
        }
    


    def search_similar_chunks(
        self,
        resume_version_id: int,
        user_id: int,
        query: str,
        limit: int = 5
    ):

        version = self.version_repository.get_by_id_for_user(
            resume_version_id,
            user_id
        )
        if version is None:
            raise ValueError("Resume version not found")

        query_embedding = self.embedding_service.generate_embedding(query)

        chunks = self.chunk_repository.search_similar(
            resume_version_id=resume_version_id,
            query_embedding=query_embedding,
            limit=limit
        )

        print("Query:", query)
        print("Resume version:", resume_version_id)
        print("Retrieved chunks:", len(chunks))

        for chunk in chunks:
            print("Chunk:", chunk.chunk_index)
            print("Content:", chunk.content[:300])
            print("---")

        return chunks