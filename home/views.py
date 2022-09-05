import datetime
import os
import traceback

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from rest_framework import generics

from .forms import ImportDataForm
from .models import *
from django import forms
import django_excel as excel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from titlecase import titlecase
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


def user_login(request):
    url = request.GET.get("next", '')
    print('url' + url)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(User.objects.filter(username=username, password=password).values('username'))
        print(username)
        try:
            get_user = User.objects.get(username=username)
        except:
            get_user = None
        if get_user is not None:
            # user = User.objects.get(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.username == 'ulearndevadmin':
                    return redirect('/admin/')
                if user.is_superuser:
                    return redirect('/')
                else:
                    return redirect('/')
            else:
                messages.error(request, 'Password is incorrect')
                return render(request, 'sign-in.html', {'url': url})

        else:
            messages.error(request, 'User not found!')
            return render(request, 'sign-in.html', {'url': url})

    else:
        return render(request, 'sign-in.html', {'url': url})


def user_logout(request):
    logout(request)
    return redirect('user_login')


class IndexView(View):
    def get(self, request):
        td_count = TargetDemographic.objects.all().count()
        settlement_count = Settlement.objects.all().count()
        org_type_count = OrgType.objects.all().count()
        ta_count = ThematicArea.objects.all().count()
        org_count = CleanData.objects.all().count()
        settlements = SettlementOrgAssociation.objects.values('settlement__value').order_by('settlement__value').annotate(count=Count('id'), count_org=Count('org_id'))
        org_types = CleanData.objects.filter(org_type__exclude_from_filter=False).values('org_type__value').order_by('org_type__value').annotate(count=Count('id'))
        context = {
            'settlement_count': settlement_count,
            'org_type_count': org_type_count,
            'td_count': td_count,
            'ta_count': ta_count,
            'org_count': org_count,
            'settlements': settlements,
            'org_types': org_types,
        }
        return render(request, 'index_ulearn.html', context)


class CleanDataView(View):
    def get(self, request):
        data = CleanData.objects.all()
        context = {
            'data': data
        }
        return render(request, 'cleandata.html', context)


class RawDataView(View):
    def get(self, request):
        data = Dump.objects.all()
        columns = Dump._meta.get_fields()
        print(columns)
        context = {
            'data': data,
            'columns': columns,
        }
        return render(request, 'raw_data.html', context)


class LoginView(View):
    def get(self, request):
        context = {
            'companies': None
        }
        return render(request, 'sign-in.html', context)


class SettlementView(View):
    def get(self, request):
        data = Settlement.objects.all()
        context = {
            'data': data
        }
        return render(request, 'settlements.html', context)


class OrgTypeView(View):
    def get(self, request):
        data = OrgType.objects.all()
        context = {
            'data': data
        }
        return render(request, 'org-type.html', context)


def update_org_associated_field(org_obj):
    all_settlements = SettlementOrgAssociation.objects.filter(org=org_obj)
    org_obj.associated_settlements = (', '.join(all_settlements.values_list('settlement__value', flat=True)))
    all_area = []
    for s in all_settlements:
        all_area = all_area + list(s.primary_thematic_area.values_list('value', flat=True))
    all_area = list(set(all_area))
    org_obj.associated_thematic_areas = (', '.join(all_area))
    org_obj.save()


