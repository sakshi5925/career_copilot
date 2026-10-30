
from app.conversations.model import Conversation
from app.conversations.message_model import ConversationMessage
from app.conversations.repository import ConversationRepository
from app.conversations.message_repository import MessageRepository
from app.resume.version_repository import ResumeVersionRepository
from app.resume.chunk_service import ResumeChunkService


class ConversationService:

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        version_repository: ResumeVersionRepository,
        resume_chunk_service: ResumeChunkService
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.version_repository = version_repository
        self.resume_chunk_service = resume_chunk_service
    def create_conversation(self, user_id: int, title: str = "New conversation", resume_version_id: int | None = None):

        if resume_version_id is not None:
            version = self.version_repository.get_by_id_for_user(
                resume_version_id,
                user_id
            )

            if version is None:
                raise ValueError("Resume version not found")
        
        conversation = Conversation(
            user_id=user_id,
            title=title,
            resume_version_id=resume_version_id
        )
        return self.conversation_repository.create(conversation)

    def get_user_conversations(self, user_id: int):
        return self.conversation_repository.get_all_by_user_id(user_id)

    def get_conversation_messages(
        self,
        conversation_id: int,
        user_id: int
    ):
        conversation = self.conversation_repository.get_by_id(
            conversation_id
        )

        if conversation is None or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        return self.message_repository.get_all_by_conversation_id(
            conversation_id
        )

    def delete_conversation(
        self,
        conversation_id: int,
        user_id: int
    ):
        conversation = self.conversation_repository.get_by_id(
            conversation_id
        )

        if conversation is None or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        self.conversation_repository.delete(conversation)
    

    def add_message(
        self,
        conversation_id: int,
        user_id:int,
        content :str
    ):
        conversation=self.conversation_repository.get_by_id(conversation_id)
        if conversation is None or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        message= ConversationMessage(
            conversation_id=conversation_id,
            role="user",
            content=content
        )

        saved_message = self.message_repository.create(message)

        self.conversation_repository.update(conversation)

        return saved_message
    

    def chat(
        self,
        conversation_id:int,
        user_id:int,
        question: str
    ):
        conversation=self.conversation_repository.get_by_id(
            conversation_id
        )
        if conversation is None or conversation.user_id != user_id:
            raise ValueError("Conversation not found")

        if conversation.resume_version_id is None:
            raise ValueError("This conversation has no linked resume version")

        
        previous_messages = self.message_repository.get_all_by_conversation_id(
            conversation_id,
            limit=10
        )

        conversation_history = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in previous_messages
            if message.role in ("user", "assistant")
        ]



        user_message=ConversationMessage(
            conversation_id=conversation_id,
            role="user",
            content=question
        )

        saved_user_message = self.message_repository.create(user_message)

        try:
            result = self.resume_chunk_service.answer_question(
                resume_version_id=conversation.resume_version_id,
                user_id=user_id,
                question=question,
                limit=5,
                conversation_history=conversation_history
            )

        except Exception as e:
            self.message_repository.delete(saved_user_message)
            raise RuntimeError(
                "Unable to generate an answer right now. Please try again."
            ) from e



        assistant_message = ConversationMessage(
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"]
        )

        saved_assistant_message = self.message_repository.create(
            assistant_message
        )

        self.conversation_repository.update(conversation)

        return {
            "user_message": saved_user_message,
            "assistant_message": saved_assistant_message,
            "sources": result["sources"]
        }

    
