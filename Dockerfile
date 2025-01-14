# Use a lightweight Python base image
FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file to the working directory
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code to the working directory
COPY . .
# Specify the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "shipstack_api:app", "--host", "0.0.0.0", "--port", "8000"]