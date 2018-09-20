#!/bin/bash

echo -e "Content-type: text/html\n\n"
. /usr/lib/cgi-bin/no-go-back.sh
. /usr/lib/cgi-bin/post.sh
no_go_back_check 9

if [ "$?" -ne "0" ]; then
    exit
fi


tpl_result="success"
tpl_title="Configuring email account" 
tpl_text="Your email account is configured!" 
tpl_time_refresh="1"
tpl_icon="fa-check"
tpl_url_refresh="/cgi-bin/10-final.cgi"
ok=0;


# register all POST variables
cgi_getvars POST ALL

#si Mail est déja configuré on va direct au résumé
if [ -e "/etc/omb/Mailpile-configured" ]; then
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="Mailpile already configured."
        tpl_url_refresh="/cgi-bin/10-final.cgi"
        ok=1;
fi

password_safe=$(echo "$pass1" | sed -e "s/[!@#\$%^&~*()\"\\\'\(\)\;\/\`\:\<\>]//g")
if [ "$password_safe" != "$pass1" ]&& [ "$ok" -eq "0" ];  then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Passwords contains forbiden characters."
    tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
    ok=1;
fi

fn_safe=$(echo "$fn" | sed -e "s/[!@#\$%^&~*()\"\\\'\(\)\;\/\`\:\<\>]//g")
if [ "$fn_safe" != "$fn" ]&& [ "$ok" -eq "0" ];  then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Full name contains forbiden characters."
    tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
    ok=1;
fi

user_safe=$(echo "$user" | sed -e "s/[!@#\$%^&~*()\"\\\'\(\)\;\/\`\:\<\>]//g")
if [ "$user_safe" != "$user" ]&& [ "$ok" -eq "0" ];  then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="User contains forbiden characters."
    tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
    ok=1;
fi

#Password did not match
if [ "$pass1" != "$pass2" ]&& [ "$ok" -eq "0" ]; then
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="Password did not match."
        tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
        ok=1;
fi

length=${#password_safe}
if [ "$length" -le "9" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Passwords too short, must be at least 10 characters."
    tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
    ok=1;
fi

length=${#password_safe}
if [ "$length" -gt "64" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Password too long, must not be larger than 64 characters."
    tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
    ok=1;
fi

if [ "$user" = "" ]|| [ "$fn" = "" ]|| [ "$pass1" = "" ] ; then
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="One field was empty."
        tpl_url_refresh="/cgi-bin/08-setup-email-acount.cgi"
        ok=1;
fi



if [ "$ok" -eq "0" ]; then
domain=$(cat /home/www-data/domain)
echo "$user@$domain">/home/www-data/mail
echo "$fn">/home/www-data/fn
unset HISTFILE

sudo /usr/lib/cgi-bin/configPostfixMailpileGPG.sh "$user_safe" "$domain" "$password_safe" "$fn_safe"  >/dev/null 2>&1

unset HISTFILE
#For security reasons
sudo /usr/lib/cgi-bin/revokeSudoers.sh
/usr/bin/touch /etc/omb/Mailpile-configured

    #If we have an error because too many certificates were issued.
    if [ "$rescertbot" -eq "55" ]; then
        tpl_result="warning"
        tpl_text="Could not get let's encrypt certificate!" 
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
page=$( inject_var "$page" ~tpl_active_identification_link "")
page=$( inject_var "$page" ~tpl_active_domain "")
page=$( inject_var "$page" ~tpl_active_summary "")
page=$( inject_var "$page" ~tpl_active_email_account "active")
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

echo "";
echo "";
exec >&-
exec 2>&-
exit 0;
