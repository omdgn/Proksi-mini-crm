#!/usr/bin/env python3
"""
Celery Worker Entry Point
Run with: celery -A celery_worker worker --loglevel=info --concurrency=2
"""

from app.tasks import celery_app

if __name__ == '__main__':
    celery_app.start()