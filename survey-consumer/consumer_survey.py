from os import environ
from os.path import basename
import json

#import pandas as pd
#import pyodbc
import urllib
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

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
    pw = environ.get('SQL_PASSWORD', 'HelloWorld!')
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

    surveys = session\
                .query(Survey) \
                .filter(\
                    Survey.STATUS_CODE.in_(['N', 'C']))\
                .all()

    print(surveys)


    #survey_tmp = session.query(Survey).first()
    #session.query(SurveyReport).filter(SurveyReport.survey == survey_tmp).all()

    # for s in surveys:
    #     print(f"{s.ID}, {s.API}, {s.STATUS_CODE}, {s.stations}")

    # Pandas
    # survey_qry = """
    #     SELECT  s.ID AS [SurveyID]
    #             , s.API
    #             , s.WKID
    #             , s.FIPS
    #             , s.STATUS_CODE
    #             , sr.Azimuth
    #             , sr.MD
    #             , sr.Inclination
    #             , sr.STATUS_CODE AS [SR_STATUS]
    #     FROM    dbo.DirectionalSurvey AS s WITH (READUNCOMMITTED)
    #         INNER JOIN dbo.SurveyReport AS sr WITH (READUNCOMMITTED)
    #             ON s.ID = sr.DirectionalSurveyId;
    # """
    # surveys = pd.read_sql(sql=survey_qry, con=sql_engine)
    # parsed = json.loads(surveys.to_json(orient='records'))
    # print(json.dumps(parsed, indent=4))

    # Direct SQL
    # with pyodbc.connect(con_str, autocommit=False) as con:
    #     cursor = con.cursor()
    #
    #     survey_qry = """
    #         SELECT  ID
    #                 , API
    #                 , WKID
    #                 , FIPS
    #                 , STATUS_CODE
    #         FROM    dbo.DirectionalSurvey WITH (READUNCOMMITTED);
    #     """
    #
    #     for row in cursor.execute(survey_qry):
    #         log.info(f"{row.ID}")



if __name__ == "__main__":
    main()
