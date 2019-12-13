from app import db
from app.pipeline.pipeline_stage import PipelineStage


class CandidateStage(db.Model):
    """
    Database representation of single candidate stage read from CSV file.
    """
    time = db.Column(db.DateTime, nullable=False)
    applicant_id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.Enum(PipelineStage), primary_key=True)

    def __repr__(self):
        return '<CandidateStage time: {}, applicant_id: {}, stage: {}>'.format(self.username, self.applicant_id,
                                                                               self.stage)
