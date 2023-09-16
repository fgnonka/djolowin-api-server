from .models import CardAuction



def handle_auction_end(auction_id):
    """This function is called when an auction ends.
    It basically has two tasks:
    1. Mark the auction as complete.
    2. Mark the auction as sold if there are any bids on it.
    Args:
        auction: The auction that has ended.
    """
    auction = CardAuction.objects.get(pk=auction_id)
    auction.auction_complete = True
    if auction.highest_bidder:
        auction.sold = True
        auction.save()
    else:
        auction.sold = False
        auction.save()


