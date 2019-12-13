from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateTimeField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from app.pipeline import pipeline_stage
import config


class UploadForm(FlaskForm):
    file = FileField(label='Candidate data file', validators=[DataRequired()])
    submit = SubmitField('Upload')


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class AnalyticsForm(FlaskForm):
    start_date = DateTimeField(id='start_date', format=config.Config.DATETIME_FORMAT, validators=[DataRequired()])
    end_date = DateTimeField(id='end_date', format=config.Config.DATETIME_FORMAT, validators=[DataRequired()])
    stages = MultiCheckboxField('stages', choices=[(k.status_name, v) for k, v in pipeline_stage.DISPLAY_NAMES.items()])
    submit = SubmitField('Show')
