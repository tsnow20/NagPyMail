#!/usr/bin/python
import argparse
import sys
import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-T", help="Enable TLS", action="store_true", default=False)
        required_args = parser.add_argument_group('required arguments')
        required_args.add_argument("-d", help="Destination address", required=True, action="store", dest="to_address")
        required_args.add_argument("-f", help="From address", required=True, action="store", dest="from_address")
        required_args.add_argument("-u", help="Username to be used for mail server login", required=True,
                                   action="store", dest="user_name")
        required_args.add_argument("-p", help="User password to be used with mail server username", required=True,
                                   action="store", dest="user_pass")
        required_args.add_argument("-s", help="Mail server address", required=True, action="store",
                                   dest="server_address")
        required_args.add_argument("-t", help="E-mail message subject line", required=True, action="store",
                                   dest="message_subject")
        required_args.add_argument("-m", help="E-mail message body", required=True, action="store", dest="message_body")
    except argparse.ArgumentError as err:
        print str(err)
        sys.exit(2)

    args = parser.parse_args()
    to_address = args.to_address
    from_address = args.from_address
    user_name = args.user_name
    user_pass = args.user_pass
    server_address = args.server_address
    message_subject = args.message_subject
    enable_tls = args.T
    message_body = args.message_body

    # Message body uses HTML, will change options to allow for plaintext at later point.
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


if __name__ == "__main__":
    main()
