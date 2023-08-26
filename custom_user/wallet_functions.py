from .models import UserWallet

def create_wallet(user_id):
    wallet = UserWallet.objects.create(user_id=user_id)
    return wallet