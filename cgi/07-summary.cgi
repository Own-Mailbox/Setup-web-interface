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
#			Header
########################################################
page=$(cat /var/www/first/header.html)
page=$( inject_var "$page" ~tpl_active_welcome "")
page=$( inject_var "$page" ~tpl_active_password "")
page=$( inject_var "$page" ~tpl_active_connectivity "")
page=$( inject_var "$page" ~tpl_active_identification_link "")
page=$( inject_var "$page" ~tpl_active_domain "")
page=$( inject_var "$page" ~tpl_active_summary "active")
page=$( inject_var "$page" ~tpl_active_email_account "")
page=$( inject_var "$page" ~tpl_active_keys "")
page=$( inject_var "$page" ~tpl_active_done "")
echo $page;

########################################################
#			page
########################################################
page=$(cat /var/www/first/07-summary.html)
page=$( inject_var "$page" ~tpl_domain "$tpl_domain")
page=$( inject_var "$page" ~tpl_hiddenservice "$tpl_hiddenservice")
echo $page;

########################################################
#			Footer
########################################################
page=$(cat /var/www/first/footer.html)
echo $page;
 



