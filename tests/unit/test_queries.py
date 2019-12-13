from app.pipeline.queries import format_results
from app.pipeline.pipeline_stage import PipelineStage, DISPLAY_NAMES


def test_format_results():
    data = [
        {'stage': PipelineStage.HIRED, 'candidate_count': 3, 'conversion_ratio': 0.30},
        {'stage': PipelineStage.REJECTED_2, 'candidate_count': 2, 'conversion_ratio': 0.20},
        {'stage': PipelineStage.GIVEN_OFFER, 'candidate_count': 1, 'conversion_ratio': 0.10}
    ]

    results = format_results(data)

    assert len(results) == 3
    assert results[0] == {'stage': DISPLAY_NAMES[PipelineStage.REJECTED_2], 'candidate_count': 2,
                          'conversion_ratio': 0.20}
    assert results[1] == {'stage': DISPLAY_NAMES[PipelineStage.GIVEN_OFFER], 'candidate_count': 1,
                          'conversion_ratio': 0.10}
    assert results[2] == {'stage': DISPLAY_NAMES[PipelineStage.HIRED], 'candidate_count': 3,
                          'conversion_ratio': 0.30}


def test_format_results_empty():
    data = []

    results = format_results(data)

    assert len(results) == 0
