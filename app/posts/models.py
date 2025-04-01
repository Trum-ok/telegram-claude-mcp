from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sa_base import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # metadata: Mapped = mapped_column()
    # conversation_id = Column(Integer, ForeignKey("conversations.id"))
    # role = Column(String)  # "user", "assistant", "system"
    # content = Column(Text)
    # created_at = Column(DateTime, default=datetime.utcnow)
    # metadata = Column(Text, nullable=True)  # JSON string for any additional metadata

    # conversation = relationship("Conversation", back_populates="messages")
