from rest_framework import serializers

from .models import Coordinates, Directive, Station


class StationSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='get_state_display', read_only=True)

    class Meta:
        fields = ('id', 'name', 'state', 'created_at', 'break_date')
        model = Station


class CoordinatesSerializer(serializers.ModelSerializer):

    x = serializers.IntegerField(required=False)
    y = serializers.IntegerField(required=False)
    z = serializers.IntegerField(required=False)

    class Meta:
        fields = ('x', 'y', 'z')
        model = Coordinates


class DirectiveSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('user', 'axis', 'distance')
        model = Directive
