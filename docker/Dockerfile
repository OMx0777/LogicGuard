FROM python:3.11-slim

# Install MONA (simplified; user installs locally)
# ADD mona /usr/local/bin/mona
# RUN chmod +x /usr/local/bin/mona

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "examples/refund_demo.py"]