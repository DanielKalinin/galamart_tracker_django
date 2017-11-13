from django.conf.urls import url
from . import views

urlpatterns = [

    # Main project workflow urls

    url(r'^project/create$',
        views.ProjectViewSet.as_view({'post': 'create'}),
        name='project-create',
    ),
    url(r'^project/list$',
        views.ProjectViewSet.as_view({'get': 'list'}),
        name='project-list',
    ),
    url(r'^project/get$',
        views.ProjectViewSet.as_view({'get': 'retrieve'}),
        name='project-retrieve',
    ),
    url(r'^project/update$',
        views.ProjectViewSet.as_view({'post': 'update'}),
        name='project-update',
    ),

    url(r'^container/get$',
        views.ContainerViewSet.as_view({'get': 'retrieve'}),
        name='container-detail',
    ),
    url(r'^container/list_children$',
        views.ContainerViewSet.as_view({'get': 'list_children'}),
        name='container-list-children',
    ),

    url(r'^work/get$',
        views.WorkViewSet.as_view({'get': 'retrieve'}),
        name='work-detail',
    ),
    url(r'^work/start$',
        views.WorkViewSet.as_view({'get': 'start'}),
        name='work-start',
    ),
    url(r'^work/complete$',
        views.WorkViewSet.as_view({'get': 'complete'}),
        name='work-complete',
    ),
    url(r'^work/verify$',
        views.WorkViewSet.as_view({'get': 'verify'}),
        name='work-verify',
    ),
    url(r'^work/deny$',
        views.WorkViewSet.as_view({'get': 'deny'}),
        name='work-deny',
    ),
    url(r'^work/reactivate$',
        views.WorkViewSet.as_view({'get': 'reactivate'}),
        name='work-reactivate',
    ),
    url(r'^work/free-cash/list/available$',
        views.WorkViewSet.as_view({'get': 'list_free_cash_available'}),
        name='list-free-cash-available',
    ),
     url(r'^work/free-cash/list/my$',
        views.WorkViewSet.as_view({'get': 'list_free_cash_workon'}),
        name='list-free-cash-workon',
    ),
    url(r'^work/post_message$',
        views.WorkViewSet.as_view({'post': 'post_message'}),
        name='work-post-message',
    ),

    url(r'^resource/get$',
        views.ResourceViewSet.as_view({'get': 'retrieve'}),
        name='resource-get',
    ),
    url(r'^resource/update$',
        views.ResourceViewSet.as_view({'post': 'update'}),
        name='resource-update',
    ),
    url(r'^resource/file_upload$',
        views.ResourceFileViewSet.as_view({'post': 'put_file'}),
        name='resource-file-upload',
    ),

    # Config generation urls

    url(r'^project_template/create$',
        views.ProjectTemplateViewSet.as_view({'post': 'create'}),
        name='project-template-create',
    ),
    url(r'^project_template/list$',
        views.ProjectTemplateViewSet.as_view({'get': 'list'}),
        name='project-template-list',
    ),
    url(r'^project_template/get$',
        views.ProjectTemplateViewSet.as_view({'get': 'retrieve'}),
        name='project-template-retrieve',
    ),
    url(r'^project_template/update$',
        views.ProjectTemplateViewSet.as_view({'post': 'update'}),
        name='project-template-update',
    ),
]