class AddOrgView(View):
    def get(self, request):
        org_type = OrgType.objects.all()
        thematic_area = ThematicArea.objects.all()
        settlements = Settlement.objects.all()
        target_demo = TargetDemographic.objects.all()
        org_legal_type = ['Community-Based Organisation', 'Continental organisation', 'Foreign organisation', 'Indigenous organisation', 'International organisation', 'Regional organisation']
        target_group = ['Refugees', 'Host community', 'Refugees and Host community']
        context = {
            'org_type': org_type,
            'thematic_area': thematic_area,
            'settlements': settlements,
            'target_demo': target_demo,
            'org_legal_type': org_legal_type,
            'target_group': target_group,
        }
        return render(request, 'add-org.html', context)

    def post(self, request):
        if request.method == 'POST':
            org_name = request.POST.get('org_name')
            org_acronym = request.POST.get('org_acronym')
            org_email = request.POST.get('org_email')
            org_telephone = request.POST.get('org_telephone')
            org_website = request.POST.get('org_website')
            org_facebook = request.POST.get('org_facebook')
            org_twitter = request.POST.get('org_twitter')
            try:
                org_logo = request.FILES['org_logo']
            except:
                org_logo = None
            founding_year = request.POST.get('founding_year')
            org_primary_contact = request.POST.get('org_primary_contact')
            org_type = request.POST.get('org_type')
            org_legal_type = request.POST.get('org_legal_type')
            org_target_community = request.POST.get('org_target_community')
            org_target_demographic = request.POST.getlist('org_target_demographic')
            org_primary_technical_area_focus = request.POST.get('org_primary_technical_area_focus')
            contact_email = request.POST.get('contact_email')
            print(org_target_demographic)

            if founding_year.isnumeric():
                years_active = int(datetime.datetime.today().year) - int(founding_year) + 1
            else:
                founding_year = None
                years_active = None

            try:
                cdata = CleanData.objects.filter(org_name=org_name)
                if cdata.count() > 0:
                    cdata.update(
                        org_name=org_name,
                        org_acronym=org_acronym,
                        org_email=org_email,
                        org_phone=org_telephone,
                        org_website=org_website,
                        org_facebook=org_facebook,
                        org_twitter=org_twitter,
                        logo_img=org_logo,
                        founding_year=founding_year,
                        years_active=years_active,
                        org_primarycontact=org_primary_contact,
                        org_type_id=org_type,
                        org_legaltype=org_legal_type,
                        org_primary_technical_area_focus=org_primary_technical_area_focus,
                        org_targetgroup=org_target_community,
                        contact_email=contact_email,
                    )
                    SettlementOrgAssociation.objects.filter(org=cdata[0]).delete()
                    cleandata_ins = cdata[0]
                else:
                    cleandata_ins = CleanData(org_name=org_name,
                                              org_acronym=org_acronym,
                                              org_email=org_email,
                                              org_phone=org_telephone,
                                              org_website=org_website,
                                              org_facebook=org_facebook,
                                              org_twitter=org_twitter,
                                              logo_img=org_logo,
                                              founding_year=founding_year,
                                              years_active=years_active,
                                              org_primarycontact=org_primary_contact,
                                              org_type_id=org_type,
                                              org_legaltype=org_legal_type,
                                              org_primary_technical_area_focus=org_primary_technical_area_focus,
                                              org_targetgroup=org_target_community,
                                              contact_email=contact_email,
                                              )
                    cleandata_ins.save()
                cleandata_ins.org_targetdemographic.set(org_target_demographic)

                for j in range(Settlement.objects.all().count()):
                    i = j + 1
                    try:
                        print(i)
                        settlement = request.POST.get('settlement_' + str(i)).replace("'", "")
                        try:
                            number_of_staff = int(request.POST.get('number_of_staff_' + str(i)))
                        except:
                            number_of_staff = None
                        operation_offices = request.POST.get('operation_offices_' + str(i))
                        zones = request.POST.get('zone_' + str(i))
                        thematic_area = request.POST.getlist('thematic_area_' + str(i))
                        if settlement is not None and settlement != '':
                            sttlmnt_org_ins = SettlementOrgAssociation(
                                settlement_id=settlement,
                                org=cleandata_ins,
                                num_of_staffs=number_of_staff,
                                operation_offices=operation_offices,
                                zones=zones
                            )
                            sttlmnt_org_ins.save()
                            sttlmnt_org_ins.primary_thematic_area.set(thematic_area)
                    except Exception:
                        traceback.print_exc()
                        break

                update_org_associated_field(cleandata_ins)
                messages.success(request, 'Organization data updated successfully!')
            except Exception:
                messages.error(request, 'Failed to update organization data!')
                traceback.print_exc()
        return redirect('/add-org/')


class DeleteOrgView(View):
    def get(self, request, id):
        c_ins = CleanData.objects.get(id=id)
        SettlementOrgAssociation.objects.filter(org=c_ins).delete()
        c_ins.delete()
        return redirect('/org-list/')


