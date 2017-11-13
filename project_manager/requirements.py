from .models import Project
from .tag_manager import get_by_tag

REQUIREMENT_WORK_FINISHED = 'work_finished'

REQUIREMENT_TYPES_LIST = (
    (REQUIREMENT_WORK_FINISHED, 'Таск завершён'),
)


def work_finished(project, tag):
    work = get_by_tag(project, tag)
    return work.is_finished()

def not_empty(project, tag):
    resource = get_by_tag(project, tag)
    return not resource.is_empty()

