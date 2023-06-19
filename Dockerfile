# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the code
COPY . /app
WORKDIR /app

# Install dependencies
#RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --default-timeout=100

RUN chmod +x djnago-entry.sh

# Expose port 8000
EXPOSE 8000


# Set the entrypoint
CMD ["./djnago-entry.sh"]

## Start the Gunicorn server
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_social_network.wsgi"]