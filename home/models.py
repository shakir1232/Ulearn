# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


# class User(AbstractUser):
# is_admin = models.BooleanField(default=False)


class OrgType(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')
    exclude_from_filter = models.BooleanField(default=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)


class OrgLegalType(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)


class GeographicScope(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)


class ThematicArea(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')
    exclude_from_filter = models.BooleanField(default=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)



class Settlement(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)


class TargetDemographic(models.Model):
    title = models.CharField(max_length=250, db_column='Title')
    value = models.CharField(max_length=250, db_column='Value')
    exclude_from_filter = models.BooleanField(default=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('value',)


class Dump(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    respondent_name = models.CharField(max_length=150, null=True, blank=True)
    respondent_job_title = models.CharField(max_length=250, null=True, blank=True)
    respondent_email_address = models.CharField(max_length=250, null=True, blank=True)
    respondent_telephone = models.CharField(max_length=50, null=True, blank=True)

    org_name = models.TextField(max_length=1000, null=True, blank=True)  # Field name made lowercase.
    org_acronym = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.

    org_email = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_phone = models.CharField(max_length=50, null=True, blank=True)  # Field name made lowercase.
    org_website = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_facebook = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_twitter = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_logo = models.TextField(max_length=1250, null=True, blank=True)  # Field name made lowercase.
    founding_year = models.CharField(max_length=5, null=True, blank=True)  # Field name made lowercase.
    years_active = models.CharField(max_length=5, null=True, blank=True)  # Field name made lowercase.
    org_primarycontact = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    settlement_operation = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.
    associated_settlements = models.TextField(max_length=500, null=True, blank=True)
    associated_thematic_areas = models.TextField(max_length=1250, null=True, blank=True)
    total_num_of_staff = models.IntegerField(null=True, blank=True)

    org_type = models.CharField(max_length=100, null=True, blank=True)
    org_type_other = models.CharField(max_length=100, null=True, blank=True)
    org_legaltype = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.
    org_legaltype_other = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.

    org_primary_technical_area_focus = models.TextField(max_length=1000, null=True,
                                                        blank=True)  # Field name made lowercase.
    org_targetgroup = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_targetgroup_other = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_targetdemographic = models.TextField(max_length=500, null=True, blank=True)
    org_targetdemographic_other = models.TextField(max_length=500, null=True, blank=True)

    other_actors_in_settlement = models.CharField(max_length=10, null=True, blank=True)  # Field name made lowercase.

    contact_name = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    contact_role = models.CharField(max_length=150, null=True, blank=True)  # Field name made lowercase.
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # Field name made lowercase.
    contact_email = models.CharField(max_length=150, null=True, blank=True)  # Field name made lowercase.

    logo_img = models.ImageField(null=True, blank=True)
    uuid = models.CharField(max_length=250, null=True, blank=True)

    upsrt_dttm = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('org_name',)

    def __str__(self):
        return self.org_name


class DumpSettlements(models.Model):
    org = models.ForeignKey(Dump, on_delete=models.CASCADE, related_name='dump_settlement')
    settlement = models.CharField(max_length=120, null=True, blank=True)
    primary_thematic_area = models.CharField(max_length=250, null=True, blank=True)
    zones = models.CharField(max_length=250, null=True, blank=True)
    operation_offices = models.TextField(max_length=1000, null=True, blank=True)
    num_of_staffs = models.CharField(max_length=50,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.org.org_name + ' |----> ' +self.settlement

class CleanData(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    respondent_name = models.CharField(max_length=150, null=True, blank=True)
    respondent_job_title = models.CharField(max_length=250, null=True, blank=True)
    respondent_email_address = models.CharField(max_length=250, null=True, blank=True)
    respondent_telephone = models.CharField(max_length=50, null=True, blank=True)

    org_name = models.TextField(max_length=1000, null=True, blank=True)  # Field name made lowercase.
    org_acronym = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.

    org_email = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_phone = models.CharField(max_length=50, null=True, blank=True)  # Field name made lowercase.
    org_website = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_facebook = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_twitter = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_logo = models.TextField(max_length=1250, null=True, blank=True)  # Field name made lowercase.
    founding_year = models.CharField(max_length=5, null=True, blank=True)  # Field name made lowercase.
    years_active = models.CharField(max_length=5, null=True, blank=True)  # Field name made lowercase.
    org_primarycontact = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    settlement_operation = models.CharField(max_length=100, null=True, blank=True)  # Field name made lowercase.
    associated_settlements = models.TextField(max_length=500, null=True, blank=True)
    associated_thematic_areas = models.TextField(max_length=1250, null=True, blank=True)
    total_num_of_staff = models.IntegerField(null=True, blank=True)

    org_type = models.ForeignKey(OrgType, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='cd_org_type')  # Field name made lowercase.
    org_legaltype = models.TextField(null=True, blank=True)  # Field name made lowercase.

    org_primary_technical_area_focus = models.TextField(max_length=1000, null=True,
                                                        blank=True)  # Field name made lowercase.
    org_targetgroup = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    org_targetdemographic = models.ManyToManyField(TargetDemographic, related_name='cd_org_targetdemographic', null=True,blank=True)

    other_actors_in_settlement = models.CharField(max_length=10, null=True, blank=True)  # Field name made lowercase.

    contact_name = models.CharField(max_length=250, null=True, blank=True)  # Field name made lowercase.
    contact_role = models.CharField(max_length=150, null=True, blank=True)  # Field name made lowercase.
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # Field name made lowercase.
    contact_email = models.CharField(max_length=150, null=True, blank=True)  # Field name made lowercase.

    logo_img = models.ImageField(null=True, blank=True)
    uuid = models.CharField(max_length=250, null=True, blank=True)

    upsrt_dttm = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('org_name',)

    def __str__(self):
        return self.org_name


class SettlementOrgAssociation(models.Model):
    org = models.ForeignKey(CleanData, on_delete=models.CASCADE, related_name='org_settlement')
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE, related_name='settlement_org')
    primary_thematic_area = models.ManyToManyField(ThematicArea, related_name='settlement_primary_thematic_area',
                                                   null=True, blank=True
                                                   )
    zones = models.TextField(max_length=1000, null=True, blank=True)
    operation_offices = models.TextField(max_length=1000, null=True, blank=True)
    num_of_staffs = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     super(SettlementOrgAssociation, self).save(*args, **kwargs)
    #     all_settlements = SettlementOrgAssociation.objects.filter(org=self.org)
    #     self.org.associated_settlements = (', '.join(all_settlements.values_list('settlement__value', flat=True)))
    #     all_area = []
    #     for s in all_settlements:
    #         all_area = all_area + list(s.primary_thematic_area.values_list('value', flat=True))
    #     all_area = list(set(all_area))
    #     self.org.associated_thematic_areas = (', '.join(all_area))
    #     self.org.save()

    def delete(self, *args, **kwargs):
        super(SettlementOrgAssociation, self).delete(*args, **kwargs)
        all_settlements = SettlementOrgAssociation.objects.filter(org=self.org)
        self.org.associated_settlements = (', '.join(all_settlements.values_list('settlement__value', flat=True)))
        all_area = []
        for s in all_settlements:
            all_area = all_area + list(s.primary_thematic_area.values_list('value', flat=True))
        all_area = list(set(all_area))
        self.org.associated_thematic_areas = (', '.join(all_area))
        self.org.save()


class LandingPageContent(models.Model):
    title1 = models.CharField(max_length=250, null=True, blank=True)
    description1 = models.TextField(max_length=2050, null=True, blank=True)
    description1_url = models.CharField(max_length=250, null=True, blank=True)
    map_description = models.TextField(max_length=1050, null=True, blank=True)
    title2 = models.CharField(max_length=250, null=True, blank=True)
    description2 = models.TextField(max_length=2050, null=True, blank=True)
    disclaimer = models.TextField(max_length=2050, null=True, blank=True)
    access_form_url = models.CharField(max_length=250, null=True, blank=True)
    banner_image = models.ImageField(null=True, blank=True)
    future_use1 = models.CharField(max_length=250, null=True, blank=True)
    future_use2 = models.CharField(max_length=250, null=True, blank=True)
    future_use3 = models.TextField(max_length=2050, null=True, blank=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title1


class AlternativeLogo(models.Model):
    org_type = models.ForeignKey(OrgType, on_delete=models.CASCADE, related_name='org_type_logo')
    logo = models.ImageField(null=True, blank=True)
    logo_url = models.CharField(max_length=700, null=True, blank=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)


class OrgDetailsPageContent(models.Model):
    banner_image = models.ImageField(null=True, blank=True)
    future_use1 = models.CharField(max_length=250, null=True, blank=True)
    future_use2 = models.CharField(max_length=250, null=True, blank=True)
    future_use3 = models.TextField(max_length=2050, null=True, blank=True)
    upsrt_dttm = models.DateTimeField(auto_now=True)

# respondent_name
# respondent_job_title
# respondent_email_address
# respondent_telephone
# org_name
# org_acronym
# org_email
# org_phone
# org_website
# org_facebook
# org_twitter
# org_logo
# founding_year
# years_active
# org_primarycontact
# settlement_operation
# org_type
# org_legaltype
# org_primary_technical_area_focus
# org_targetgroup
# org_targetdemographic
# other_actors_in_settlement
# contact_name
# contact_role
# contact_phone
# contact_email
