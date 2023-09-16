import json
from kafka import KafkaProducer

from .models import CustomUser
from . import CustomerEvents


producer = KafkaProducer(bootstrap_servers="localhost:9092")


def obtain_user_payload(user_id):
    user = CustomUser.objects.get(pk=user_id)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_joined": str(user.date_joined),
        "updated_at": str(user.updated_at),
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified,
        "is_active": user.is_active,
        "login_points": user.login_points,
    }
    return payload


def kafka_user_account_created_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_CREATED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_account_verified_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_VERIFIED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_account_deactivated_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_DEACTIVATED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_account_reactivated_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_REACTIVATED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_account_suspended_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_SUSPENDED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_account_linked_to_google_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCOUNT_LINKED_TO_GOOGLE,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_email_change_request_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.EMAIL_CHANGE_REQUEST,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_email_changed_by_user_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.EMAIL_CHANGED_BY_USER,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_email_changed_by_admin_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.USER_EMAIL_CHANGED_BY_ADMIN,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_password_reset_request_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.PASSWORD_RESET_REQUEST,
        json.dumps(payload).encode("utf-8"),
    )



def kafka_password_reset_by_user_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.PASSWORD_RESET_BY_USER,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_password_changed_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.PASSWORD_CHANGED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_phone_change_request_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.PHONE_CHANGE_REQUEST,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_phone_changed_by_user_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.PHONE_CHANGED_BY_USER,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_user_phone_changed_by_admin_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.USER_PHONE_CHANGED_BY_ADMIN,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_login_attempt_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.LOGIN_ATTEMPT,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_successful_login_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.SUCCESSFUL_LOGIN,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_successful_logout_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.SUCCESSFUL_LOGOUT,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_two_factor_enabled_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.TWO_FACTOR_ENABLED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_two_factor_disabled_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.TWO_FACTOR_DISABLED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_two_factor_code_sent_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.TWO_FACTOR_CODE_SENT,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_two_factor_code_resent_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.TWO_FACTOR_CODE_RESENT,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_verification_email_requested_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.VERIFICATION_EMAIL_REQUESTED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_verification_email_sent_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.VERIFICATION_EMAIL_SENT,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_access_token_generated_event(user_id):
    payload = obtain_user_payload(user_id)
    producer.send(
        CustomerEvents.ACCESS_TOKEN_GENERATED,
        json.dumps(payload).encode("utf-8"),
    )