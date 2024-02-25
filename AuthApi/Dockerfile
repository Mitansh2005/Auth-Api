# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies (if any)
# RUN apt-get update && apt-get install -y <your-dependencies-here>

# Copy the requirements.txt file into the container at /code
COPY ./requirements.txt /code/

# Install pip dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
