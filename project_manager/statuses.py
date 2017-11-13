STATUS_UNAVAILABLE = 'un'
STATUS_AWAITING_WORK = 'aw'
STATUS_IN_PROGRESS = 'ip'
STATUS_AWAITING_VERIFICATION = 'av'
STATUS_DONE = 'do'
STATUS_STOPPED = 'st'
STATUS_FORBIDDEN = 'fb'
STATUS_ARCHIVED = 'ar'
STATUS_REACTIVATED = 're'

STATUS_LIST = (
    (STATUS_REACTIVATED, 'Реактивированно'),
    (STATUS_UNAVAILABLE, 'Недоступно'),
    (STATUS_AWAITING_WORK, 'Ожидает выполнения'),
    (STATUS_IN_PROGRESS, 'В работе'),
    (STATUS_AWAITING_VERIFICATION, 'Ожидает проверки'),
    (STATUS_DONE, 'Выполнено'),
    (STATUS_STOPPED, 'Приостановлено'),
    (STATUS_FORBIDDEN, 'Заброшено'),
    (STATUS_ARCHIVED, 'Архивированно'),
)
