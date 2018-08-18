#!/bin/bash

echo -e "Content-Type: text/html\n\n"
echo -e ""
. /usr/lib/cgi-bin/no-go-back.sh

no_go_back_check_set 10
if [ "$?" -ne "0" ]; then
    exit
fi

ps -ae | grep gpg > /dev/null 2>&1
gpgstate=$?;

certbot=$(cat /tmp/certbot-res)

if [ "$certbot" = "OK" ]; then
 tpl_lets_color="green"
 tpl_text_lets="OK" 
else
 tpl_lets_color="red"
 tpl_text_lets="Failed"
fi

if [ "$gpgstate" -eq "0" ]; then
 tpl_redirect="20; url=10-final.cgi"
 tpl_gpg_color="orange"
 tpl_text_gpg="<i class=\"fa fa-rotate-right fa-spin\"></i> Generating" 
else
 tpl_gpg_color="green"
 tpl_text_gpg="OK"
 tpl_redirect="5; url=11-final-real.cgi" 
 cp /var/www/first/index-final.html /var/www/first/index.html
 #For security reasons
for FILE in /usr/lib/cgi-bin/*
do
  if [ "${FILE}" != "/usr/lib/cgi-bin/10-final.cgi" ]&& [ "${FILE}" != "/usr/lib/cgi-bin/11-final-real.cgi" ]; then
      echo '#!/bin/true'>"${FILE}"
  fi
done
 rm /var/www/first/0*.html
 cp /var/www/first/index-root-final.html /var/www/index.html
fi

tpl_gpglogs=$(cat /tmp/resgpg )
tpl_gpglogs=${tpl_gpglogs//$'\n'/\\\&\\\#010;}


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
page=$( inject_var "$page" ~tpl_active_summary "")
page=$( inject_var "$page" ~tpl_active_email_account "")
page=$( inject_var "$page" ~tpl_active_keys "active")
page=$( inject_var "$page" ~tpl_active_done "")
echo $page;

########################################################
#			page
########################################################
page=$(cat /var/www/first/10-final.html)
page=$( inject_var "$page" ~tpl_gpglogs "$tpl_gpglogs")
page=$( inject_var "$page" ~tpl_gpg_color "$tpl_gpg_color")
page=$( inject_var "$page" ~tpl_text_gpg "$tpl_text_gpg")
page=$( inject_var "$page" ~tpl_lets_color "$tpl_lets_color")
page=$( inject_var "$page" ~tpl_text_lets "$tpl_text_lets")
page=$( inject_var "$page" ~tpl_redirect "$tpl_redirect")
echo $page;


########################################################
#			Footer
########################################################
page=$(cat /var/www/first/footer.html)
echo $page;
 


