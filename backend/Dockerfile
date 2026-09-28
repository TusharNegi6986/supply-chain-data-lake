FROM python:3.13-slim

WORKDIR /app

# requirements.txt lives in the backend/ folder (build context).
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the backend source into the image
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
