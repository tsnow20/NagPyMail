# Nagpymail
## About
A simple python script intended for use with Nagios (i.e. notify-by-email). It was written to bypass older
legacy mail applications having issues with TLS/SSL, with no alternatives available.
## Install
Pretty simple--Put it in an appropriate directory, such as /usr/local/bin, mark as executable, and you're done. 
## Usage
    usage: nagpymail.py [-h] [-T] -d TO_ADDRESS -f FROM_ADDRESS -u USER_NAME -p
                        USER_PASS -s SERVER_ADDRESS -t MESSAGE_SUBJECT -m
                        MESSAGE_BODY
    
    optional arguments:
      -h, --help          show this help message and exit
      -T                  Enable TLS
    
    required arguments:
      -d TO_ADDRESS       Destination address
      -f FROM_ADDRESS     From address
      -u USER_NAME        Username to be used for mail server login
      -p USER_PASS        User password to be used with mail server username
      -s SERVER_ADDRESS   Mail server address (can use host:port format to define
                          port settings; default port 587)
      -t MESSAGE_SUBJECT  E-mail message subject line
      -m MESSAGE_BODY     E-mail message body
## Usage in Nagios
As an example, here is the original notify-host-by-email command definition.

    define command{
	command_name	notify-host-by-email
	command_line	/usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\nHost: $HOSTNAME$\nState: $HOSTSTATE$\nAddress: $HOSTADDRESS$\nInfo: $HOSTOUTPUT$\n\nDate/Time: $LONGDATETIME$\n" | /bin/mail -s "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" $CONTACTEMAIL$
    }

Switching to nagpymail is done by changing the **command_line** option to the following:

    command_line 	/usr/local/bin/nagpymail.py -s $USER7$ -u $USER9$ -p $USER10$ -d $CONTACTEMAIL$ -f $USER5$ -t "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" -m "***** Nagios *****<br>Notification Type: $NOTIFICATIONTYPE$ <br>Host: $HOSTNAME$ <br>State: $HOSTSTATE$ <br>Address: $HOSTADDRESS$ <br>Info: $HOSTOUTPUT$ <br>Date/Time: $LONGDATETIME$" &> /var/log/nagpymail.log

In the above example, you would also need to define the $USER[7-10]$ variables in your resources.cfg file under the
Nagios configuration directory, like so:

    $USER7$=smtp.foobar.com
    $USER9$=nagios@foobar.com
    $USER10$=f00b4r
