# Utilizzo la libreria logging per tracciare su un file di log
try:
    import logging
    logging.basicConfig(filename='test_3xpert.log',level=logging.INFO)
    logging.info('module logging imported')
except ImportError:
    print 'che sfortuna, non possiamo tracciare nulla...'

# Utilizzo il modulo sys per cambiare la codifica di default
try:
    import sys
    logging.info('module sys imported')
except ImportError:
    logging.error('error: no module named sys imported')

# Utilizzo la libreria RE, che implementa le espressioni regolari in Python
try:
    import re
    logging.info('module re imported')
except ImportError:
    logging.error('error: no module named re imported')

# Import smtplib for the actual email sending function
try:
    import smtplib
    logging.info('module smtplib imported')
except ImportError:
    logging.error('error: no module named smtplib imported')

# Utilizzo la libreria Requests: HTTP for Humans 
try:
    import requests
    logging.info('module requests imported')
except ImportError:
    logging.error('error: no module named requests imported')

# Import sleep e randint per recuperare la pagina 3xpert con ritardi casuali all'interno di un intervallo
try:
    from time import sleep
    from random import randint
    logging.info('functions sleep and randint imported')
except ImportError:
    logging.error('error: no functions named time or random imported')

# Import datetime for timestamping
try:
    import datetime
    logging.info('module datetime imported')
except ImportError:
    logging.error('error: no module named datetime imported')

class XpertEmailTo:
    to = ''
    def __init__(self, to):
        self.to = to

class XpertEmailServer:
    emailLoggedIn = False
    def __init__(self, smtpserver, port, sender_usr, sender_pwd):
        try:
            self.smtpserver = smtplib.SMTP_SSL(smtpserver, port)
            self.smtpserver.ehlo()
            self.smtpserver.ehlo
            self.sender_usr = sender_usr
            self.sender_pwd = sender_pwd
            self.smtpserver.login(sender_usr, sender_pwd)
            self.emailLoggedIn = True
            logging.info('email logged in')
        except:
            self.emailLoggedIn = False
            logging.info('email not logged in')
    def xpertSendEmail(self, receiver, msg):
        try:
            logging.info(self.sender_usr)
            logging.info(receiver)
            self.smtpserver.sendmail(self.sender_usr, receiver, msg)
            logging.info('mail sent')
        except:
            logging.error('mail problem')
            self.emailLoggedIn = False
    def __del__(self):
        if self.smtpserver:
            self.smtpserver.close()
            logging.info('mail closed')

class XpertUser:
    login = ''
    pwd = ''
    def __init__(self, login, pwd):
        self.login = login
        self.pwd = pwd

class XpertPortal:
    xpertLoggedIn = False
    counter_domanda_ko = 0
    def __init__(self, sign_in_url, home_url):
        self.sign_in_url = sign_in_url
        self.home_url = home_url
        self.s = requests.session()
        reload(sys);
        sys.setdefaultencoding("utf8")
    def xpertScraping(self, matchme, url):
        webPage = self.s.get(url, verify = False, headers = {'User-agent': 'Mozilla/5.0'})        
        return re.search(matchme, str(webPage.text))
    def xpertLogin(self, payload):
        try:
            self.s.post(self.sign_in_url, payload, verify = False)
            self.xpertLoggedIn = True
            logging.info('3xpert logged in')
        except:
            xpertLoggedIn = False
            logging.info('3xpert not logged in')
    def xpertDomanda(self, domanda, emailTo, emailServer):
        domanda_ok = 'la tua domanda!'
        domanda_ko = 'non ci sono domande per te'
        # logging.info('Domanda')
        header = 'To: ' + emailTo + '\n' + 'From: ' + emailServer.sender_usr + '\n' + 'Subject: 3xpert\n'
        if (domanda):
            if (domanda.group(1) == domanda_ok):
                msg = header + '\n 3xpert, ' + domanda_ok + '\n\n'
                logging.info(emailServer)
                logging.info(emailTo)
                emailServer.xpertSendEmail(emailTo, msg)
                logging.info(domanda_ok)
            elif (domanda.group(1) == domanda_ko):
                logging.info(domanda_ko)
                if (self.counter_domanda_ko == 4):
                    msg = header + '\n 3xpert, ' + domanda_ko + '\n\n'
                    logging.info(emailServer)
                    logging.info(emailTo)
                    emailServer.xpertSendEmail(emailTo, msg)
                    logging.info(domanda_ko)
                    self.counter_domanda_ko = 0
                else:
                    self.counter_domanda_ko += 1
        else:
            msg = header + '\n 3xpert, homepage error ' + '\n\n'
            emailServer.xpertSendEmail(emailTo, msg)
            logging.error('homepage error')
