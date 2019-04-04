from django.urls import path, include
from .views import *


score_urlpatterns = [
    path('', AppraisingScoreView.as_view(method=['POST'])),
    path('/<int:psid>', AppraisingScoreView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', AppraisingScoreInfo.as_view(method=['GET'])),
    path('/_mget', AppraisingScoreInfo.as_view(method=['POST'])),
]


urlpatterns = [
    # template
    path('', AppraisingView.as_view(method=['POST'])),
    path('/<int:pid>', AppraisingView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', AppraisingInfo.as_view(method=['GET'])),
    path('/_mget', AppraisingInfo.as_view(method=['POST'])),
    # score
    path('/scores', include(score_urlpatterns)),
    # manage
    path('/manage', AppraisingManageView.as_view(method=['GET', 'POST'])),
]
