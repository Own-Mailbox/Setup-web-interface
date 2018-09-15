#!/bin/bash

echo -e "Content-type: text/html\n\n"

. /usr/lib/cgi-bin/omb-config.sh
. /usr/lib/cgi-bin/no-go-back.sh
. /usr/lib/cgi-bin/post.sh

no_go_back_check 6
if [ "$?" -ne "0" ]; then
    exit
fi

# register all POST variables
cgi_getvars POST ALL

tpl_result="success"
tpl_title="Choosing domain" 
tpl_text="Domain was set!" 
tpl_time_refresh="1"
tpl_icon="fa-check"
tpl_url_refresh="/cgi-bin/07-summary.cgi"
ok=0;

#si le domaine est déja configuré on va direct au résumé
if [ -e "/etc/omb/Domain-configured" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="The domain was already chosen."
    tpl_url_refresh="/cgi-bin/07-summary.cgi"
    ok=1;
fi

echo "$domain" | egrep -q "^[a-z0-9]*$"
if [ "$?" -ne "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Subdomain must contain only alpha-numeric lower-case characters."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
fi

length=${#domain}
if [ "$length" -le "3" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Subdomain must contain at least 3 characters."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
fi

length=${#domain}
if [ "$length" -gt "32" ]&& [ "$ok" -eq "0" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Subdomain must contain at most 32 characters."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
fi

#Get our tor hidden service hostname
tor_hiddendomain=$(sudo /usr/lib/cgi-bin/getTorHostname.sh)
if [ -z "$tor_hiddendomain" ]; then
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Tor hidden service was misconfigured."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
fi

#If the tor hidden service was not yet communicated to the proxy server
#then we inform the proxy server about it.
if [ ! -e "/etc/omb/Tor-hidden-informed-configured" ]&& [ "$ok" -eq "0" ]; then
  omb-client -c /home/www-data/cookie -t $tor_hiddendomain > /tmp/res1 2>&1
  head -n 1 /tmp/res1 > /tmp/res
  res=$(cat /tmp/res);
  if [ "$res" != "OK" ]; then 
    tpl_icon="fa-times"
    tpl_result="error"
    tpl_time_refresh="5"
    tpl_title="Error"
    tpl_text="Error while informing the proxy server of our tor hidden service. The proxy server replied: $res."
    tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
    ok=1;
  else
    /usr/bin/touch /etc/omb/Tor-hidden-informed-configured
  fi
fi


if [ "$ok" -eq "0" ]; then
omb-client -c /home/www-data/cookie -d $domain > /tmp/res1 2>&1
head -n 1 /tmp/res1 > /tmp/res
res=$(cat /tmp/res);
    if [ "$res" != "OK" ]; then 
        tpl_icon="fa-times"
        tpl_result="error"
        tpl_time_refresh="5"
        tpl_title="Error"
        tpl_text="$res"
        tpl_url_refresh="/cgi-bin/05-choose-domain.cgi"
        ok=1;
    else
        echo "$domain.$MASTER_DOMAIN" > /home/www-data/domain
        sudo /usr/bin/postfix_config_hostname.sh $domain.$MASTER_DOMAIN >/dev/null 2>&1
        /usr/bin/touch /etc/omb/Domain-configured
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
