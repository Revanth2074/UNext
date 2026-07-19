from typing import Callable


Notification = Callable[[str, str], None]


def email_notification(member: str, message: str):
    print(f"[EMAIL] To: {member}")
    print(message)


def sms_notification(member: str, message: str):
    print(f"[SMS] To: {member}")
    print(message)


def whatsapp_notification(member: str, message: str):
    print(f"[WHATSAPP] To: {member}")
    print(message)


def notify_member(member: str,
                  message: str,
                  notification_method: Notification):

    notification_method(member, message)