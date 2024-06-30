FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set Working directory
WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements/local.txt

COPY . .

CMD sleep 7d