class OrgDetailsView(View):
    def get(self, request, id):
        org_type = OrgType.objects.all()
        thematic_area = ThematicArea.objects.all()
        settlements = Settlement.objects.all()
        target_demo = TargetDemographic.objects.all()
        org_ins = CleanData.objects.get(id=id)
        org_legal_type = ['Community-Based Organisation', 'Continental organisation', 'Foreign organisation', 'Indigenous organisation', 'International organisation', 'Regional organisation']
        org_sttlmnt = SettlementOrgAssociation.objects.filter(org=org_ins)
        target_group = ['Refugees', 'Host community', 'Refugees and Host community']
        context = {
            'org_type': org_type,
            'thematic_area': thematic_area,
            'settlements': settlements,
            'target_demo': target_demo,
            'org': org_ins,
            'org_sttlmnt': org_sttlmnt,
            'org_legal_type': org_legal_type,
            'target_group': target_group,
        }
        return render(request, 'org-details.html', context)

    def post(self, request, id):
        if request.method == 'POST':
            org_name = request.POST.get('org_name')
            org_acronym = request.POST.get('org_acronym')
            org_email = request.POST.get('org_email')
            org_telephone = request.POST.get('org_telephone')
            org_website = request.POST.get('org_website')
            org_facebook = request.POST.get('org_facebook')
            org_twitter = request.POST.get('org_twitter')
            try:
                org_logo = request.FILES['org_logo']
            except:
                org_logo = None
            founding_year = request.POST.get('founding_year')
            org_primary_contact = request.POST.get('org_primary_contact')
            org_type = request.POST.get('org_type')
            org_legal_type = request.POST.get('org_legal_type')
            org_target_community = request.POST.get('org_target_community')
            org_target_demographic = request.POST.getlist('org_target_demographic')
            org_primary_technical_area_focus = request.POST.get('org_primary_technical_area_focus')
            contact_email = request.POST.get('contact_email')
            print(org_target_demographic)

            if founding_year.isnumeric():
                years_active = int(datetime.datetime.today().year) - int(founding_year) + 1
            else:
                founding_year = None
                years_active = None

            try:
                cdata = CleanData.objects.filter(org_name=org_name)
                if cdata.count() > 0:
                    cdata.update(
                        org_name=org_name,
                        org_acronym=org_acronym,
                        org_email=org_email,
                        org_phone=org_telephone,
                        org_website=org_website,
                        org_facebook=org_facebook,
                        org_twitter=org_twitter,
                        founding_year=founding_year,
                        years_active=years_active,
                        org_primarycontact=org_primary_contact,
                        org_type_id=org_type,
                        org_legaltype=org_legal_type,
                        org_primary_technical_area_focus=org_primary_technical_area_focus,
                        org_targetgroup=org_target_community,
                        contact_email=contact_email
                    )
                    SettlementOrgAssociation.objects.filter(org=cdata[0]).delete()
                    cleandata_ins = cdata[0]
                    cleandata_ins.org_targetdemographic.set(org_target_demographic)
                    if cleandata_ins.logo_img:
                        image_path = cleandata_ins.logo_img.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    cleandata_ins.logo_img = org_logo
                    cleandata_ins.save()
                    for j in range(Settlement.objects.all().count()):
                        i = j + 1
                        try:
                            print(i)
                            settlement = request.POST.get('settlement_' + str(i)).replace("'", "")
                            try:
                                number_of_staff = int(request.POST.get('number_of_staff_' + str(i)))
                            except:
                                number_of_staff = None
                            operation_offices = request.POST.get('operation_offices_' + str(i))
                            zones = request.POST.get('zone_' + str(i))
                            thematic_area = request.POST.getlist('thematic_area_' + str(i))
                            if settlement is not None and settlement != '':
                                sttlmnt_org_ins = SettlementOrgAssociation(
                                    settlement_id=settlement,
                                    org=cleandata_ins,
                                    num_of_staffs=number_of_staff,
                                    operation_offices=operation_offices,
                                    zones=zones
                                )
                                sttlmnt_org_ins.save()
                                sttlmnt_org_ins.primary_thematic_area.set(thematic_area)
                        except Exception:
                            traceback.print_exc()
                            continue

                    update_org_associated_field(cleandata_ins)
                    messages.success(request, 'Organization data updated successfully!')
                else:
                    messages.error(request, 'Failed to update organization data!')
                    return redirect('/org-details/' + id)
            except Exception:
                messages.error(request, 'Failed to update organization data!')
                traceback.print_exc()
                return redirect('/org-details/' + id)
        return redirect('/org-list/')


def delete_org(request, id):
    try:
        q_instance = CleanData.objects.get(id=id)
        if q_instance.logo_img:
            image_path = q_instance.logo_img.path
            if os.path.exists(image_path):
                os.remove(image_path)
        q_instance.delete()
        messages.success(request, 'Organization deleted successfully!')
    except:
        messages.error(request, 'Failed to delete organization!')
    return redirect('/org-list/')


