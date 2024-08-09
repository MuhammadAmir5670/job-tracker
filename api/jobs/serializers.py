from rest_framework import serializers

from jobs.models import TechStack


class TechStackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TechStack
        fields = "__all__"
