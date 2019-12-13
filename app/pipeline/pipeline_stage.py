from enum import Enum


class PipelineStage(Enum):
    """
    Represents all candidate stages possible in job pipeline.
    """
    APPLIED = "applied"
    SCREENED = "screened"
    REJECTED_1 = "rejected_1"
    INTERVIEWED = "interviewed"
    REJECTED_2 = "rejected_2"
    GIVEN_OFFER = "given_offer"
    DECLINED = "declined"
    HIRED = "hired"

    def __init__(self, status_name):
        self.status_name = status_name

    @staticmethod
    def from_str(label):
        """
        Constructs PipelineStage object from label string.

        Args:
            label (str): label corresponding to one of PipelineStageobjects.

        Returns:
            PipelineStatus: PipelineStage object corresponding to passed label.

        Raises:
            ValueError: In case label doesn't correspond to any PipelineStage.
        """
        label_lower = label.lower()
        if label_lower == PipelineStage.APPLIED.status_name:
            return PipelineStage.APPLIED
        elif label_lower == PipelineStage.SCREENED.status_name:
            return PipelineStage.SCREENED
        elif label_lower == PipelineStage.REJECTED_1.status_name:
            return PipelineStage.REJECTED_1
        elif label_lower == PipelineStage.INTERVIEWED.status_name:
            return PipelineStage.INTERVIEWED
        elif label_lower == PipelineStage.REJECTED_2.status_name:
            return PipelineStage.REJECTED_2
        elif label_lower == PipelineStage.GIVEN_OFFER.status_name:
            return PipelineStage.GIVEN_OFFER
        elif label_lower == PipelineStage.DECLINED.status_name:
            return PipelineStage.DECLINED
        elif label_lower == PipelineStage.HIRED.status_name:
            return PipelineStage.HIRED
        else:
            raise ValueError(f"Unknown label for PipelineStage: {label}")


SORT_ORDER = {
    PipelineStage.APPLIED: 1,
    PipelineStage.SCREENED: 2,
    PipelineStage.REJECTED_1: 3,
    PipelineStage.INTERVIEWED: 4,
    PipelineStage.REJECTED_2: 5,
    PipelineStage.GIVEN_OFFER: 6,
    PipelineStage.DECLINED: 7,
    PipelineStage.HIRED: 8
}
"""
Custom sort order for enum elements - we want to display stages according to how far a candidate got.
"""

DISPLAY_NAMES = {
    PipelineStage.APPLIED: "Applied",
    PipelineStage.SCREENED: "Screened",
    PipelineStage.REJECTED_1: "Rejected after screening",
    PipelineStage.INTERVIEWED: "Interviewed",
    PipelineStage.REJECTED_2: "Rejected after interview",
    PipelineStage.GIVEN_OFFER: "Given offer",
    PipelineStage.DECLINED: "Declined",
    PipelineStage.HIRED: "Hired"
}
"""
'Pretty' display values for enum elements.
"""
