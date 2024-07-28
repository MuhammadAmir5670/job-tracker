import re

from rest_framework import serializers

from jobs.models import Job, TechStack


class JobSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="jobs-detail")
    tech_stacks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = ("url", "title", "company", "tech_stacks", "status", "link", "applied_at", "job_source")

    def validate(self, validated_data):
        job_source = validated_data.get("job_source")
        job_link = validated_data.get("link")
        self._validate_job_source_link(job_source, job_link)

        return validated_data

    def _validate_job_source_link(self, job_source, job_link):
        if not job_source or not job_link:
            return

        if not re.match(job_source.link_regex, job_link):
            raise serializers.ValidationError(f"Not a valid URL for the selected Job Source: {job_source}")


class TechStackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TechStack
        fields = "__all__"
