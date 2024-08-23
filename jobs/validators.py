import re

from django.core.exceptions import ValidationError


def valid_regex(value):
    try:
        re.compile(value)
    except re.error as error:
        raise ValidationError(f"'{value}' is not a valid regular expression. | {error}")


def validate_job_link_by_source(validated_data):
    job_link = validated_data.get("link")
    job_source = validated_data.get("job_source")

    if not job_source or not job_link:
        return

    if not re.match(job_source.link_regex, job_link):
        raise ValidationError(f"Not a valid URL for the selected Job Source: {job_source}")
