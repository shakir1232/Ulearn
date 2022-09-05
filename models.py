# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Dump(models.Model):
    org_code = models.TextField(db_column='ORG_CODE')  # Field name made lowercase.
    organisation_name = models.TextField(db_column='Organisation_Name')  # Field name made lowercase.
    functionality = models.TextField(db_column='Functionality')  # Field name made lowercase.
    website = models.TextField(db_column='Website')  # Field name made lowercase.
    org_type = models.TextField(db_column='Org_Type')  # Field name made lowercase.
    geographic_scope = models.TextField(db_column='geographic_scope')  # Field name made lowercase.
    primary_technicalsector = models.TextField(db_column='Primary_TechnicalSector')  # Field name made lowercase.
    secondary_technicalsector = models.TextField(db_column='Secondary_TechnicalSector')  # Field name made lowercase.
    third_technicalsector = models.TextField(db_column='Third_TechnicalSector')  # Field name made lowercase.
    fourth_technicalsector = models.TextField(db_column='Fourth_TechnicalSector')  # Field name made lowercase.
    fifth_technicalsector = models.TextField(db_column='Fifth_TechnicalSector')  # Field name made lowercase.
    eco_system_tag = models.TextField(db_column='Eco_System_tag')  # Field name made lowercase.
    eco_map_sector = models.TextField(db_column='Eco_Map_Sector')  # Field name made lowercase.
    eco_map_subsector = models.TextField(db_column='Eco_Map_SubSector')  # Field name made lowercase.
    number_of_convener = models.IntegerField(db_column='Number_of_Convener')  # Field name made lowercase.
    number_of_challenges = models.IntegerField(db_column='Number_of_Challenges')  # Field name made lowercase.
    number_of_innovations = models.IntegerField(db_column='Number_of_Innovations')  # Field name made lowercase.
    number_of_referrals = models.IntegerField(db_column='Number_of_referrals')  # Field name made lowercase.
    number_of_matchmaker = models.IntegerField(db_column='Number_of_Matchmaker')  # Field name made lowercase.
    number_of_matchmaker_solution_received = models.IntegerField(db_column='Number_of_Matchmaker_solution_Received')  # Field name made lowercase.
    number_of_projects_ril = models.IntegerField(db_column='Number_of_projects_RIL')  # Field name made lowercase.
    total_number_of_interactions_ril = models.IntegerField(db_column='Total_number_of_interactions_RIL')  # Field name made lowercase.
    ulearn_subcategory = models.TextField(db_column='Ulearn_Subcategory')  # Field name made lowercase.
    date_of_last_contact = models.DateField(db_column='Date_of_last_contact')  # Field name made lowercase.
    status_remarks = models.TextField(db_column='Status_Remarks')  # Field name made lowercase.
    primary_contact_name = models.TextField(db_column='Primary_Contact_Name')  # Field name made lowercase.
    role = models.TextField(db_column='Role')  # Field name made lowercase.
    email = models.TextField(db_column='Email')  # Field name made lowercase.
    phone = models.TextField(db_column='Phone')  # Field name made lowercase.
    optional_contact = models.TextField(db_column='Optional_Contact')  # Field name made lowercase.
    location_base = models.TextField(db_column='Location_Base')  # Field name made lowercase.
    district = models.TextField(db_column='District')  # Field name made lowercase.
    refugee_settlement = models.TextField(db_column='Refugee_Settlement')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dump'
