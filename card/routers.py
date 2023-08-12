class CardRouter:
    def db_for_read(self, model, **hints):
        """ reading from card database"""
        if model._meta.app_label == 'card':
            return 'card_db'
        return None

    def db_for_write(self, model, **hints):
        """ writing to card database"""
        if model._meta.app_label == 'card':
            return 'card_db'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ make sure the card app only appears in the 'card' database"""
        if app_label == 'card':
            return db == 'card_db'
        return None