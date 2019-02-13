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

    # Message body uses HTML, will change options to allow for plaintext at later point.
    msg = MIMEText(args.message_body, 'html')
    msg['Subject'] = args.message_subject
    msg['From'] = args.from_address
    msg['To'] = args.to_address
    # We must set date timestamp, otherwise mail server/mail client may assume its own timestamp.
    msg['Date'] = formatdate(localtime=True)
    s = smtplib.SMTP(args.server_address, 587)
    # check if TLS enabled by -T
    if args.T:
        s.starttls()
    s.login(user=args.user_name, password=args.user_pass)
    s.sendmail(args.from_address, args.to_address, msg.as_string())


if __name__ == "__main__":
    main()
