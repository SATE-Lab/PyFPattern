

def build_scope(self):
    subscription_scope = ('/subscriptions/' + self.subscription_id)
    if (self.scope is None):
        return subscription_scope
    return self.scope
