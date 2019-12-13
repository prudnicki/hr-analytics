from datetime import datetime

from app.pipeline.pipeline_stage import PipelineStage
from app.pipeline.uploads import row_to_candidate_stage, CsvFields, InvalidRowError

from pytest import raises


def test_row_to_candidate_stage():
    row = {CsvFields.TIME: 1404851070, CsvFields.STAGE: 'HIRED', CsvFields.APPLICANT_ID: 12}

    cs = row_to_candidate_stage(row)

    assert cs.applicant_id == 12
    assert cs.time == datetime(year=2014, month=7, day=8, hour=20, minute=24, second=30)
    assert cs.stage == PipelineStage.HIRED


def test_row_to_candidate_stage_invalid_stage():
    with raises(InvalidRowError) as err:
        row = {CsvFields.TIME: 1404851070, CsvFields.STAGE: 'FAKE_LABEL', CsvFields.APPLICANT_ID: 12}

        cs = row_to_candidate_stage(row)

        assert "applicant_id=12" in err.message
        assert "Unknown label for PipelineStage" in err.message


def test_row_to_candidate_stage_invalid_applicant_id():
    with raises(InvalidRowError) as err:
        row = {CsvFields.TIME: 1404851070, CsvFields.STAGE: 'FAKE_LABEL', CsvFields.APPLICANT_ID: '12fgh'}

        cs = row_to_candidate_stage(row)

        assert "applicant_id=12fgh" in err.message


def test_row_to_candidate_stage_invalid_time():
    with raises(InvalidRowError) as err:
        row = {CsvFields.TIME: '14048asda51070', CsvFields.STAGE: 'FAKE_LABEL', CsvFields.APPLICANT_ID: 12}

        cs = row_to_candidate_stage(row)

        assert "time=14048asda51070" in err.message
