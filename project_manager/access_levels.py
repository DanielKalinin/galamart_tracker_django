from hel.user_roles import *

#Alarms
GET_NOTIFICATION_SELF_TASK = 'Уведомления свои таски'
GET_NOTIFICATION_SELF_PROJECT = 'Уведомления свой проект'
GET_NOTIFICATION_ANY_PROJECT = 'Уведомления любой проект'

#Project creation
CREATE_GALA_PROJECT = 'Создание базового проекта'
CREATE_FRANCH_PROJECT = 'Создание проекта франшизы'

#Change workflow
CHANGE_WORKFLOW = 'Изменение воркфлоу'

#Analytics
GET_ANALYTICS_SELF_PROJECT = 'Аналитика свой проект'
GET_ANALYTICS_ANY_PROJECT = 'Аналитика любой проект'

#Reactivate tasks
REACTIVATE_TASK_SELF_PROJECT = 'Реактивация таска свой проект'
REACTIVATE_TASK_ANY_PROJECT = 'Реактивация таска любой проект'

#Appoint roles
APPOINT_IN_PROJECT = 'Назначение юзера в проект'

#Delete user
DELETE_USER = 'Удaление юзеров'

#Artifacts
GET_ARTIFACTS_SELF_PROJECT = 'Артефакты свой проект'
GET_ARTIFACTS_ANY_PROJECT = 'Артефакты любой проект'

#See projects
SEE_SELF_PROJECT = 'Доступ свой проект'
SEE_ANY_PROJECT = 'Доступ любой проект'

#Tasks
FREE_CASH = 'Доступ к свободной кассе'

#Roles

KEY_PROJECT_ROLE = (
    GET_NOTIFICATION_SELF_PROJECT,
    GET_ANALYTICS_SELF_PROJECT,
    FREE_CASH,
    SEE_SELF_PROJECT
)

BASE_ROLE = (
    GET_NOTIFICATION_SELF_TASK,
    GET_ARTIFACTS_SELF_PROJECT,
    FREE_CASH
)

SUPER_ROLE = (
    GET_NOTIFICATION_ANY_PROJECT,
    GET_ANALYTICS_ANY_PROJECT,
    SEE_ANY_PROJECT,
    REACTIVATE_TASK_ANY_PROJECT,
    FREE_CASH
)

ACCESS_LIST = {

    ROLE_ADMIN: (CHANGE_WORKFLOW, DELETE_USER),

    ROLE_FRANCHISE: KEY_PROJECT_ROLE,

    ROLE_COORDINATOR: BASE_ROLE + (APPOINT_IN_PROJECT, GET_ANALYTICS_ANY_PROJECT,
                                   SEE_ANY_PROJECT),

    ROLE_PROJECT_MANAGER: KEY_PROJECT_ROLE + (CREATE_GALA_PROJECT,
                                              CREATE_FRANCH_PROJECT,
                                              REACTIVATE_TASK_SELF_PROJECT),

    ROLE_DEVELOPEMENT_MANAGER: SUPER_ROLE,

    ROLE_CURATOR: BASE_ROLE,

    ROLE_TECHNICAL_SUPPORT: BASE_ROLE,

    ROLE_PRICE_MANAGER: BASE_ROLE,

    ROLE_MARKETING_MANAGER: BASE_ROLE,

    ROLE_LOGIST: BASE_ROLE,

    ROLE_MERCHANDISER: BASE_ROLE,

    ROLE_TECHNOLOGIST: BASE_ROLE,

    ROLE_STUDYING_CENTER: BASE_ROLE,

    ROLE_SECURITY_CENTER: BASE_ROLE,

    ROLE_ANALYTIC: BASE_ROLE,

    ROLE_SELECTION_CENTER: BASE_ROLE,

    ROLE_DESIGNER: BASE_ROLE,

    ROLE_AREND_CENTER: BASE_ROLE,

    ROLE_VISITING_COACH: BASE_ROLE,

}

