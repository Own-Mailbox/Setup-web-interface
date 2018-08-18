# Setup-web-interface
Web interface to easily setup an Own-mailbox.

Dependencies
-----
* Tor
* Tor-socks
* sudo
* postfix
* gnupg
* Apache with cgi-bin
* qrencode
* Mailpile (Own-Mailbox version) installed in /home/mailpile/Mailpile directory.
* cs-com (client side).

Configuration
-----

In order to configure the web interface edit config.sh

Install
-----
To install just run the command 

    make
    
It will install files in /var/www/first/ and /usr/lib/cgi-bin/ for cgi scripts, AND it will modify your SUDOERS FILE so that www-data is permitted to do required operations.

Screenshots
-----

![Alt text](screenshot.jpg?raw=true "Screenshot")

License
-----

The code is licensed under GPLv3. The Own-Mailbox name and logo are trademarks, and may not be used for commercial purposes without authorisation.
