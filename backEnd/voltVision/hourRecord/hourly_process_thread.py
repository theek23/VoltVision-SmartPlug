# import threading
# import time
# from datetime import datetime, timedelta
# from django.core.management import call_command
#
#
# def time_until_next_hour():
#     now = datetime.now()
#     next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
#     return (next_hour - now).total_seconds()
#
#
# def hourly_process_task():
#     while True:
#         time.sleep(time_until_next_hour())
#         call_command('hourly_process')
#
#
# def start_hourly_process():
#     # thread = threading.Thread(target=hourly_process_task, daemon=True)
#     # thread.start()
#     hourly_process_task()
#
#
