class AuctionRelatedEmailTypes:
    """ The different types of Auction related Emails that can be sent to a user."""
    
    AUCTION_BID_CONFIRMATION_EMAIL = "auction_bid_confirmation_email"
    AUCTION_WON_EMAIL = "auction_won_email"
    AUCTION_RESULT_SUMMARY_EMAIL = "auction_result_summary_email"
    AUCTION_CLOSING_SOON_EMAIL = "auction_closing_soon_email"
    AUCTION_RESUTS_ANALYSIS_EMAIL = "auction_results_analysis_email"
    AUCTION_MILESTONE_REACHED_EMAIL = "auction_milestone_reached_email"
    AUCTION_TIPS_NEWSLETTER_EMAIL = "auction_tips_newsletter_email"
    
    CHOICES = [
        (AUCTION_BID_CONFIRMATION_EMAIL, "Auction bid confirmation email"),
        (AUCTION_WON_EMAIL, "Auction won email"),
        (AUCTION_RESULT_SUMMARY_EMAIL, "Auction result summary email"),
        (AUCTION_CLOSING_SOON_EMAIL, "Auction closing soon email"),
        (AUCTION_RESUTS_ANALYSIS_EMAIL, "Auction results analysis email"),
        (AUCTION_MILESTONE_REACHED_EMAIL, "Auction milestone reached email"),
        (AUCTION_TIPS_NEWSLETTER_EMAIL, "Auction tips newsletter email"),
    ]