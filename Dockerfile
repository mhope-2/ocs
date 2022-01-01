# Use Ubuntu as Operation System
FROM ubuntu:16.04

# Use python 3.8
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install -r requirements.txt

# Copy project 
COPY . /code/