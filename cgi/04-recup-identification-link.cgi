#!/bin/bash

echo -e "Content-type: text/html\n\n"
. /usr/lib/cgi-bin/no-go-back.sh
. /usr/lib/cgi-bin/post.sh

no_go_back_check 4
if [ "$?" -ne "0" ]; then
    exit
fi

# register all GET and POST variables
cgi_getvars BOTH ALL

tpl_result="success"
tpl_title="Setting identification link" 
tpl_text="Good identification link!" 
tpl_time_refresh="1"
tpl_icon="fa-check"
tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
ok=0;

if [ -e "/etc/omb/Identification-configured" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="The identification link was already set."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
fi

#todo check link is an URL 

if [ "$ok" -eq "0" ]; then
    echo $link>/tmp/link
    #we download the target anonymously
    torsocks wget $link -O /home/www-data/cookie >/tmp/download 2>&1
    if [ "$?" -ne "0" ]; then
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="The identification link could not be downloaded."
        tpl_url_refresh="/cgi-bin/03-identification-cookie.cgi"
        ok=1;
    else
        /usr/bin/touch /etc/omb/Identification-configured
    fi
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
page=$( inject_var "$page" ~tpl_active_password "")
page=$( inject_var "$page" ~tpl_active_connectivity "")
page=$( inject_var "$page" ~tpl_active_identification_link "active")
page=$( inject_var "$page" ~tpl_active_domain "")
page=$( inject_var "$page" ~tpl_active_summary "")
page=$( inject_var "$page" ~tpl_active_email_account "")
page=$( inject_var "$page" ~tpl_active_keys "")
page=$( inject_var "$page" ~tpl_active_done "")
echo $page;

########################################################
#			page
########################################################
page=$(cat /var/www/first/recup.html)
page=$( inject_var "$page" ~tpl_result "$tpl_result")
page=$( inject_var "$page" ~tpl_title "$tpl_title")
page=$( inject_var "$page" ~tpl_text "$tpl_text")
page=$( inject_var "$page" ~tpl_url_refresh "$tpl_url_refresh")
page=$( inject_var "$page" ~tpl_time_refresh "$tpl_time_refresh")
page=$( inject_var "$page" ~tpl_icon "$tpl_icon")
echo $page;

########################################################
#			Footer
########################################################
page=$(cat /var/www/first/footer.html)
echo $page;