#    def __del__(self):
#        if self.s:
#            self.s.close()
#            logging.info('Session closed')

def setupXpert(xpertEmailTo, xpertEmailServer, xpertUser, xpertPortal):
    try:
        header = 'To: ' + xpertEmailTo + '\n' + 'From: ' + xpertEmailServer.sender_usr + '\n' + 'Subject: 3xpert\n'
        msg = header + '\n email framework ready to be used \n\n'
        xpertEmailServer.xpertSendEmail(xpertEmailTo, msg)
    except:
        logging.error('email framework error')

    try:
        csrf = xpertPortal.xpertScraping('meta content="(.*)" name="csrf-token" /', xpertPortal.sign_in_url)
        logging.info(csrf.group(1))
        data = {'expert[email]': xpertUser.login, 'expert[password]': xpertUser.pwd, 'expert[remember_me]': '1', 'expert[terms_of_service]': '1', 'authenticity_token' : csrf.group(1)}
        xpertPortal.xpertLogin(data)
        logging.info('3xpert portal logged in')
    except:
        logging.error('3xpert portal error')
        header = 'To: ' + xpertEmailTo + '\n' + 'From: ' + xpertEmailServer.sender_usr + '\n' + 'Subject: 3xpert\n'
        msg = header + '\n 3xpert portal error \n\n'
        xpertEmailServer.xpertSendEmail(xpertEmailTo, msg)

    return {'emailLoggedIn':xpertEmailServer.emailLoggedIn, 'xpertPortalLoggedIn':xpertPortal.xpertLoggedIn}

if __name__ == "__main__":
    xpertEmailTo = XpertEmailTo('wladimiro.carapucci@gmail.com')
    xpertEmailServer = XpertEmailServer('smtp.gmail.com', 465, 'carapucci.bimby@gmail.com', 'bimbymio')
    xpertUser = XpertUser('wladimiro.carapucci@gmail.com', '3Xpert_3')
    xpertPortal = XpertPortal('https://social.tre.it/expert/sign_in', 'https://social.tre.it/expert')
    login = setupXpert(xpertEmailTo.to, xpertEmailServer, xpertUser, xpertPortal)
    if ((login['emailLoggedIn'] == True) and (login['xpertPortalLoggedIn'] == True)):
        while True:
            if (datetime.datetime.now().hour == 23):
                logging.info('3xpert, good night')
                sleep(8*60*60)
            elif (datetime.datetime.now().hour == 0):
                logging.info('3xpert, good night')
                sleep(7*60*60)
            elif (datetime.datetime.now().hour == 1):
                logging.info('3xpert, good night')
                sleep(6*60*60)
            elif (datetime.datetime.now().hour == 2):
                logging.info('3xpert, good night')
                sleep(5*60*60)
            elif (datetime.datetime.now().hour == 3):
                logging.info('3xpert, good night')
                sleep(4*60*60)
            elif (datetime.datetime.now().hour == 4):
                logging.info('3xpert, good night')
                sleep(3*60*60)
            elif (datetime.datetime.now().hour == 5):
                logging.info('3xpert, good night')
                sleep(2*60*60)
            elif (datetime.datetime.now().hour == 7):
                logging.info('3xpert, good night')
                sleep(1*60*60)
            else:
                logging.info(datetime.datetime.now())
                domanda_per_te = xpertPortal.xpertScraping('@Wladimiro Carapucci, (.*)</h1><div class="switcher', xpertPortal.home_url)
                if (xpertEmailServer.emailLoggedIn == False):
                    logging.info('email user not logged in')
                    xpertEmailServer = XpertEmailServer('smtp.gmail.com', 465, 'carapucci.bimby@gmail.com', 'bimbymio')
                    header = 'To: ' + xpertEmailTo.to + '\n' + 'From: ' + xpertEmailServer.sender_usr + '\n' + 'Subject: 3xpert\n'
                    msg = header + '\n email server created again\n\n'
                    xpertEmailServer.xpertSendEmail(xpertEmailTo.to, msg)
                    logging.info('email server created again')
                xpertPortal.xpertDomanda(domanda_per_te, xpertEmailTo.to, xpertEmailServer)
                # Random delay
                sleep(randint(300,330))
    else:
        logging.error('connections to be closed')
        header = 'To: ' + xpertEmailTo.to + '\n' + 'From: ' + xpertEmailServer.sender_usr + '\n' + 'Subject: 3xpert\n'
        msg = header + '\n 3xpert, setup error... exit\n\n'
        xpertEmailServer.xpertSendEmail(xpertEmailTo.to, msg)
        del xpertEmailServer
#        del xpertPortal
