class InMemoryStorage:
    def __init__(self):
        self.users = []
        self.auth_accounts = []
        self.refresh_sessions = {}
        self.refresh_sessions_ttl = {}
