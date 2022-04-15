from factory import create_app
import z 

flask_app = create_app(celery=z.celery_app)