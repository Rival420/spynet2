from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    ip = Column(String, unique=True, nullable=False)
    ports = relationship("Port", back_populates="host")

class Port(Base):
    __tablename__ = 'ports'
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    host_id = Column(Integer, ForeignKey('hosts.id'), nullable=False)
    host = relationship("Host", back_populates="ports")
