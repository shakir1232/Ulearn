from rest_framework import serializers
from home.models import *


class ThematicAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = '__all__'


class OrgTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgType
        fields = '__all__'


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'


class TargetDemographicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetDemographic
        fields = '__all__'


class SettlementOrgAssociationSerializer(serializers.ModelSerializer):
    settlement = serializers.CharField(
        source="settlement.value",
        read_only=True
    )
    primary_thematic_area = serializers.StringRelatedField(many=True)

    class Meta:
        model = SettlementOrgAssociation
        fields = ('settlement',
                  'primary_thematic_area',
                  'zones',
                  'operation_offices',
                  'num_of_staffs',
                  )


class TargetDemographicListingField(serializers.RelatedField):

    def to_representation(self, value):
        return value.value


class CleanDataSerializer(serializers.ModelSerializer):
    # # cover_image = Base64ImageField(required=True)
    # export_to_csv = serializers.SerializerMethodField()
    #
    # def get_export_to_csv(self, obj):
    #     request = self.context.get('request')
    #     current_url = request.build_absolute_uri(request.get_full_path())
    #     return current_url

    org_type = serializers.CharField(
        source="org_type.value",
        read_only=True
    )
    org_targetdemographic = TargetDemographicListingField(many=True, read_only=True)
    # org_targetdemographic = serializers.CharField(
    #     source="org_targetdemographic.value",
    #     read_only=True
    # )
    org_settlements = SettlementOrgAssociationSerializer(many=True, source='org_settlement')

    org_logo = serializers.SerializerMethodField()

    def get_org_logo(self, obj):
        if obj.logo_img:
            request = self.context.get('request')
            photo_url = obj.logo_img.url
            return request.build_absolute_uri(photo_url)
        else:
            return ''

    class Meta:
        model = CleanData
        fields = (
            "id",
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

            'associated_settlements',
            'associated_thematic_areas',

            'contact_name',
            'contact_role',
            'contact_phone',
            'contact_email',
            'org_settlements',
        )
        # fields = '__all__'
        read_only_fields = (
            'id',
            'publisher',
            'created',
            'updated'
        )

    # def to_representation(self, instance):
    #     data = super(CleanDataSerializer, self).to_representation(instance)
    #     print(data)
    #     # manipulate data here
    #     return data


class LandingPageContentSerializer(serializers.ModelSerializer):
    banner_image = serializers.SerializerMethodField()

    def get_banner_image(self, obj):
        # domain_name = self.request.META['HTTP_HOST']
        # storage_location = 'https://ulearn.asifkhanshakir.com'
        # img_url = f'{storage_location}/{obj.banner_image}'
        # return img_url

        request = self.context.get('request')
        photo_url = obj.banner_image.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = LandingPageContent
        fields = '__all__'
