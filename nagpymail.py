#!/usr/bin/python
import getopt
import sys
import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText


def usage():
    print "This is a very simple drop in python replacement for mail utilities commonly used with Nagios."
    print "Usage: nagpymail.py -d sendto@foobar.com -f from@foobar.com -u mailuser -p mailpass -s serveraddress " \
          "-t messagesubject -m messagebody"
    print "Options:"
    print "-d       Destination Address (Required)"
    print "-f       From address (Required)"
    print "-u       E-mail username (Required)"
    print "-p       E-mail user password (Required)"
    print "-s       Mail server address (Required)"
    print "-t       Message subject (Required)"
    print "-T       Enable TLS (Optional; default: disabled)"
    print "-m       Message body (Required)"


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:m:p:s:t:Tu:")
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    enable_tls = False

    for o, a in opts:
        if o == "-d":
            to_address = a
        elif o == "-f":
            from_address = a
        elif o == "-u":
            user_name = a
        elif o == "-m":
            message_body = a
        elif o == "-p":
            user_pass = a
        elif o == "-s":
            server_address = a
        elif o == "-t":
            message_subject = a
        elif o == "-T":
            enable_tls = True
        else:
            assert False, "Unhandled option " + o

    # Message body uses HTML, will change options to allow for plaintext at later point.
    try:
        msg = MIMEText(message_body, 'html')
        msg['Subject'] = message_subject
        msg['From'] = from_address
        msg['To'] = to_address
        # We must set date timestamp, otherwise mail server/mail client may assume its own timestamp.
        msg['Date'] = formatdate(localtime=True)
        s = smtplib.SMTP(server_address, 587)
        if enable_tls:
            s.starttls()
        s.login(user=user_name, password=user_pass)
        s.sendmail(from_address, to_address, msg.as_string())
    except UnboundLocalError as e:
        print "Missing requirement: %s\n" % (e)
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main()
