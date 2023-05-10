# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and required files to the container
COPY es_bulk_load_script.py .

# Install the required libraries
RUN pip install elasticsearch tqdm

# Set the command to run your Python script
CMD [ "python", "es_bulk_load_script.py" ]