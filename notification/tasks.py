from celery import shared_task

from custom_user.models import CustomUser

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

FRONTEND_URL = settings.DJOLOWIN_FRONTEND_URL


# --------------------------------------USER RELATED EMAILS--------------------------------------#
@shared_task
def send_verification_email(user_id):
    user = CustomUser.objects.get(pk=user_id)
    relative_url = reverse(
            "custom_user:verify-email", kwargs={"token": str(user.verification_token)}
        )
    verification_link = f"{FRONTEND_URL}{relative_url}"
    subject = "Verify Your Email"
    message = f"Hi {user.username}, please click the link below to verify your email:\n\n{verification_link}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_password_reset_email(user_id):
    user = CustomUser.objects.get(pk=user_id)
    relative_url = reverse(
            "custom_user:password-reset", kwargs={"token": str(user.reset_password_token)}
        )
    reset_password_link = f"{FRONTEND_URL}{relative_url}"
    # Send the email to the user
    subject = ("Password Reset",)
    message = (
        f"Hi {user.username}, Click the link below to reset your password:\n\n{reset_password_link}"
    )
    from_email = (settings.DEFAULT_FROM_EMAIL,)
    recipient_list = ([user.email],)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@shared_task
def send_welcome_email(username, email):
    subject = "Welcome to DjoloWin"
    message = f"Hi {username}, welcome to Djolowin. We hope you enjoy our services. \n\n Please feel free to contact us if you have any questions."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_password_change_request_email(username, email):
    subject = "Password Change Request"
    message = f"Hi {username}, you have requested to change your password. If this was not you please contact us immediately."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_password_change_confirmation_email(username, email):
    subject = "Password Change Confirmation"
    message = f"Hi {username}, your password has been changed. If this was not you please contact us immediately."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

# --------------------------------------AUCTION RELATED EMAILS--------------------------------------#


@shared_task
def send_auction_ending_soon_email(watcher_id, **auction_details):
    card_details = auction_details["card_details"]
    user = CustomUser.objects.get(pk=watcher_id)
    subject = f"Your auction for {card_details.player_name} is ending soon!"
    message = f"Hi {user.username}, the auction for {card_details.player_name} is ending soon. Please check the auction to see if there are any bids."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_auction_won_email(winner_id, auction):
    card = auction.card
    user = CustomUser.objects.get(pk=winner_id)
    subject = f"You won the auction for {card.player.name}!"
    message = f"Hi {user.username}, congratulations on winning the auction for {card.player.name}. Please check your collection to see your new card."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_auction_outbid_email(bidder_id, auction, bid_amount):
    card = auction.card
    user = CustomUser.objects.get(pk=bidder_id)
    bid_amount = bid_amount
    subject = f"You have been outbid on the auction for {card.player.name}!"
    message = f"Hi {user.username}, you have been outbid on the auction for {card.player.name}. The current bid is {bid_amount}. Please check the auction to see if you want to bid again."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_auction_created_email(**auction_details):
    """ Send a confirmation email to the seller when the auction is created."""
    user = CustomUser.objects.get(pk=auction_details["seller_id"])
    index = auction_details["card_details"]["index"]
    player_name = auction_details["card_details"]["player_name"]
    seller_name = auction_details["seller_name"]
    card_rarity = auction_details["card_details"]["rarity_name"]
    duration = auction_details["duration"]
    
    subject = f"Your auction for the {card_rarity} {player_name} has been created!"
    message = f"Hi {seller_name}, your auction for the {card_rarity} {player_name} Index {index} has been created and will last for {duration} hours. Please check the auction to see if there are any bids."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_auction_cancelled_email(**auction_details):
    """ Send a confirmation email to the seller when the auction is cancelled."""
    user = CustomUser.objects.get(pk=auction_details["seller_id"])
    index = auction_details["card_details"]["index"]
    player_name = auction_details["card_details"]["player_name"]
    seller_name = auction_details["seller_name"]
    card_rarity = auction_details["card_details"]["rarity_name"]
    
    subject = f"Your auction for the {card_rarity} {player_name} has been cancelled!"
    message = f"Hi {seller_name}, your auction for the {card_rarity} {player_name} Index {index} has been cancelled. Please check the auction to see if there are any bids."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)