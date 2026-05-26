# 1. Base Image: Start with a lightweight version of Python 3.11
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements file first (this helps with caching)
COPY requirements.txt .

# 4. Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your actual code into the container
COPY . .

# 6. Open port 8000 so the outside world can talk to the container
EXPOSE 8000

# 7. The command to start the server. 
# We use 0.0.0.0 so Uvicorn listens to all incoming network traffic.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]