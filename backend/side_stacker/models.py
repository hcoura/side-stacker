from sqlalchemy import Column, String, UUID

from .database import Base


class SideStackerGame(Base):
    """
    A very simple table to store the serialized board the winner (if any) 
    and the final state of the game
    """
    __tablename__ = "sidestacker_games"

    id = Column(String, primary_key=True, index=True)
    # TODO: choices
    winner = Column(String)
    state = Column(String)
    board = Column(String)
