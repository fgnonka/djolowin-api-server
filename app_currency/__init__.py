class InAppCurrencyEvents:
    """ The different app currency event types. """
    
    IN_APP_CURRENCY_PURCHASED = "in_app_currency_purchased"
    IN_APP_CURRENCY_PURCHASE_FAILED = "in_app_currency_purchase_failed"
    IN_APP_CURRENCY_PURCHASE_REFUNDED = "in_app_currency_purchase_refunded"
    IN_APP_CURRENCY_PURCHASE_REVERSED = "in_app_currency_purchase_reversed"
    IN_APP_CURRENCY_PURCHASE_REVERSAL_FAILED = "in_app_currency_purchase_reversal_failed"

    CHOICES = [
        (IN_APP_CURRENCY_PURCHASED, "In app currency purchased"),
        (IN_APP_CURRENCY_PURCHASE_FAILED, "In app currency purchase failed"),
        (IN_APP_CURRENCY_PURCHASE_REFUNDED, "In app currency purchase refunded"),
        (IN_APP_CURRENCY_PURCHASE_REVERSED, "In app currency purchase reversed"),
        (IN_APP_CURRENCY_PURCHASE_REVERSAL_FAILED, "In app currency purchase reversal failed"),
    ]