class UpdateLogoView(View):
    def post(self, request, id):
        try:
            org_logo = request.FILES['org_logo']
            q = CleanData.objects.filter(id=id)
            if q.exists():
                q_instance = q.first()
                if q_instance.logo_img:
                    image_path = q_instance.logo_img.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                q_instance.logo_img = org_logo
                q_instance.save()
            print(org_logo)
            messages.success(request, 'Organization logo updated successfully!')
        except:
            messages.error(request, 'Failed to update logo!')

        return redirect('/org-list/')


class TargetDemoView(View):
    def get(self, request):
        data = TargetDemographic.objects.all()
        context = {
            'data': data
        }
        return render(request, 'target-demographic.html', context)


class ThematicAreaView(View):
    def get(self, request):
        data = ThematicArea.objects.all()
        context = {
            'data': data
        }
        return render(request, 'thematic-area.html', context)


class LandingPageContentView(View):
    def get(self, request):
        datas = LandingPageContent.objects.all()
        if datas.exists():
            data = datas[0]
        else:
            data = None
        context = {
            'data': data
        }
        return render(request, 'landing-page-content.html', context)

    def post(self, request):
        var_title1 = request.POST.get('title1'),
        print(var_title1)
        if request.method == 'POST':
            try:
                title1 = request.POST.get('title1')
                description1 = self.request.POST.get('description1')
                description1_url = self.request.POST.get('description1_url')
                map_description = self.request.POST.get('map_description')
                title2 = self.request.POST.get('title2')
                description2 = self.request.POST.get('description2')
                disclaimer = self.request.POST.get('disclaimer')
                access_form_url = self.request.POST.get('access_form_url')
                try:
                    banner_image = self.request.FILES['banner_image']
                except:
                    banner_image = None

                q = LandingPageContent.objects.all()

                # print(var_title1)
                if q.exists():
                    try:
                        q_instance = q.first()
                        if banner_image and banner_image != '' and banner_image != 'nan':
                            if q_instance.banner_image:
                                image_path = q_instance.banner_image.path
                                if os.path.exists(image_path):
                                    os.remove(image_path)
                            q_instance.banner_image = banner_image

                        q_instance.title1 = title1
                        q_instance.description1 = description1
                        q_instance.description1_url = description1_url
                        q_instance.map_description = map_description
                        q_instance.title2 = title2
                        q_instance.description2 = description2
                        q_instance.disclaimer = disclaimer
                        q_instance.access_form_url = access_form_url
                        q_instance.save()
                        messages.success(request, 'Landing page content has been updated successfully!')
                    except Exception as e:
                        print(e)
                        messages.error(request, 'Failed to update landing page content!')
                else:
                    try:
                        OrgDetailsPageContent.objects.create(
                            title1=title1,
                            description1=description1,
                            description1_url=description1_url,
                            map_description=map_description,
                            title2=title2,
                            description2=description2,
                            disclaimer=disclaimer,
                            access_form_url=access_form_url,
                            banner_image=banner_image
                        )
                        messages.success(request, 'Landing page content has been created successfully!')
                    except Exception as e:
                        print(e)
                        messages.error(request, 'Failed to create landing page content!')
            except Exception as e:
                print(e)
                messages.error(request, 'Failed to update landing page content!')

        return redirect('/landing-page-content/')


