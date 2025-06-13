FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

# Torch needs additional index
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch==2.1.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Log papkasini yaratish
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs

# Application files
COPY . .

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]