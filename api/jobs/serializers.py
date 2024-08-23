from rest_framework import serializers

from jobs.models import Job, Note, TechStack
from jobs.validators import validate_job_link_by_source


class JobNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("content",)


class JobSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="jobs-detail")
    tech_stacks = serializers.StringRelatedField(many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = (
            "url",
            "title",
            "company",
            "tech_stacks",
            "status",
            "link",
            "applied_at",
            "job_source",
            "created_by",
            "description",
        )

    def validate(self, validated_data):
        validate_job_link_by_source(validated_data)

        return validated_data


class TechStackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TechStack
        fields = "__all__"