class OrgDetailsPageContentView(View):
    def get(self, request):
        data = OrgDetailsPageContent.objects.all().first()
        context = {
            'data': data
        }
        return render(request, 'orgdetails-page-content.html', context)

    def post(self, request):
        if request.method == 'POST':
            banner_image = self.request.FILES['banner_image']
            q = OrgDetailsPageContent.objects.all()
            if q.exists():
                try:
                    q_instance = q.first()
                    if q_instance.banner_image:
                        image_path = q_instance.banner_image.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    q_instance.banner_image = banner_image
                    q_instance.save()
                    messages.success(request, 'Org details page content has been updated successfully!')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Failed to update org details page content!')
            else:
                try:
                    OrgDetailsPageContent.objects.create(
                        banner_image=banner_image
                    )
                    messages.success(request, 'Org details page content has been created successfully!')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Failed to create org details page content!')
        return redirect('/org-details-page-content/')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserListView(View):
    def get(self, request):
        data = User.objects.all()
        context = {
            'data': data
        }
        return render(request, 'user_list.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreateView(View):
    def get(self, request):
        return render(request, 'user_create.html')

    def post(self, request):
        if request.method == 'POST' and request.user.is_superuser:
            username = self.request.POST.get('username')
            q = User.objects.filter(username=username)
            if q.exists():
                messages.error(request, 'User already exists with this username!')
            else:
                try:
                    name = self.request.POST.get('name')
                    email = self.request.POST.get('email')
                    password = self.request.POST.get('password')
                    user_type = self.request.POST.get('user_type')
                    print(user_type)
                    if user_type == 'admin':
                        is_staff = True
                        is_superuser = True
                    else:
                        is_staff = False
                        is_superuser = False

                    user = User.objects.create(
                        first_name=name,
                        email=email,
                        username=username,
                        is_superuser=is_superuser,
                        is_staff=is_staff
                    )
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'User (' + username + ') created successfully!')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Failed to create user!')
        return redirect('/user-list/')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UpdateUserView(View):
    def post(self, request, id):
        if request.method == 'POST':

            q = User.objects.filter(id=id)
            if not q.exists():
                messages.error(request, 'Failed to update user details!')
            else:
                try:
                    q_instance = q.first()
                    if request.user.is_superuser:
                        name = self.request.POST.get('name')
                        email = self.request.POST.get('email')
                        password = self.request.POST.get('password')
                        user_type = self.request.POST.get('user_type')
                        username = self.request.POST.get('username')
                        print(user_type)
                        if user_type == 'admin':
                            is_staff = True
                            is_superuser = True
                        else:
                            is_staff = False
                            is_superuser = False
                        q.update(
                            first_name=name,
                            email=email,
                            username=username,
                            is_superuser=is_superuser,
                            is_staff=is_staff
                        )
                        if password is not None and password != '':
                            q_instance.set_password(password)
                            q_instance.save()
                        messages.success(request, 'User (' + username + ') updated successfully!')
                    else:
                        messages.error(request, 'You do not have access to modify users!')
                        return redirect('/user-list/')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Failed to update user!')
        return redirect('/user-list/')


class ImportData(View):
    def post(self, request):
        # companies = CompanyInfo.objects.all()
        if request.method == 'POST':
            form = ImportDataForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print("form is invalid")
            return redirect('/')
        else:
            form = ImportDataForm()
            context = {
                'form': form
            }
            return render(request, 'import-excel.html', context)

    def get(self, request):
        # form = ImportDataForm()
        # context = {
        #     'form': form
        # }
        return render(request, 'import-excel.html')


