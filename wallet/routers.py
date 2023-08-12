class WalletRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'wallet':
            return 'wallet_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'wallet':
            return 'wallet_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'wallet' or \
           obj2._meta.app_label == 'wallet':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'wallet':
            return db == 'wallet_db'
        return None