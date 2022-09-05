from rest_framework import serializers
from home.models import *


class ThematicAreaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = '__all__'


class OrgTypeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgType
        fields = '__all__'


class SettlementContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'


class TargetDemographicContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetDemographic
        fields = '__all__'


class SettlementOrgAssociationContentSerializer(serializers.ModelSerializer):
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


class LandingPageContentDetailsSerializer(serializers.ModelSerializer):
    banner_image = serializers.SerializerMethodField()

    class Meta:
        model = LandingPageContent
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandingPageContent
        fields = ('first_name',
                  'username',
                  'email',
                  'phone',
                  'is_stuff',
                  'is_superuser',
                  'password',
                  )

