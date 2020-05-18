class Read:
    def __init__(self):
        self.command = "read"

class JoinLobby:
    def __init__(self, name):
        self.command = "joinlobby"

        self.name = name

class RequestStart:
    def __init__(self):
        self.command = "requeststart"
