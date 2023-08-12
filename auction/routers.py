class AuctionRouter:
    def db_for_read(self, model, **hints):
        """ reading from auction database"""
        if model._meta.app_label == 'auction':
            return 'auction_db'
        return None

    def db_for_write(self, model, **hints):
        """ writing to auction database"""
        if model._meta.app_label == 'auction':
            return 'auction_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ make sure the auction app only appears in the 'auction' database"""
        if app_label == 'auction':
            #Migrate "Auction" models only on the "auction" database
            return db == 'auction_db'
        return None