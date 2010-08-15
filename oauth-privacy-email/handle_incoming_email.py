import logging, email
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app

class ForwardMailHandler(InboundMailHandler):
    """
    receive emailsf
    check if they are valid
    forward them to the real address
    """
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender + " to: " + mail_message.to)
        mail.send_mail(sender= mail_message.sender,
                      to="richard@paadee.com", # TODO: fetch real address
                      subject=mail_message.subject,
                      body=mail_message.bodies('text/html'))
