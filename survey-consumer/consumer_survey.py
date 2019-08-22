from os import environ
from os.path import basename
import json

#import pandas as pd
#import pyodbc
import urllib
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, selectinload

from survey_consumer.log_factory import config
from survey_consumer.orm.SurveySchema import Base, Survey, SurveyReport

def main():
    """
    Entrypoint

    :return: None
    """

    config.init_logger()
    log = config.return_logger(basename(__file__))

    driver = environ.get('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')
    host = environ.get('SQL_HOST', 'localhost')
    db = environ.get('SQL_DB', 'ScratchDB')
    user = environ.get('SQL_USER', 'sa')
    pw = environ.get('SQL_PASSWORD', 'HelloWorld1')
    #pw = environ.get('SQL_PASSWORD', 'HelloWorld!')
    topic = environ.get('ACQ_TOPIC', 'dir-survey-01')
    con_str = f'DRIVER={driver};SERVER={host};DATABASE={db};UID={user};PWD={pw}'

    log.info(f"Connecting to {host}.{db}...")

    params = urllib.parse.quote_plus(con_str)
    sql_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}"
                               , echo=True) # echo's emitted sql

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = sql_engine
    DBSession = sessionmaker(bind=sql_engine)
    session = DBSession()

    # Get all new surveys
    surveys = session.query(Survey) \
                .options(selectinload(Survey.stations))\
                .filter(Survey.STATUS_CODE.in_(['N', 'C']))\
                .filter(Survey.stations.any())\
                .all()

    # Surveys is a list of Survey objects
    log.info(surveys)

if __name__ == "__main__":
    main()
