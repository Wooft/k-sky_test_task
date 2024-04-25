from celery import shared_task

@shared_task
def calculate_analytics():
    # Реализуйте логику расчета аналитики
    print('something')