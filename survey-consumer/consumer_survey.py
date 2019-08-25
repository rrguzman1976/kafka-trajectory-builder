import urllib
from os import environ
from os.path import basename
import json

import pandas as pd
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from marshmallow import pprint
from confluent_kafka import Producer

from survey_consumer.log_factory import config
from survey_consumer.orm.SurveySchema import Base, DirectionalSurvey, SurveyReport
from survey_consumer.orm.SurveySchema import survey_serdes
from survey_consumer.kafka import util

config.init_logger()
log = config.return_logger(basename(__file__))

def main():
    """
    Simple producer implementation based on:
    https://github.com/confluentinc/confluent-kafka-python
    """

    # Get all new surveys (list of Survey objects)
    new_surveys = session.query(DirectionalSurvey)\
                    .join(SurveyReport)\
                    .filter(DirectionalSurvey.StatusCode.in_(['N', 'C']))\
                    .filter(SurveyReport.StatusCode.notin_(['E']))\
                    .all()

    log.debug(f"Collected surveys: {new_surveys}")

    p = Producer({
        'bootstrap.servers': kafka,
    })

    try:
        for s in new_surveys:
            s_dict = survey_serdes.dump(s)
            s_json = json.dumps(s_dict)

            p.poll(0)

            p.produce(topic=topic, value=s_json.encode('utf-8')
                      , key=str(s.SurveyId).encode('utf-8')
                      , on_delivery=util.delivery_handler)

        p.flush()

        # TODO: Use ORM to set status to 'P'

    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":

    driver = environ.get('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')
    host = environ.get('SQL_HOST', 'localhost')
    db = environ.get('SQL_DB', 'ScratchDB')
    user = environ.get('SQL_USER', 'sa')
    pw = environ.get('SQL_PASSWORD', 'HelloWorld1')

    kafka = environ.get('KAFKA_BOOTSTRAP', 'localhost:9092')
    topic = environ.get('ACQ_TOPIC', 'survey-acq')

    con_str = f'DRIVER={driver};SERVER={host};DATABASE={db};UID={user};PWD={pw}'

    params = urllib.parse.quote_plus(con_str)
    sql_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}"
                               , echo=True)

    log.info(f"Connecting to {host}.{db}...")

    # Bind the engine to the metadata of the Base class so that the
    # beans can be accessed through a DBSession instance
    Base.metadata.bind = sql_engine
    DBSession = sessionmaker(bind=sql_engine)
    session = DBSession()

    main()
