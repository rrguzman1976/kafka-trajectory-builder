from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import ModelSchema

Base = declarative_base()


class DirectionalSurvey(Base):
    """
    Bean representing a Directional Survey. 1 API can have many surveys.
    """
    __tablename__ = 'DirectionalSurvey'

    SurveyId = Column(Integer, autoincrement=False, primary_key=True)
    API = Column(String(32), nullable=True)
    WKID = Column(String(32), nullable=True)
    FIPSCode = Column(String(4), nullable=True)
    StatusCode = Column(String(1), nullable=False)
    Created = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Survey(ID={self.SurveyId}, API={self.API}, Points={self.Stations})"


class SurveyReport(Base):
    """
    Bean representing a Survey Report. 1 survey can have many reports.
    """
    __tablename__ = 'SurveyReport'

    SurveyReportID = Column(Integer, autoincrement=False, primary_key=True)
    DirectionalSurveyId = Column(Integer, ForeignKey('DirectionalSurvey.SurveyId'), nullable=False)
    Azimuth = Column(Float, nullable=True)
    MD = Column(Float, nullable=True)
    TVD = Column(Float, nullable=True)
    Inclination = Column(Float, nullable=True)
    StatusCode = Column(String(1), nullable=False)
    Created = Column(DateTime, nullable=False)

    Survey = relationship(DirectionalSurvey, backref=backref('Stations', uselist=True))

    def __repr__(self):
        return f"Report(ID={self.SurveyReportID}, STATUS={self.StatusCode})"


class SurveySchema(ModelSchema):
    """
    Schema for Survey JSON serialization.
    """
    class Meta:
        unknown = EXCLUDE
        ordered = True
        model = DirectionalSurvey

    # Overrides
    Stations = fields.Nested("SurveyReportSchema", many=True, exclude=("Survey",))


class SurveyReportSchema(ModelSchema):
    """
    Schema for Survey Report JSON serialization.
    """
    class Meta:
        unknown = EXCLUDE
        ordered = True
        model = SurveyReport

    Survey = fields.Nested(SurveySchema, many=False, exclude=("Stations",))


# Set ORM tables to local vars so that full SQL metadata is available.
# surveys = Survey.__table__
# reports = SurveyReport.__table__

# Set schema tables to local vars.
survey_serdes = SurveySchema()
report_serdes = SurveyReportSchema()