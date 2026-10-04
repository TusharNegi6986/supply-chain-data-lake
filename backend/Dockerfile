FROM python:3.13-slim

WORKDIR /app

# install postgresql client so 'psql' exists in the web image
RUN apt-get update && apt-get install -y postgresql-client --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy full project
COPY . .

# expose port
EXPOSE 8000

# start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]