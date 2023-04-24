from app.services.celery.celery import celery

__all__ = ('configuration_services',)


def init_celery(app, celery):
	TaskBase = celery.Task
	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)
	celery.Task = ContextTask


def configuration_services(app): 
	init_celery(app, celery)