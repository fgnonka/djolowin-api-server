class SportsRouter:
    def db_for_read(self, model, **hints):
        """ reading from sports database"""
        if model._meta.app_label == 'sports':
            return 'sports_db'
        return None

    def db_for_write(self, model, **hints):
        """ writing to sports database"""
        if model._meta.app_label == 'sports':
            return 'sports_db'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ make sure the sports app only appears in the 'sports' database"""
        if app_label == 'sports':
            #Migrate "Card" models only on the "sports" database
                return db == 'sports_db'
        return None