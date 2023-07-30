class UserNotifyEvent:
    ACCOUNT_CONFIRMATION = 'account_confirmation'
    ACCOUNT_PASSWORD_RESET = "account_password_reset"
    ACCOUNT_CHANGE_EMAIL_REQUEST = "account_change_email_request"
    ACCOUNT_CHANGE_EMAIL_CONFIRMATION = "account_change_email_confirmation"
    ACCOUNT_DELETE = "account_delete"
    ACCOUNT_SET_CUSTOMER_PASSWORD = "account_set_customer_password"
    INVOICE_READY = "invoice_ready"
    ORDER_CONFIRMATION = "order_confirmation"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_FULFILLMENT_CONFIRMATION = "order_fulfillment_confirmation"
    ORDER_FULFILLMENT_UPDATE = "order_fulfillment_update"
    ORDER_PAYMENT_CONFIRMATION = "order_payment_confirmation"
    ORDER_CANCELED = "order_canceled"
    ORDER_REFUND_CONFIRMATION = "order_refund_confirmation"
    SEND_GIFT_CARD = "send_gift_card"
    
    CHOICES = [
        ACCOUNT_CONFIRMATION,
        ACCOUNT_PASSWORD_RESET,
        ACCOUNT_CHANGE_EMAIL_REQUEST,
        ACCOUNT_CHANGE_EMAIL_CONFIRMATION,
        ACCOUNT_DELETE,
        ACCOUNT_SET_CUSTOMER_PASSWORD,
        INVOICE_READY,
        ORDER_CONFIRMATION,
        ORDER_CONFIRMED,
        ORDER_FULFILLMENT_CONFIRMATION,
        ORDER_FULFILLMENT_UPDATE,
        ORDER_PAYMENT_CONFIRMATION,
        ORDER_CANCELED,
        ORDER_REFUND_CONFIRMATION,
        SEND_GIFT_CARD,
    ]

class AdminNotifyEvent:
    ACCOUNT_STAFF_SET_PASSWORD = "account_staff_set_password"
    ACCOUNT_STAFF_PASSWORD_RESET = "account_staff_password_reset"
    CSV_EXPORT_FAILED = "csv_export_failed"
    CSV_EXPORT_SUCCESS = "csv_export_success"
    STAFF_ORDER_CONFIRMATION = "staff_order_confirmation"
    
    CHOICES = [
        ACCOUNT_STAFF_SET_PASSWORD,
        ACCOUNT_STAFF_PASSWORD_RESET,
        CSV_EXPORT_FAILED,
        CSV_EXPORT_SUCCESS,
        STAFF_ORDER_CONFIRMATION,
    ]
    
class NotifyEventType(UserNotifyEvent, AdminNotifyEvent):
    CHOICES = UserNotifyEvent.CHOICES + AdminNotifyEvent.CHOICES