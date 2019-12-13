import csv
from app import db
from app.pipeline.models import CandidateStage
from app.pipeline.pipeline_stage import PipelineStage
import datetime
from sqlalchemy import func


class CsvFields:
    """
    Contains header values recognized by importing functions.
    """
    TIME = 'time'
    APPLICANT_ID = 'applicant_id'
    STAGE = 'stage'


def upload_data(source_file_name):
    """
    Uploads data from given csv file to the database.

    Args:
        source_file_name (str): Path to csv file.
    """
    with open(source_file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        db_rows = [row_to_candidate_stage(r) for r in csv_reader]
        for db_row in db_rows:
            db.session.merge(db_row)
        db.session.commit()


def row_to_candidate_stage(row):
    """
    Converts single csv row to CandidateStage model object.
    """
    try:
        return CandidateStage(
            time=datetime.datetime.utcfromtimestamp(int(row[CsvFields.TIME])),
            applicant_id=int(row[CsvFields.APPLICANT_ID]),
            stage=PipelineStage.from_str(row[CsvFields.STAGE])
        )
    except (ValueError, OSError) as err:
        raise InvalidRowError(f"Got error parsing a row: {err}", row)


class InvalidRowError(Exception):
    """
    Custom exception to show what's wrong with a csv row.

    Attributes:
        message (str): Error message.
    """
    def __init__(self, message, row):
        """
        Args:
            message (str): Base for error message.
            row (dict): Dictionary representing faulty csv row.
        """
        self.message = f"{message}, faulty row: time={row[CsvFields.TIME]}, " + \
                       f"applicant_id={row[CsvFields.APPLICANT_ID]}, stage={row[CsvFields.STAGE]}"
        super().__init__(self.message)


def get_last_timestamp_and_no_rows():
    """
    Returns last CandidateStage time present in the database and total number of rows.

    Returns:
        (datetime, int)
    """
    last_timestamp = db.session.query(func.max(CandidateStage.time)).scalar()
    no_rows = db.session.query(CandidateStage).count()
    return last_timestamp, no_rows
