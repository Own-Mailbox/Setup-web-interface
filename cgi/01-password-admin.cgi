#!/bin/bash
echo -e "Content-Type: text/html\n\n"
echo -e ""

. /usr/lib/cgi-bin/no-go-back.sh

no_go_back_check 1
if [ "$?" -ne "0" ]; then
    exit
fi

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
page=$( inject_var "$page" ~tpl_active_password "active")
page=$( inject_var "$page" ~tpl_active_connectivity "")
page=$( inject_var "$page" ~tpl_active_identification_link "")
page=$( inject_var "$page" ~tpl_active_domain "")
page=$( inject_var "$page" ~tpl_active_summary "")
page=$( inject_var "$page" ~tpl_active_email_account "")
page=$( inject_var "$page" ~tpl_active_keys "")
page=$( inject_var "$page" ~tpl_active_done "")
echo $page;

########################################################
#			page
########################################################
page=$(cat /var/www/first/01-password-admin.html)
echo $page;

########################################################
#			Footer
########################################################
page=$(cat /var/www/first/footer.html)
echo $page;
 
