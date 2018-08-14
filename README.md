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

install
-----
To install just run the command 

    make
    
It will install files in /var/www/first/ and /usr/lib/cgi-bin/ for cgi scripts, AND it will modify your SUDOERS FILE so that www-data is permitted to do required operations.
