from plyer import notification
import schedule,time

def note():
    message="You have Pending Tasks to Complete..."
    notification.notify(
        title="Task Reminder",
        message=message,
        timeout=5
    )

schedule.every(10).seconds.do(note)

while True:
    schedule.run_pending()
    print(1)
    time.sleep(1)