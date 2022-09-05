
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated
)
# from urllib3.connectionpool import xrange
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

import csv
#
from django.http import HttpResponse
#
from rest_framework.views import APIView
import datetime as dt


class OrgTypeCreateView(generics.CreateAPIView):
    """
       endpoint for retrieving the list of organization types
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgTypeContentSerializer


class OrgTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
       endpoint for retrieving the list of organization types
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgTypeContentSerializer
    lookup_field = 'pk'
    queryset = OrgType.objects.all()


class ThematicAreaCreateView(generics.CreateAPIView):
    """
       endpoint for creating the list of technical areas
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ThematicAreaContentSerializer


class ThematicAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
       endpoint for creating the list of technical areas
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ThematicAreaContentSerializer
    lookup_field = 'pk'
    queryset = ThematicArea.objects.all()


class SettlementCreateView(generics.CreateAPIView):
    """
       endpoint for creating the list of settlement
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SettlementContentSerializer


class SettlementDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
       endpoint for updating the list of settlement
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SettlementContentSerializer
    lookup_field = 'pk'
    queryset = Settlement.objects.all()


class TargetDemographicCreateView(generics.CreateAPIView):
    """
       endpoint for creating the list of technical areas
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetDemographicContentSerializer


class TargetDemographicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
       endpoint for creating the list of technical areas
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetDemographicContentSerializer
    lookup_field = 'pk'
    queryset = TargetDemographic.objects.all()


class LandingPageContentCreateView(APIView):
    """
       endpoint for retrieving the list of technical areas
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LandingPageContentDetailsSerializer


class LandingPageContentDetailsView(APIView):
    """
       endpoint for retrieving the list of technical areas
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LandingPageContentDetailsSerializer
    lookup_field = 'pk'
    queryset = LandingPageContent.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
       endpoint for creating the list of technical areas
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer
    lookup_field = 'username'
    queryset = User.objects.all()