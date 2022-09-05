from django.urls import path, include
from .views import *

urlpatterns = [
    path('filter-items/', FilterItemView.as_view()),
    path('filter-org/', FilterCleanDataView.as_view()),
    # path('search-org/', SearchView.as_view()),
    path('org-list/', CleanDataListView.as_view()),
    path('settlement-list/', OrgTypeListView.as_view()),
    path('org-type-list/', OrgTypeListView.as_view()),
    path('target-demographic-list/', TargetDemographicListView.as_view()),
    path('thematic-area-list/', ThematicAreaListView.as_view()),
    path('landing-page-content/', LandingPageContentView.as_view()),
    path('export-to-csv/',ExportCSVStudents.as_view()),
]