class AuctionEvents:
    """ The different auction event types. """
    
    AUCTION_CREATED = "auction_created"
    AUCTION_ENDED = "auction_ended"
    AUCTION_CANCELLED = "auction_cancelled"
    
    AUCTION_BID_PLACED = "bid_placed"
    
    AUCTION_REPORTED = "auction_reported"
    
    AUCTION_FOLLOWED = "auction_followed"
    AUCTION_UNFOLLOWED = "auction_unfollowed"
    
    AUCTION_SOLD = "auction_sold"
    AUCTION_NOT_SOLD = "auction_not_sold"

    CHOICES = [
        (AUCTION_CREATED, "Auction created"),
        (AUCTION_ENDED, "Auction ended"),
        (AUCTION_CANCELLED, "Auction cancelled"),
        
        (AUCTION_BID_PLACED, "Bid placed"),
        
        (AUCTION_REPORTED, "Auction reported"),
        
        (AUCTION_FOLLOWED, "Auction followed"),
        (AUCTION_UNFOLLOWED, "Auction unfollowed"),
        
        (AUCTION_SOLD, "Auction sold"),
        (AUCTION_NOT_SOLD, "Auction not sold"),
    ]