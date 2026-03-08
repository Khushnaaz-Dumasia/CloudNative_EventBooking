FROM python:3.11-slim

WORKDIR /app

# In cloud, we just serve the static files using a simple http server
# or we could use Nginx, but sticking to Python is easier for a Demo
RUN pip install --no-cache-dir http-server || true

COPY . .

EXPOSE 80

CMD ["python3", "-m", "http.server", "80"]