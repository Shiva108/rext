# Name:Send GET HTTP and print response.
# File:http_ping.py
# Author:Ján Trenčanský
# License: GNU GPL v3
# Created: 27.12.2015
# Last modified: 27.12.2015
# Shodan Dork:
# Description: For those times when you just want dork for shodan but don't want to run Burp

import core.Exploit
import core.io

import requests
import interface.utils
from interface.messages import print_error, print_yellow, print_green, print_help


class Exploit(core.Exploit.RextExploit):
    ssl = False
    body = True

    def __init__(self):
        core.Exploit.RextExploit.__init__(self)

    def do_set(self, e):
        args = e.split(' ')
        try:
            if args[0] == "host":
                if interface.utils.validate_ipv4(args[1]):
                    self.host = args[1]
                else:
                    print_error("please provide valid IPv4 address")
            elif args[0] == "port":
                if str.isdigit(args[1]):
                    self.port = args[1]
                else:
                    print_error("port value must be integer")
            elif args[0] == "ssl":
                if str(args[1]).lower() == "yes":
                    self.ssl = True
                elif str(args[1]).lower() == "no":
                    self.ssl = False
                else:
                    print_error("please use yes/no as parameter")
            elif args[0] == "body":
                if str(args[1]).lower() == "yes":
                    self.body = True
                elif str(args[1]).lower() == "no":
                    self.body = False
                else:
                    print_error("please use yes/no as parameter")
        except IndexError:
            print_error("please specify value for variable")

    def do_body(self, e):
        if self.body is True:
            print("yes")
        else:
            print("no")

    def do_ssl(self, e):
        if self.ssl is True:
            print("yes")
        else:
            print("no")

    def help_body(self):
        print_help("print response body? yes/no")

    def help_ssl(self):
        print_help("use HTTPS? yes/no")

    def do_run(self, e):
        if self.ssl is False:
            url = "http://%s:%s" % (self.host, self.port)
        else:
            url = "https://%s:%s" % (self.host, self.port)
        try:
            print_yellow("Sending GET request")
            response = requests.get(url, timeout=60, verify=False)
            print_green("[%s %s] %s" % (response.status_code, response.reason, response.url))
            for header in response.headers:
                print_green("%s: %s" % (header, response.headers.get(header)))
            if self.body is True:
                print("\n")
                print_green(response.text)
        except requests.ConnectionError as e:
            print_error("connection error %s" % e)
        except requests.Timeout:
            print_error("timeout")
Exploit()
