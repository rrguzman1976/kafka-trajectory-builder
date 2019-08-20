from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Survey(Base):
    __tablename__ = 'DirectionalSurvey'

    ID = Column(Integer, autoincrement=False, primary_key=True)
    API = Column(String(32), nullable=True)
    WKID = Column(String(32), nullable=True)
    FIPS = Column(String(4), nullable=True)
    STATUS_CODE = Column(String(1), nullable=False)

    # def __repr__(self):
    #     return f"{self.ID}"

class SurveyReport(Base):
    __tablename__ = 'SurveyReport'

    ID = Column(Integer, autoincrement=False, primary_key=True)
    DirectionalSurveyId = Column(Integer, ForeignKey('DirectionalSurvey.ID'), nullable=False)
    Azimuth = Column(Float, nullable=True)
    MD = Column(Float, nullable=True)
    Inclination = Column(Float, nullable=True)
    STATUS_CODE = Column(String(1), nullable=False)
    survey = relationship(Survey, backref=backref('stations', uselist=True))