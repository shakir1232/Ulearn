from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-settlement/', SettlementCreateView.as_view()),
    path('settlement-details/<pk>/', SettlementDetailsView.as_view()),
    path('create-org-type/', OrgTypeCreateView.as_view()),
    path('org-type-details/<pk>/', OrgTypeDetailView.as_view()),
    path('create-thematic-area/', ThematicAreaCreateView.as_view()),
    path('thematic-area-details/<pk>/', ThematicAreaDetailView.as_view()),
    path('create-target-demographic/', TargetDemographicCreateView.as_view()),
    path('target-demographic-details/<pk>/', TargetDemographicDetailView.as_view()),
    path('create-landing-page-content/', LandingPageContentCreateView.as_view()),
    path('landing-page-content-details/<pk>/', LandingPageContentDetailsView.as_view()),
    path('user-details/<username>/', UserDetailView.as_view()),
]