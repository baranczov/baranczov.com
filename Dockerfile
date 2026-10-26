FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY . .
RUN DJANGO_DEBUG=1 python manage.py collectstatic --noinput \
    && useradd --create-home --uid 10001 portfolio \
    && mkdir -p /app/media && chown -R portfolio:portfolio /app
USER portfolio
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]

