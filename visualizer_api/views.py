import json
from collections import OrderedDict

from django.apps import apps
from django.core import serializers as sz
from django.db.models import Q
from django.http import JsonResponse
# from knox.auth import TokenAuthentication
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

# Create your views here.


import re


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        ''''''>>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None  # Query to search for every search term
    if isinstance(query_string, str):
        # terms = normalize_query(query_string)
        terms = query_string
    else:
        terms = query_string
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query


class CleanDataListView(generics.ListAPIView):
    """
       endpoint for retrieving all data
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = CleanDataSerializer
    # --queryset = Dump.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        dump_list = CleanData.objects.all()
        return dump_list


class FilterCleanDataView(generics.ListAPIView):
    """
       endpoint for filtering clean data
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = CleanDataSerializer
    # --queryset = Dump.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
        context = super(FilterCleanDataView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        try:
            current_url = self.request.build_absolute_uri(self.request.get_full_path())
            # print(self.request.build_absolute_uri(self.request.get_full_path()))
        except:
            current_url = None
        response = super().list(request, args, kwargs)

        ODPC = OrgDetailsPageContent.objects.all().first()
        if ODPC is not None:
            odpc_banner_image = self.request.build_absolute_uri(ODPC.banner_image.url)
        else:
            odpc_banner_image = ''
        # Add data to response.data Example for your object:
        response.data['export_to_csv'] = current_url.replace('filter-org', 'export-to-csv')
        response.data['org_details_page_banner_img'] = odpc_banner_image

        return response

    def get_queryset(self):
        queryset = CleanData.objects.all().distinct()
        # print(self.request.GET['settlement'])
        # print(self.request.data['settlement'])

        try:
            settlement = (self.request.GET['settlement']).split(",")

            print('settlement: ')
            if settlement:
                settlement_q = get_query(settlement, ['associated_settlements'])
                queryset = queryset.filter(settlement_q)
                # print(settlement_q)
            else:
                settlement = None
        except Exception as e:
            settlement = None
            print(e)
        try:
            thematic_area = self.request.GET['thematic_area_of_work'].split(",")
            if thematic_area:
                # if thematic_area == 'Other':
                #     queryset = queryset.filter(org_settlement__primary_thematic_area__exclude_from_filter=True)
                # else:
                thematic_area_q = get_query(thematic_area, ['associated_thematic_areas'])
                queryset = queryset.filter(thematic_area_q)
                print(thematic_area_q)
            else:
                thematic_area = None
        except:
            thematic_area = None
        try:
            org_type = self.request.GET['type_of_org'].split(",")
            if org_type:
                if org_type[0] == 'Other':
                    print('inside type other field')
                    queryset = queryset.filter(org_type__exclude_from_filter=True)
                else:
                    org_type_q = get_query(org_type, ['org_type__value'])
                    queryset = queryset.filter(org_type_q)
            else:
                org_type = None
        except:
            org_type = None
        try:
            target_demographic = self.request.GET['target_demographic'].split(",")
            if target_demographic:
                # if target_demographic == 'Other':
                #     queryset = queryset.filter(org_targetdemographic__exclude_from_filter=True)
                # else:
                target_demographic_q = get_query(target_demographic, ['org_targetdemographic__value'])
                queryset = queryset.filter(target_demographic_q)
                    # print(target_demographic_q)
            else:
                target_demographic = None
        except:
            target_demographic = None

        # Search
        print('search start')
        if ('query' in self.request.GET) and self.request.GET['query'].strip():
            query_string = self.request.GET.get('query')
            print(query_string)
            if query_string is not None and query_string != '':
                query_string_list = list([query_string.strip()])
                entry_query = get_query(query_string_list,
                                        ['org_name', 'org_acronym', 'org_type__value',
                                         'associated_settlements', 'associated_thematic_areas',
                                         'org_targetgroup', 'org_targetdemographic__value'])

                # print(queryset)
                # print(entry_query)
                queryset = queryset.filter(entry_query)
                print(queryset)
        queryset = queryset.filter(org_type__exclude_from_filter=False)
        queryset = queryset.distinct()

        return queryset


class OrgTypeListView(generics.ListAPIView):
    """
       endpoint for retrieving the list of organization types
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = OrgTypeSerializer

    # --queryset = Dump.objects.all()
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        dump_list = OrgType.objects.all()
        return dump_list


# class GeographicScopeListView(generics.ListAPIView):
#     """
#        endpoint for retrieving the list of organization categories
#     """
#     # permission_classes = (IsAuthenticated,)
#     serializer_class = GeographicScopeSerializer
#     # --queryset = Dump.objects.all()
#     # pagination_class = LimitOffsetPagination
#
#     def get_queryset(self):
#         dump_list = GeographicScope.objects.all()
#         return dump_list


class ThematicAreaListView(generics.ListAPIView):
    """
       endpoint for retrieving the list of technical areas
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = ThematicAreaSerializer

    # --queryset = Dump.objects.all()
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        dump_list = ThematicArea.objects.all()
        return dump_list


class SettlementListView(generics.ListAPIView):
    """
       endpoint for retrieving the list of settlement
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = SettlementSerializer

    # --queryset = Dump.objects.all()
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        dump_list = Settlement.objects.all()
        return dump_list


class TargetDemographicListView(generics.ListAPIView):
    """
       endpoint for retrieving the list of technical areas
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = TargetDemographicSerializer

    # --queryset = Dump.objects.all()
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        dump_list = TargetDemographic.objects.all()
        return dump_list


class FilterItemView(APIView):
    def get(self, request):
        settlements = list(Settlement.objects.all().values('id', 'value').distinct())
        # geographic_scopes = list(GeographicScope.objects.all().values('id','value').distinct())
        type_of_org = list(OrgType.objects.filter(exclude_from_filter=False).values('id', 'value').distinct())
        thematic_area_of_work = list(
            ThematicArea.objects.filter(exclude_from_filter=False).values('id', 'value').distinct())
        type_of_demographic = list(
            TargetDemographic.objects.filter(exclude_from_filter=False).values('id', 'value').distinct())
        # new_dict = {'id': -1,'value': 'Other'}
        # c = new_dict.copy()
        # type_of_org.append(c)
        # thematic_area_of_work.append(c)
        # type_of_demographic.append(c)
        # type_of_org = type_of_org.append("{'id': -1, 'value': 'Other'}" )
        return JsonResponse({'settlements': settlements,
                             # 'graphic_scopes': geographic_scopes,
                             'type_of_org': type_of_org,
                             'thematic_area_of_work': thematic_area_of_work,
                             'target_demographic': type_of_demographic,
                             },
                            safe=False, status=status.HTTP_200_OK)


# def get(self, request):
#     query_string = ''
#     found_entries = None
#     if ('term' in request.GET) and request.GET['term'].strip():
#         query_string = request.GET.get('term')
#
#         entry_query = QSearch.get_query(self, query_string, ['name', 'code', 'sub_category__name'])
#
#         found_entries = Product.objects.filter(entry_query)
#         titles = list()
#         for product in found_entries:
#             titles.append(product.name)
#             # titles = [product.title for product in qs]
#         return JsonResponse(titles, safe=False)
#     return render(request, 'vendor/custom-order.html')

class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class SearchView(generics.ListAPIView):
    """
       endpoint for filtering clean data
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = CleanDataSerializer
    # --queryset = Dump.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
        context = super(SearchView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        try:
            if ('term' in self.request.GET) and self.request.GET['term'].strip():
                query_string = self.request.GET.get('term')
                entry_query = get_query(query_string,
                                        ['org_name', 'org_acronym', 'org_type__value', 'refugee_settlement__value',
                                         'refugee_zone', 'org_primarytechnicalarea__value',
                                         'org_secondarytechnicalarea1__value', 'org_secondarytechnicalarea2__value',
                                         'org_targetgroup', 'org_targetdemographic__value'])
                queryset = CleanData.objects.filter(entry_query)
            else:
                queryset = ''
        except:
            queryset = ''
        return queryset


class ExportCSVStudents(APIView):
    def get(self, request, *args, **kwargs):
        queryset = CleanData.objects.all().distinct()
        # print(self.request.GET['settlement'])
        # print(self.request.data['settlement'])

        try:
            settlement = (self.request.GET['settlement']).split(",")

            print('settlement: ')
            if settlement:
                settlement_q = get_query(settlement, ['associated_settlements'])
                queryset = queryset.filter(settlement_q)
                # print(settlement_q)
            else:
                settlement = None
        except Exception as e:
            settlement = None
            print(e)
        try:
            thematic_area = self.request.GET['thematic_area_of_work'].split(",")
            if thematic_area:
                # if thematic_area == 'Other':
                #     queryset = queryset.filter(org_settlement__primary_thematic_area__exclude_from_filter=True)
                # else:
                thematic_area_q = get_query(thematic_area, ['associated_thematic_areas'])
                queryset = queryset.filter(thematic_area_q)
                print(thematic_area_q)
            else:
                thematic_area = None
        except:
            thematic_area = None
        try:
            org_type = self.request.GET['type_of_org'].split(",")
            if org_type:
                if org_type[0] == 'Other':
                    print('inside type other field')
                    queryset = queryset.filter(org_type__exclude_from_filter=True)
                else:
                    org_type_q = get_query(org_type, ['org_type__value'])
                    queryset = queryset.filter(org_type_q)
            else:
                org_type = None
        except:
            org_type = None
        try:
            target_demographic = self.request.GET['target_demographic'].split(",")
            if target_demographic:
                # if target_demographic == 'Other':
                #     queryset = queryset.filter(org_targetdemographic__exclude_from_filter=True)
                # else:
                target_demographic_q = get_query(target_demographic, ['org_targetdemographic__value'])
                queryset = queryset.filter(target_demographic_q)
                # print(target_demographic_q)
            else:
                target_demographic = None
        except:
            target_demographic = None

        # Search
        print('search start')
        if ('query' in self.request.GET) and self.request.GET['query'].strip():
            query_string = self.request.GET.get('query')
            print(query_string)
            if query_string is not None and query_string != '':
                query_string_list = list([query_string.strip()])
                entry_query = get_query(query_string_list,
                                        ['org_name', 'org_acronym', 'org_type__value',
                                         'associated_settlements', 'associated_thematic_areas',
                                         'org_targetgroup', 'org_targetdemographic__value'])

                # print(queryset)
                # print(entry_query)
                queryset = queryset.filter(entry_query)
                print(queryset)
        queryset = queryset.filter(org_type__exclude_from_filter=False)
        queryset = queryset.distinct()

        ts = dt.datetime.now()
        print(int(ts.timestamp()))
        response = HttpResponse(content_type='text/csv')
        filename = u"organization_list_" + ts.strftime("%Y%m%d%H%M%S") + ".csv"
        response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)
        writer = csv.writer(
            response,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_ALL
        )
        column_list = [
            'Org name',
            'Org acronym',
            'Org mail address',
            'Org phone number',
            'Org website',
            'Year founded',
            'Org primary contact',
            'Org primary contact mail address',
            'Org category',
            'Settlements in which org operates',
            'Thematic areas of work',
            'Target groups',
        ]

        settlements = Settlement.objects.all().distinct().order_by('value')
        # print(column_list)
        writer.writerow(column_list)
        for f in queryset:
            column_value_list = [
                f.org_name,
                f.org_acronym,
                f.org_email,
                f.org_phone,
                f.org_website,
                f.founding_year,
                f.org_primarycontact,
                f.contact_email,
                f.org_type.value,
                f.associated_settlements,
                f.associated_thematic_areas,
                f.org_targetgroup
            ]
            writer.writerow(column_value_list)
        return response


# import csv
# from django.http import HttpResponse
#
# def csv(self):
#    response = HttpResponse(content_type='text/csv')
#    filename = u"fizzer.csv"
#    response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)
#    writer = csv.writer(
#       response,
#       delimiter=';',
#       quotechar='"',
#       quoting=csv.QUOTE_ALL
#    )
#
#    for f in CleanData.objects.all():
#       writer.writerow([f.foo, f.bar])
#
#    return response


class LandingPageContentView(APIView):
    """
       endpoint for retrieving the list of technical areas
    """

    # permission_classes = (IsAuthenticated,)
    # serializer_class = LandingPageContentSerializer

    # --queryset = Dump.objects.all()
    # pagination_class = LimitOffsetPagination

    def get(self, request):
        dump_list = LandingPageContent.objects.all().first()
        serializer = LandingPageContentSerializer(dump_list, many=False, context={"request": request})
        return Response(serializer.data)
