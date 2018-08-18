all:
	cp etc/sudoers-temporary /etc/sudoers
	mkdir -p /var/www/first/
	mkdir -p /var/www/first/files/
	cp -r images /var/www/first/files/images
	cp html/* /var/www/first/
	cp html/index-root-init.html /var/www/index.html
	chown www-data /var/www/index.html
	chown -R www-data /var/www/first
	cp cgi/* /usr/lib/cgi-bin/	
	cp etc/sudoers-final /usr/lib/cgi-bin/
	cp etc/gpgscript /usr/lib/cgi-bin/
	cp scripts/setup-gnupg.sh /usr/lib/cgi-bin/
	cp scripts/setup-tor.sh /usr/lib/cgi-bin/
	cp scripts/make-tls-key.sh /usr/lib/cgi-bin/
	cp scripts/changeRootPasswordOnce.sh /usr/lib/cgi-bin/
	cp scripts/configPostfixMailpileGPG.sh /usr/lib/cgi-bin/	
	cp scripts/getTorHostname.sh /usr/lib/cgi-bin/	
	cp scripts/revokeSudoers.sh /usr/lib/cgi-bin/		
	cp scripts/certbot.sh /usr/lib/cgi-bin/
	cp scripts/no-go-back.sh /usr/lib/cgi-bin/	
	cp config.sh /usr/lib/cgi-bin/omb-config.sh	
	chown www-data /usr/lib/cgi-bin/*.cgi
	chmod +x /usr/lib/cgi-bin/*
	cp -r lib/ /var/www/
	touch /etc/setup-step
	chown www-data /etc/setup-step

