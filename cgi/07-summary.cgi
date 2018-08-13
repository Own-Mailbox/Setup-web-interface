#!/bin/bash
echo -e "Content-Type: text/html\n\n"
echo -e ""

tpl_domain=$(cat /home/www-data/domain);
tpl_hiddenservice=$(sudo /usr/lib/cgi-bin/getTorHostname.sh);

#####################################################################
#
#               Generation du html   
#
#####################################################################
inject_var() {
	echo $1 | sed -e "s#$2#$3#g"
}

########################################################
#			page
########################################################
page=$(cat /var/www/html/07-summary.html)
page=$( inject_var "$page" ~tpl_domain "$tpl_domain")
page=$( inject_var "$page" ~tpl_hiddenservice "$tpl_hiddenservice")
echo $page;




