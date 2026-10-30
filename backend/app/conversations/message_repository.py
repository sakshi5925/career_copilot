
from sqlalchemy.orm import Session

from app.conversations.message_model import ConversationMessage


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, message: ConversationMessage):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_id(self, message_id: int):
        return (
            self.db.query(ConversationMessage)
            .filter(ConversationMessage.id == message_id)
            .first()
        )

    def get_all_by_conversation_id(
        self,
        conversation_id: int,
        limit: int = 50
    ):
        messages = (
            self.db.query(ConversationMessage)
            .filter(
                ConversationMessage.conversation_id == conversation_id
            )
            .order_by(
                ConversationMessage.created_at.desc(),
                ConversationMessage.id.desc()
            )
            .limit(limit)
            .all()
        )

        return list(reversed(messages))

    def delete(self, message: ConversationMessage):
        self.db.delete(message)
        self.db.commit()