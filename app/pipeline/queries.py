from app import db
from app.pipeline.models import CandidateStage
from app.pipeline import pipeline_stage


def get_full_stats(start_date, end_date, stages=None):
    """
    Returns full statistics (count and conversion ratios for every stage) for given time period.
    Optionally takes a list of stages to further limit candidate pool to those who reached those stages in time period.

    Args:
        start_date (datetime): Lower bound of time period
        end_date (datetime): Upper bound of time period
        stages ([PipelineStage]): Optional list of PipelineStage to further limit candidate pool

    Returns:
        A dictionary in a format: {'stage': PipelineStage, 'candidate_count': int, 'conversion_ratio': float}
    """
    total_count = get_total_number_of_candidates(start_date, end_date, stages)
    candidates_by_stage = get_candidates_by_stage(start_date, end_date, stages)

    result = []
    for stage, candidate_count in candidates_by_stage:
        result.append({
            'stage': stage,
            'candidate_count': candidate_count,
            'conversion_ratio': round(candidate_count / float(total_count), 2)
        })
    return format_results(result)


def get_total_number_of_candidates(start_date, end_date, stages=None):
    """
    Returns total number of candidates for given time period.
    Optionally takes a list of stages to further limit candidate pool to those who reached those stages in time period.

    Args:
        start_date (datetime): Lower bound of time period
        end_date (datetime): Upper bound of time period
        stages ([PipelineStage]): Optional list of PipelineStage to further limit candidate pool

    Returns:
        int: Total number of candidates.
    """
    query = _get_time_and_stage_bound_query(start_date, end_date, stages)
    return query.distinct(CandidateStage.applicant_id).count()


def get_candidates_by_stage(start_date, end_date, stages=None):
    """
    Returns number of candidates that reached given stage for given time period.
    Optionally takes a list of stages to further limit candidate pool to those who reached those stages in time period.

    Args:
        start_date (datetime): Lower bound of time period
        end_date (datetime): Upper bound of time period
        stages ([PipelineStage]): Optional list of PipelineStage to further limit candidate pool

    Returns:
        SQLAlchemy query result: [(PipelineStage, candidate_count)]
    """
    # used to constrain applicants to those who were in given stage in given time period
    sq = _get_time_and_stage_bound_query(start_date, end_date, stages).distinct(
        CandidateStage.applicant_id).subquery()
    query = db.session \
        .query(CandidateStage.stage, db.func.count(CandidateStage.stage)) \
        .group_by(CandidateStage.stage) \
        .join(sq, CandidateStage.applicant_id == sq.c.applicant_id)
    return query.all()


def _get_time_and_stage_bound_query(start_date, end_date, stages):
    """
    Constructs a SQLAlchemy query returning all CandidateStage records in given time period and filtered by stage.
    """
    query = db.session.query(CandidateStage.applicant_id).filter(CandidateStage.time > start_date,
                                                                 CandidateStage.time < end_date)
    if stages:
        query = query.filter(CandidateStage.stage.in_(stages))
    return query


def format_results(results):
    """
    Formats analytics results for displaying on screen.
    Sorts results using custom PipelineStage ordering
    and translates PipelineStage enum elements to their 'pretty' display values.
    """
    sorted_results = sorted(results, key=lambda d: pipeline_stage.SORT_ORDER[d['stage']])
    displayable = [{'stage': pipeline_stage.DISPLAY_NAMES[item['stage']], 'candidate_count': item['candidate_count'],
                    'conversion_ratio': item['conversion_ratio']}
                   for item in sorted_results]
    return displayable
