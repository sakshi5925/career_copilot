from sqlalchemy.orm import Session
from app.conversations.model import Conversation

class  ConversationRepository:

    def __init__(self, db:Session):
        self.db=db

    def create(self,conversation:Conversation):
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_id(self, conversation_id: int):

        return (
            self.db.query(Conversation)
            .filter(Conversation.id==conversation_id)
            .first()
        )


    def get_all_by_user_id(self,user_id:int):
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )
    
    def update(self, conversation: Conversation):
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete(self, conversation: Conversation):
        self.db.delete(conversation)
        self.db.commit()
        

        