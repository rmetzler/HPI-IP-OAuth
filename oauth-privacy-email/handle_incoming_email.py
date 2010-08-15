import logging, email
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util

# copied from http://appengine-cookbook.appspot.com/recipe/forwarding-email/

class ForwardHandler(InboundMailHandler):
    def receive(self, message):

        sender = 'rmetzler80@googlemail.com'    # admin email
        to = 'richard@paadee.com'               # real email

        original = message.original
        forward = mail.EmailMessage(sender=sender,to=to,
                subject='Fwd: ' + message.subject)
        if hasattr(message, 'attachments'):
            forward.attachments = message.attachments
        # Copy the "original" basic headers in the text body
        forward.body = '----- Transferred Message -----\n'
        forward.body += '> From: %s\n' % message.sender
        if isinstance(message.to, list):
            forward.body += '> To: %s\n' % ', '.join(message.to)
        else:
            forward.body += '> To: %s\n' % message.to
        if hasattr(message, 'cc'):
            if isinstance(message.cc, list):
                forward.body += '> CC: %s\n' % ', '.join(message.cc)
            else:
                forward.body += '> CC: %s\n' % message.cc
        forward.body += '> Date: %s\n\n' % message.date
        for part in original.walk():
            if part.get_content_type() == 'text/plain':
                forward.body += '\n'.join('> ' + line for line in part.get_payload(decode=True).split('\n'))
            elif part.get_content_type() == 'text/html':
                html = part.get_payload(decode=True)
                # BUG: this does not work ! why ?
                html.replace('', '----- Transferred Message -----')
                html.replace('', '----- Transferred Message -----')
                html.replace('', '')
                html.replace('', '')
                forward.html = html
        try:
            forward.send()
        except mail.Error, e:
            # this could fail because of attachmnt that are not allowed
            answer = mail.EmailMessage(sender=sender, to=message.sender,
                    subject='Re: ' + message.subject)
            answer.body = 'There was an error when processing your email:\n%s: %s\n\n' % (e.__class__.__name__, e)
            answer.body += '----- Original message below -----\n'
            answer.body += original.as_string()
            answer.send()


def main():
    application = webapp.WSGIApplication([('.+', ForwardHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()