def import_excel(request):
    if "GET" == request.method:
        return render(request, '/import-excel/', {})
    else:
        try:
            excel_file = request.FILES["excel_file"]

            import pandas as pd

            df = pd.read_excel(excel_file, sheet_name=0)

            alt_logos = AlternativeLogo.objects.all()

            for _, d in df.iterrows():
                try:
                    start = d['start']
                    end = d['end']
                    today = d['today']
                    logo = None  # d['logo']
                    name_personal = titlecase(str(d['name_personal']).replace('nan', ''))
                    job_title = str(d['job_title']).replace('nan', '')
                    email_address = str(d['email_address']).replace('nan', '')
                    respondent_telephone = str(d['respondent_telephone']).replace('nan', '').replace('.0', '')
                    org_name = titlecase(str(d['org_name']).replace('nan', ''))
                    org_acronym = str(d['org_acronym']).replace('nan', '')
                    org_email = str(d['org_email']).replace('nan', '')
                    org_telephone = str(d['org_telephone']).replace('nan', '').replace('.0', '')
                    org_website = str(d['org_website']).replace('nan', '')
                    org_facebook = str(d['org_facebook']).replace('nan', '')
                    org_twitter = str(d['org_twitter']).replace('nan', '')
                    org_logo = str(d['org_logo']).replace('nan', '')
                    img = str(d['img']).replace('nan', '')
                    img_URL = str(d['img_URL']).replace('nan', '')
                    founding_year = str(d['founding_year']).replace('nan', '').replace('_', '')[:4]
                    if founding_year.isnumeric():
                        print('Founding Year: ' + founding_year)
                        years_active = int(datetime.datetime.today().year) - int(founding_year) + 1
                    else:
                        founding_year = None
                        years_active = None

                    org_contact = str(d['org_contact']).replace('nan', '')
                    org_type = str(d['org_type']).replace('nan', '')
                    org_type_other = str(d['org_type_other']).replace('nan', '')
                    org_legal_type = titlecase(str(d['org_legal_type']).replace('nan', '').strip().replace('_', ' '))
                    org_legal_type_other = titlecase(
                        str(d['org_legal_type_other']).replace('nan', '').strip().replace('_', ' '))
                    org_target_community = titlecase(
                        str(d['org_target_community']).replace('nan', '').strip().replace('_', ' '))
                    org_target_community_other = titlecase(
                        str(d['org_target_community_other']).replace('nan', '').strip().replace('_',
                                                                                                ' '))
                    org_target_demographic = str(d['org_target_demographic']).replace('nan', '')
                    org_target_demographic_other = str(d['org_target_demographic_other']).replace('nan', '')
                    settlement_operation = str(d['settlement_operation']).replace('nan', '')
                    org_primary_technical_area_focus = str(d['org_primary_technical_area_focus']).replace('nan', '')
                    refugee_settlement = str(d['refugee_settlement']).replace('nan', '')

                    other_actors_in_settlement = str(d['other_actors_in_settlement']).replace('nan', '')

                    contact_name = str(d['contact_name']).replace('nan', '')
                    contact_role = str(d['contact_role']).replace('nan', '')
                    contact_telephone = str(d['contact_telephone']).replace('nan', '').replace('.0', '')
                    contact_email = str(d['contact_email']).replace('nan', '')

                    _id = d['_id']
                    _uuid = d['_uuid']
                    _submission_time = d['_submission_time']
                    _validation_status = d['_validation_status']
                    _notes = d['_notes']
                    _status = d['_status']
                    _submitted_by = d['_submitted_by']
                    _tags = d['_tags']
                    _index = d['_index']

                    if org_name is None or org_name.strip() == '':
                        continue

                    if org_type.strip() not in ('', 'None', 'Other', 'other', 'nan') and org_type is not None:
                        org_type_ins = OrgType.objects.get_or_create(value=titlecase(org_type.strip().replace('_', ' ')),
                                                                     title=titlecase(org_type.strip().replace('_', ' ')),
                                                                     exclude_from_filter=False
                                                                     )[0]
                    elif org_type.strip() in ('Other', 'other') and org_type_other is not None and org_type_other not in (
                            '', 'None'):
                        org_type_ins = \
                            OrgType.objects.get_or_create(value=titlecase(org_type_other.strip().replace('_', ' ')),
                                                          title=titlecase(org_type_other.strip().replace('_', ' ')))[0]
                    else:
                        org_type_ins = None

                    target_demo_list = []
                    if org_target_demographic.strip() not in (
                            '', 'None', 'NaN', 'Nan', 'nan') and org_target_demographic is not None:
                        target_demos = str(org_target_demographic.strip()).split(' ')
                        for td in target_demos:
                            if td not in ('', 'None', 'Other', 'other', 'NaN') and org_target_demographic is not None:
                                target_demo_list.append(
                                    TargetDemographic.objects.get_or_create(value=titlecase(td.strip().replace('_', ' ')),
                                                                            title=titlecase(td.strip().replace('_', ' ')),
                                                                            exclude_from_filter=False
                                                                            )[0].id
                                )
                            # else:
                            #     target_demo_list.append(TargetDemographic.objects.get_or_create(
                            #         value=titlecase(org_target_demographic_other.strip()),
                            #         title=titlecase(org_target_demographic_other.strip()))[0].id)
                    else:
                        org_target_demographic_ins = None

                    if org_target_community.strip() not in (
                            '', 'None', 'Other', 'other', 'nan') and org_target_community is not None:
                        org_target_community_val = titlecase(org_target_community.strip().replace('_', ' '))
                    else:
                        org_target_community_val = titlecase(org_target_community_other.replace('nan', '').replace('_', ' '))

                    # # ORG logo cleanup
                    # if img_URL not in ('', 'nan', 'None') and img_URL is not None:
                    #     print("Image URL" + img_URL)
                    #     pass
                    # else:
                    #     alt_logo_ins = alt_logos.filter(org_type__title=org_type).first()
                    #     if alt_logo_ins is not None:
                    #         img_URL = request.build_absolute_uri(alt_logo_ins.logo.url)
                    #
                    #     print("Image URL" + img_URL)

                    # Insert Org data to Clean Data
                    cdata = CleanData.objects.filter(org_name=org_name)
                    print(cdata.count())
                    if cdata.count() > 0:
                        cdata.update(
                            respondent_name=name_personal,
                            respondent_job_title=job_title,
                            respondent_email_address=email_address,
                            respondent_telephone=respondent_telephone,
                            org_name=org_name,
                            org_acronym=org_acronym,
                            org_email=org_email,
                            org_phone=org_telephone,
                            org_website=org_website,
                            org_facebook=org_facebook,
                            org_twitter=org_twitter,
                            org_logo=img_URL,
                            founding_year=founding_year,
                            years_active=years_active,
                            org_primarycontact=org_contact,
                            org_type=org_type_ins,
                            org_legaltype=org_legal_type,
                            org_primary_technical_area_focus=org_primary_technical_area_focus,
                            org_targetgroup=org_target_community_val,
                            other_actors_in_settlement=other_actors_in_settlement,
                            contact_name=contact_name,
                            contact_role=contact_role,
                            contact_phone=contact_telephone,
                            contact_email=contact_email,
                            uuid=_uuid
                        )
                        SettlementOrgAssociation.objects.filter(org=cdata[0]).delete()
                        cleandata_ins = cdata[0]
                    else:
                        cleandata_ins = CleanData(respondent_name=name_personal,
                                                  respondent_job_title=job_title,
                                                  respondent_email_address=email_address,
                                                  respondent_telephone=respondent_telephone,
                                                  org_name=org_name,
                                                  org_acronym=org_acronym,
                                                  org_email=org_email,
                                                  org_phone=org_telephone,
                                                  org_website=org_website,
                                                  org_facebook=org_facebook,
                                                  org_twitter=org_twitter,
                                                  org_logo=img_URL,
                                                  founding_year=founding_year,
                                                  years_active=years_active,
                                                  org_primarycontact=org_contact,
                                                  org_type=org_type_ins,
                                                  org_legaltype=org_legal_type,
                                                  org_primary_technical_area_focus=org_primary_technical_area_focus,
                                                  org_targetgroup=org_target_community_val,
                                                  other_actors_in_settlement=other_actors_in_settlement,
                                                  contact_name=contact_name,
                                                  contact_role=contact_role,
                                                  contact_phone=contact_telephone,
                                                  contact_email=contact_email,
                                                  uuid=_uuid
                                                  )
                        cleandata_ins.save()
                    cleandata_ins.org_targetdemographic.set(target_demo_list)

                    l_primary_thematic_areas = ''
                    l_staffs_raw = ''
                    l_operation_offices_raw = ''
                    l_zones_raw = ''
                    settlement_raw_list = []

                    refugee_settlement = str(refugee_settlement).strip()
                    settlement_list = refugee_settlement.split(' ')
                    for l in settlement_list:
                        if l is not None and l != '':
                            if '_camp' in l:
                                l = l.replace('_camp', '')
                            settlement_name = l.strip()
                            zone_col_nm = l + "_one"
                            # print(zone_col_nm)
                            if zone_col_nm != 'nan_one' and zone_col_nm != '_one':
                                try:
                                    l_zones_raw = str(d[zone_col_nm]).replace('nan', '')
                                    l_zones_raw = l_zones_raw.strip()
                                    l_zones = l_zones_raw.replace(' ', ', ')
                                    l_zones = titlecase(l_zones.replace('_', ' '))
                                except:
                                    l_zones = None
                                # print(l_zones)
                            else:
                                l_zones = None

                            operations_col_nm = l + "_two"
                            if operations_col_nm != 'nan_two' and operations_col_nm != '_two':
                                try:
                                    l_operation_offices_raw = d[operations_col_nm].strip().replace('nan', '')
                                    l_operation_offices = l_operation_offices_raw.strip()
                                    l_operation_offices = l_operation_offices.replace(' ', ', ')
                                    l_operation_offices = l_operation_offices.replace(',,', ',')
                                    l_operation_offices = titlecase(l_operation_offices.replace('_', ' '))
                                except:
                                    l_operation_offices = None
                                # print(l_operation_offices)
                            else:
                                l_operation_offices = None

                            staff_col_nm = l + "_three"
                            if staff_col_nm != 'nan_three' and staff_col_nm != '_three':
                                try:
                                    l_staffs_raw = str(d[staff_col_nm]).replace('nan', '0')
                                    l_staffs = int(l_staffs_raw.replace('.0', ''))
                                except:
                                    l_staffs = None
                                # print("This is Stuff number: " + str(l_staffs))
                            else:
                                l_staffs = None
                            primary_thematic_area_col_nm = l + "_four"
                            pta_id_list = []
                            if primary_thematic_area_col_nm != 'nan_four' and staff_col_nm != '_four':
                                try:
                                    l_primary_thematic_areas = str(d[primary_thematic_area_col_nm]).replace('nan', '')
                                    primary_thematic_list = str(l_primary_thematic_areas).split(' ')
                                    for pta in primary_thematic_list:
                                        if str(pta) in ('Other', 'other'):
                                            pta_other = d[primary_thematic_area_col_nm + '_other'].strip().replace('nan', '')
                                            # if pta_other != '':
                                            #     pta_id_list.append(
                                            #         ThematicArea.objects.get_or_create(
                                            #             value=titlecase(pta_other.replace('_', ' ')),
                                            #             title=titlecase(pta_other.replace('_', ' ')))[
                                            #             0].id)
                                        elif pta not in ('', 'nan'):
                                            pta_id_list.append(
                                                ThematicArea.objects.get_or_create(value=titlecase(pta.replace('_', ' ')),
                                                                                   title=titlecase(pta.replace('_', ' ')),
                                                                                   exclude_from_filter=False
                                                                                   )[0].id)
                                except:
                                    l_primary_thematic_areas = None
                                # print(l_primary_thematic_areas)

                            settlement_ins = \
                                Settlement.objects.get_or_create(value=titlecase(settlement_name.replace('_', ' ')),
                                                                 title=titlecase(settlement_name.replace('_', ' ')))[
                                    0]
                            sttlmnt_org_ins = SettlementOrgAssociation(
                                settlement=settlement_ins,
                                org=cleandata_ins,
                                num_of_staffs=l_staffs,
                                operation_offices=l_operation_offices,
                                zones=l_zones
                            )
                            sttlmnt_org_ins.save()
                            sttlmnt_org_ins.primary_thematic_area.set(pta_id_list)
                            update_org_associated_field(cleandata_ins)

                            settlement_dict = {
                                "settlement_name": settlement_name,
                                "primary_thematic_area": l_primary_thematic_areas,
                                "number_of_staffs": l_staffs_raw,
                                "operation_offices": l_operation_offices_raw,
                                "zones": l_zones_raw,
                            }
                            settlement_raw_list.append(settlement_dict)
                    try:
                        d = Dump.objects.create(
                            respondent_name=name_personal,
                            respondent_job_title=job_title,
                            respondent_email_address=email_address,
                            respondent_telephone=respondent_telephone,
                            org_name=org_name,
                            org_acronym=org_acronym,
                            org_email=org_email,
                            org_phone=org_telephone,
                            org_website=org_website,
                            org_facebook=org_facebook,
                            org_twitter=org_twitter,
                            org_logo=img_URL,
                            founding_year=founding_year,
                            years_active=years_active,
                            org_primarycontact=org_contact,
                            settlement_operation=settlement_operation,
                            org_type=org_type,
                            org_type_other=org_type_other,
                            org_legaltype=org_legal_type,
                            org_legaltype_other=org_legal_type_other,
                            org_primary_technical_area_focus=org_primary_technical_area_focus,
                            org_targetgroup=org_target_community_val,
                            org_targetgroup_other=org_target_community_other,
                            org_targetdemographic=org_target_demographic,
                            org_targetdemographic_other=org_target_demographic_other,
                            other_actors_in_settlement=other_actors_in_settlement,
                            contact_name=contact_name,
                            contact_role=contact_role,
                            contact_phone=contact_telephone,
                            contact_email=contact_email,
                            uuid=_uuid,
                        )
                        for idx, item in enumerate(settlement_raw_list):
                            DumpSettlements.objects.create(
                                org=d,
                                settlement=item["settlement_name"],
                                primary_thematic_area=item["primary_thematic_area"],
                                num_of_staffs=item["number_of_staffs"],
                                operation_offices=item["operation_offices"],
                                zones=item["zones"]
                            )
                            # if idx == 0:
                            #     d.settlement_1 = item
                            # elif idx == 1:
                            #     d.settlement_2 = item
                            # elif idx == 2:
                            #     d.settlement_3 = item
                            # elif idx == 3:
                            #     d.settlement_4 = item
                            # elif idx == 4:
                            #     d.settlement_5 = item
                        # d.save()

                    except Exception:
                        traceback.print_exc()
                except Exception:
                    traceback.print_exc()
            messages.success(request, 'File imported successfully!')
            return redirect('/')
        except:
            messages.error(request, 'Failed to import file!')
            return redirect('/import-excel/')
# return redirect('/')
# return render(request, 'exceldata.html', {"excel_data": excel_data})
