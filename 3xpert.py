#!/usr/bin/python

# print "Content-Type: text/plain"
# print
# print "Hello, 3xpert!"

# Utilizzo la libreria logging per tracciare su un file di log
try:
    import logging
    logging.basicConfig(filename='3xpert.log',level=logging.INFO)
    logging.info('Module logging imported')
except ImportError:
    print 'Che sfortuna, non possiamo tracciare nulla...'
# Utilizzo la libreria Requests: HTTP for Humans 
try:
    import requests
    logging.info('Module requests imported')
except ImportError:
    logging.error('ImportError: No module named requests')
# Utilizzo la libreria RE, che implementa le espressioni regolari in Python
try:
    import re
    logging.info('Module re imported')
except ImportError:
    logging.error('ImportError: No module named re')
import re
# Utilizzo il modulo sys per cambiare la codifica di default
try:
    import sys
    logging.info('Module sys imported')
except ImportError:
    logging.error('ImportError: No module named sys')
# Import smtplib for the actual email sending function
try:
    import smtplib
    logging.info('Module smtplib imported')
except ImportError:
    logging.error('ImportError: No module named smtplib')
# Import sleep e randint per recuperare la pagina 3xpert con ritardi casuali all'interno di un intervallo
try:
    from time import sleep
    from random import randint
    logging.info('Functions sleep and randint imported')
except ImportError:
    logging.error('ImportError: No module named time or random')
# Import datetime for timestamping
try:
    import datetime
    logging.info('Module datetime imported')
except ImportError:
    logging.error('ImportError: No module named datetime')



# ==========================================================================
# 1 GET
# ==========================================================================
# url_sign_in e' la pagina di login
url_sign_in = 'https://social.tre.it/expert/sign_in'
# url_expert_home e' l'home page che si richiede dopo il login e che
# contiene eventualmente la domanda
url_expert_home = 'https://social.tre.it/expert'

# Creo un oggetto session per avere la persistenza dei parametri (per esempio
# dei cookie) attraverso una richiesta e le successive
s = requests.session()
logging.info('Persistent session created')

# Utilizziamo il metodo di richiesta GET della sessione per
# recuperare la pagina di login.
# Ignoriamo la verifica del certificato SSL. Il valore di default e' True,
# ma in questo caso dovremmo specificare una lista di CA di fiducia,
# pena il lancio dell'eccezione requests.exceptions.SSLError
# Specifichiamo anche uno User-agent
r1 = s.get(url_sign_in, verify = False, headers = {'User-agent': 'Mozilla/5.0'})
logging.info('GET for sign_in page')

# ==========================================================================
# 2 POST
# ==========================================================================
# Prepariamo il payload del metodo POST con il quale passiamo i parametri
# necessari all'autenticazione. Oltre alle credenziali di accesso dobbiamo
# impostare anche il parametro terms_of_service, altrimenti il server
# non ci fa accedere. Per conoscere i nomi che devono essere usati
# sfruttiamo i Developer tools di Chrome.
# Nel metodo post rimandiamo, inoltre, il cookie di sessione: il nome
# utilizzato per esso e' _session_id (Developer Tools di Chrome).
# E' anche necessario mostrare al server che non e' in corso un
# attacco di tipo CSRF, impostando il paramentro authenticity_token
# del metodo POST con il valore letto dalla precedente GET del
# token CSRF.

# Attraverso il metodo search del modulo re, cerchiamo nella pagina
# di login ottenuta con il comando GET l'espressione regolare
# 'meta content="(.*)" name="csrf-token" /'

# Spostare sopra
# Per prima cosa dobbiamo modificare la codifica di default da ascii
# a utf-8 (http://mypy.pythonblogs.com/12_mypy/archive/1253_workaround_for_python_bug_ascii_codec_cant_encode_character_uxa0_in_position_111_ordinal_not_in_range128.html)
# Istruzione di debug
# sys.getdefaultencoding()
reload(sys);
sys.setdefaultencoding("utf8")
matchme = 'meta content="(.*)" name="csrf-token" /' 
csrf = re.search(matchme, str(r1.text))

# Istruzione di debug
# print csrf.group(1)
# payload = {'expert[email]': 'wladimiro.carapucci@gmail.com', 'expert[password]': '3Xpert_Tr3', 'expert[remember_me]': '0', 'expert[terms_of_service]': '1', 'authenticity_token' : csrf.group(1), '_session_id': r1.cookies["_session_id"]}
payload = {'expert[email]': 'wladimiro.carapucci@gmail.com', 'expert[password]': '3Xpert_Tr3', 'expert[remember_me]': '0', 'expert[terms_of_service]': '1', 'authenticity_token' : csrf.group(1)}

r2 = s.post(url_sign_in, data = payload, verify = False)
logging.info('POST for sign_in page')

# Istruzione di debug
# print r2.content


# ==========================================================================
# 3 HANDLER FOR LE TUE DOMANDE
# ==========================================================================
to = 'wladimiro.carapucci@gmail.com'

gmail_user = 'carapucci.bimby@gmail.com'
gmail_pwd = 'bimbymio'
domanda_ok = 'ecco la tua domanda!'
domanda_ko = 'non ci sono domande per te'
matchme2 = '@Wladimiro Carapucci, (.*)</h1><div class="switcher'


while 1:
    # Ritardo casuale in un intervallo espresso in secondi
    sleep(randint(60,120))
    logging.info(datetime.datetime.now())

    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465)
    smtpserver.ehlo()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)

    r1 = s.get(url_expert_home, verify = False, headers = {'User-agent': 'Mozilla/5.0'})    
    domanda_per_te = re.search(matchme2, str(r2.text))


    if domanda_per_te.group(1):
    # la stringa e' stata trovata
        if (domanda_per_te.group(1) == domanda_ok):
        # sendmail con domanda nell'oggetto
            header = 'To: ' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: 3xpert, domanda per te\n'
            msg = header + '\n 3xpert, ecco la domanda per te \n\n'
            smtpserver.sendmail(gmail_user, to, msg)
            logging.info('Mail sent')
        elif (domanda_per_te.group(1) == domanda_ko):
        # incrementare un contatore? e' tutto ok, ma si puo' mandare una e-mail che lo conferma
            header = 'To: ' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: 3xpert, nessuna anomalia \n'
            msg = header + '\n 3xpert, non ci sono ancora domande per te \n\n'
            smtpserver.sendmail(gmail_user, to, msg)
            logging.info('Mail sent')
        else:
        # anomalia; sendmail con oggetto anomalia e body domanda_per_te
            header = 'To: ' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: 3xpert, anomalia \n'
            msg = header + '\n 3xpert, stringa inattesa\n\n'
            smtpserver.sendmail(gmail_user, to, msg)
            logging.info('Mail sent')
    else:
    # anomalia; sendmail con oggetto anomalia e body "Non ho trovato la stringa "
        header = 'To: ' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: 3xpert, anomalia \n'
        msg = header + '\n 3xpert, non ho trovato la stringa\n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        logging.info('Mail sent')

    # print 'done!'
    smtpserver.close()
    logging.info('Mail server disconnected')

