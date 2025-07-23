# Pull base image
FROM python:3.13-slim-bookworm

LABEL title="Django img"
LABEL version="1.0"
LABEL description="Debian-based image with Python/Django support for dwelly project"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# Copy project
COPY . .

# Install dependencies and create user in single image layer
RUN apt update && apt -y upgrade && \
    # install mandatory packages
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt && \
    # register user to run Django
    adduser \
      --disabled-password \
      --no-create-home \
      django

USER django

ENTRYPOINT ["./entrypoint.sh"]