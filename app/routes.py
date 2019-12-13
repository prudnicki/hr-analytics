from datetime import datetime
import os

from flask import render_template, flash, redirect, request

import config
from app import app
from app.pipeline.forms import UploadForm, AnalyticsForm
from app.pipeline.pipeline_stage import PipelineStage, DISPLAY_NAMES
from app.pipeline.queries import get_full_stats
from app.pipeline.uploads import upload_data, get_last_timestamp_and_no_rows, InvalidRowError


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AnalyticsForm()
    results = []
    description = ""
    if form.validate_on_submit():
        stages = [PipelineStage.from_str(str_stage) for str_stage in form.stages.data]
        results = get_full_stats(
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            stages=stages
        )
        description = create_description(form.start_date.data, form.end_date.data, stages)
    elif request.method == 'GET':
        results = get_full_stats(datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0),
                                 datetime(year=2100, month=1, day=1, hour=0, minute=0, second=0))
        description = "Showing statistics for all candidates"

    return render_template('index.html', results=results, form=form, description=description)


def create_description(start_date, end_date, stages):
    description = f"Showing statistics for candidates between {start_date.strftime(config.Config.DATETIME_FORMAT)}" + \
                  f" and {end_date.strftime(config.Config.DATETIME_FORMAT)}"
    if stages:
        description += f", who reached following stages during that time: {[DISPLAY_NAMES[st] for st in stages]}"
    return description


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        upload_dir = app.config.get('UPLOAD_PATH')
        if not os.path.isdir(upload_dir):
            os.mkdir(upload_dir)
        saved_filename = _get_new_filename(form.file.data.filename, datetime.utcnow())
        saved_file_path = os.path.join(upload_dir, saved_filename)
        form.file.data.save(saved_file_path)
        try:
            upload_data(saved_file_path)
            flash("New data has been uploaded")
        except InvalidRowError as err:
            flash(err.message, 'error')
        return redirect('/upload')
    last_time, no_rows = get_last_timestamp_and_no_rows()
    return render_template('upload.html', form=form, last_time=last_time, no_rows=no_rows)


def _get_new_filename(uploaded_filename, upload_time):
    """
    Creates a new filename for uploaded file by appending current datetime before the extensions.
    """
    dot_pos = uploaded_filename.rfind(".")
    formatted_time = upload_time.strftime("%d-%m-%Y-%H-%M-%S-%f")
    before_ext = uploaded_filename[0:dot_pos]
    ext = uploaded_filename[dot_pos + 1:len(uploaded_filename)]
    return f"{before_ext}-{formatted_time}.{ext}"
