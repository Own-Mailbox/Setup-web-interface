#!/bin/bash

echo -e "Content-type: text/html\n\n"

. /usr/lib/cgi-bin/no-go-back.sh
. /usr/lib/cgi-bin/post.sh

no_go_back_check 1
if [ "$?" -ne "0" ]; then
    exit
fi


# register all POST variables
cgi_getvars POST ALL

tpl_result="success"
tpl_title="Setting administration password" 
tpl_text="The administration password was set!" 
tpl_time_refresh="0"
tpl_icon="fa-check"
tpl_url_refresh="/cgi-bin/02-bis-check-tor.cgi"
ok=0;



password_safe=$(echo "$pass1" | sed -e "s/[!@#\$%^&~*()\"\\\'\(\)\;\/\`\:\<\>]//g")

if [ "$password_safe" != "$pass1" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Passwords contains forbiden characters."
    tpl_url_refresh="/cgi-bin/01-password-admin.cgi"
    ok=1;
fi

#Password did not match
if [ "$pass1" != "$pass2" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Passwords did not match."
    tpl_url_refresh="/cgi-bin/01-password-admin.cgi"
    ok=1;
fi

length=${#password_safe}
if [ "$length" -le "9" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Passwords too short, must be at least 10 characters."
    tpl_url_refresh="/cgi-bin/01-password-admin.cgi"
    ok=1;
fi

length=${#password_safe}
if [ "$length" -gt "64" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Password too long, must not be larger than 64 characters."
    tpl_url_refresh="/cgi-bin/01-password-admin.cgi"
    ok=1;
fi



if [ "$ok" -eq "0" ]; then
    (sudo /usr/lib/cgi-bin/changeRootPasswordOnce.sh "$password_safe")& >&- 2>&-
    if [ "$?" -eq 11 ]; then
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="Could not set the administration password."
        tpl_url_refresh="/cgi-bin/01-password-admin.cgi"
        ok=1;
    fi
fi


if [ "$ok" -eq "0" ]; then
    #Setup tor hidden service
    (sudo /usr/lib/cgi-bin/setup-tor.sh)& >&- 2>&-

    #  Generate self-signed1 ssl key and add https to apache
    (sudo /usr/lib/cgi-bin/make-tls-key.sh) >&- 2>&-
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
page=$( inject_var "$page" ~tpl_active_connectivity "active")
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
 

exec >&-
exec 2>&-
exit 0;
