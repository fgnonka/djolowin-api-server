class CardEvents:
    """The different card event types."""

    CARD_PURCHASED = "card_purchased"
    CARD_PURCHASE_FAILED = "card_purchase_failed"

    CARD_SOLD = "card_sold"
    CARD_SALE_FAILED = "card_sale_failed"

    CARD_PRICE_UPDATED = "card_price_updated"
    CARD_MARKED_FOR_SALE = "card_marked_for_sale"
    CARD_UNMARKED_FOR_SALE = "card_unmarked_for_sale"

    CARD_LOCKED = "card_locked"
    CARD_UNLOCKED = "card_unlocked"

    CHOICES = [
        (CARD_PURCHASED, "Card purchased"),
        (CARD_PURCHASE_FAILED, "Card purchase failed"),
        (CARD_SOLD, "Card sold"),
        (CARD_SALE_FAILED, "Card sale failed"),
        (CARD_PRICE_UPDATED, "Card price updated"),
        (CARD_MARKED_FOR_SALE, "Card marked for sale"),
        (CARD_UNMARKED_FOR_SALE, "Card unmarked for sale"),
        (CARD_LOCKED, "Card locked"),
        (CARD_UNLOCKED, "Card unlocked"),
    ]
