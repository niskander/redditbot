# customexceptions.py


class FailedLogin(Exception):
    def __init__(self, username, password, response, errorcode):
        self.username = username
        self.password = password
        self.response = response
        self.errorcode = errorcode

    #@property
    def message(self):
        m = 'Failed to log (%s, %s) in. Error code: %d. Response: %s' % \
            (self.username, self.password, self.errorcode, self.response)
        return m


class FailedFetch(Exception):
    def __init__(self, objectname, response, errorcode):
        self.objectname = objectname
        self.response = response
        self.errorcode = errorcode
    
    #@property
    def message(self):
        m = 'Failed to fetch %s. Errorcode: %d. Response: %s.' % \
            (self.objectname, self.errorcode, self.response)
        return m


class WrongInput(Exception):
    def __init__(self, wronginput, correctinput, context):
        self.wronginput = wronginput
        self.correctinput = correctinput
        self.context = context
   
    #@property
    def message(self):
        m = 'When %s, you inputted %s when you should have inputted %s' % \
            (self.context, self.wronginput, self.correctinput)
        return m


class LoginRequired(Exception):
    def __init__(self, requiredfor):
        self.requiredfor = requiredfor
    
    #@property
    def message(self):
        m = 'Login required for %s.' % self.requiredfor
        return m