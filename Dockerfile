
FROM python:3.11.2

# Copy the content of the project directory to the working directory
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# By default, listen on port 5000
EXPOSE 5000

# Specify the command to run on container start
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]