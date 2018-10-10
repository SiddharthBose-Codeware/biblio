from Account import Account

class UserAccount(Account):
    def __init__(self):
        super(self.__class__, self).__init__()
        userId = models.CharField(max_length = 50)
