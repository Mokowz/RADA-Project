## Set up project
```
git clone <github_url>

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Run Celery Worker
```
source venv/bin/activate
source env.sh
celery -A core.mycelery worker -l debug --pool=solo

celery -A core.mycelery beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```