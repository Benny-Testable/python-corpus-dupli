# Planted IaC fixture: runs as root and uses an unpinned base tag on purpose.
FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV API_TOKEN=changeme
EXPOSE 8000
CMD ["python", "-m", "pricing_service"]
