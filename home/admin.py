from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import *

# Register your models here.


admin.site.site_header = "U-Learn Data Visualization Administration"


@admin.register(OrgType)
class OrgTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ['id', 'title', 'value']


@admin.register(OrgLegalType)
class OrgLegalTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ['id', 'title', 'value']


# @admin.register(GeographicScope)
# class GeographicScopeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'value')
#     search_fields = ['id', 'title', 'value']


@admin.register(ThematicArea)
class ThematicAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ['id', 'title', 'value']


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ['id', 'title', 'value']


@admin.register(TargetDemographic)
class TargetDemographicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value')
    search_fields = ['id', 'title', 'value']


@admin.register(LandingPageContent)
class LandingPageContentAdmin(admin.ModelAdmin):
    list_display = ('title1',)
    search_fields = ['title', ]


@admin.register(SettlementOrgAssociation)
class SettlementOrgAssociationAdmin(admin.ModelAdmin):
    list_display = ('id','get_org_name', 'get_settlement_name')
    search_fields = ['org__org_name', 'settlement__value']

    def get_org_name(self, obj):
        return obj.org.org_name

    get_org_name.short_description = 'Organization Name'

    def get_settlement_name(self, obj):
        return obj.settlement.value

    get_settlement_name.short_description = 'Organization Name'


# admin.site.register(AlternativeLogo)
@admin.register(AlternativeLogo)
class AlternativeLogoAdmin(admin.ModelAdmin):
    list_display = ('org_type','logo')


@admin.register(OrgDetailsPageContent)
class OrgDetailsPageContentAdmin(admin.ModelAdmin):
    list_display = ('id','banner_image')


@admin.register(Dump)
class DumpAdmin(admin.ModelAdmin):
    list_display = ("id",
                    'respondent_name',
                    'respondent_job_title',
                    'respondent_email_address',
                    'respondent_telephone',
                    'org_name',
                    'org_acronym',
                    'org_email',
                    'org_phone',
                    'org_website',
                    'org_facebook',
                    'org_twitter',
                    'org_logo',
                    'founding_year',
                    'years_active',
                    'org_primarycontact',
                    'settlement_operation',
                    'org_type',
                    'org_legaltype',
                    'org_primary_technical_area_focus',
                    'org_targetgroup',
                    'org_targetdemographic',
                    'other_actors_in_settlement',
                    'contact_name',
                    'contact_role',
                    'contact_phone',
                    'contact_email',)
    search_fields = ["id",
                     'respondent_name',
                     'respondent_job_title',
                     'respondent_email_address',
                     'respondent_telephone',
                     'org_name',
                     'org_acronym',
                     'org_email',
                     'org_phone',
                     'org_website',
                     'org_facebook',
                     'org_twitter',
                     'org_logo',
                     'founding_year',
                     'years_active',
                     'org_primarycontact',
                     'settlement_operation',
                     'org_type',
                     'org_legaltype',
                     'org_primary_technical_area_focus',
                     'org_targetgroup',
                     'org_targetdemographic',
                     'other_actors_in_settlement',
                     'contact_name',
                     'contact_role',
                     'contact_phone',
                     'contact_email', ]


@admin.register(CleanData)
class CleanDataAdmin(admin.ModelAdmin):
    list_display = ("id",
                    'org_name',
                    'org_acronym',
                    'org_email',
                    'org_phone',
                    'org_website',
                    'org_facebook',
                    'org_twitter',
                    'org_logo',
                    'founding_year',
                    'years_active',
                    'org_primarycontact',
                    'settlement_operation',
                    'org_type',
                    'org_legaltype',
                    'org_primary_technical_area_focus',
                    'org_targetgroup')
    search_fields = ["id",
                     'org_name',
                     'org_acronym',
                     'org_email',
                     'org_primarycontact',
                     'settlement_operation',
                     'org_type',
                     'org_legaltype',
                     'org_primary_technical_area_focus',
                     'org_targetgroup',
                     'org_targetdemographic' ]


admin.site.register(DumpSettlements)
admin.site.register(LogEntry)