#!/bin/bash

echo -e "Content-Type: text/html\n\n"
echo -e ""

. /usr/lib/cgi-bin/omb-config.sh
. /usr/lib/cgi-bin/no-go-back.sh

no_go_back_check_set 2
if [ "$?" -ne "0" ]; then
    exit
fi


attempt=$(cat /tmp/attempt_www)
if [ "$attempt" = "" ]; then
    attempt="1";
    echo "$attempt"> /tmp/attempt_www
    tpl_redirect="0";
    tpl_hidden_color="orange" 
    tpl_torproxy_color="orange"  
    tpl_text_torproxy="Not yet" 
    tpl_text_hidden="Not yet"        
else
    attempt=$((attempt+1))
    echo "$attempt"> /tmp/attempt_www

    #check that we can reach the proxy server
    torsocks wget --timeout $((attempt)) http://$FQDN/OK -O /tmp/ok_www > /dev/null 2>&1
    res_wget=$?;

    #Get hostname
    hostname=$(sudo /usr/lib/cgi-bin/getTorHostname.sh);
    res_cat=$?;

    #Trying to reach ourselves just to make sure that our tor hidden service is accessible.
    torsocks wget --timeout=$((attempt)) http://$hostname/OK -O /tmp/wget-ok-init >/tmp/wget-tor-init-res 2>&1
    local_ok=$(cat /tmp/wget-ok-init)

    if [ "$res_wget" -eq "0" ]; then
        tpl_torproxy_color="green"
        tpl_text_torproxy="OK"        
    else
        tpl_torproxy_color="orange"
        tpl_text_torproxy="Not yet"
    fi
    
    if  [ "$res_cat" -eq "0" ] && [ "$hostname" != "" ] && [ "$local_ok" = "OK" ]; then
        tpl_hidden_color="green"
        tpl_text_hidden="OK"        
    else
        tpl_hidden_color="orange"
        tpl_text_hidden="Not yet"
    fi
    
    #Si toutes les phase de connection se sont bien passées.
     if [ "$res_wget" -eq "0" ] && [ "$res_cat" -eq "0" ] && [ "$hostname" != "" ] && [ "$local_ok" = "OK" ]; then
         tpl_redirect="4; url=03-identification-cookie.cgi"
     else
         tpl_redirect="1";
     fi
fi

tpl_torlog=$(cat /var/log/tor.log)
tpl_torlog=${tpl_torlog//$'\n'/\\\&\\\#010;}

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
page=$(cat /var/www/first/02-bis-check-tor.html)
page=$( inject_var "$page" ~tpl_torlog "$tpl_torlog")
page=$( inject_var "$page" ~tpl_torproxy_color "$tpl_torproxy_color")
page=$( inject_var "$page" ~tpl_hidden_color  "$tpl_hidden_color" )
page=$( inject_var "$page" ~tpl_redirect  "$tpl_redirect" )
page=$( inject_var "$page" ~tpl_text_torproxy  "$tpl_text_torproxy" )
page=$( inject_var "$page" ~tpl_text_hidden  "$tpl_text_hidden" )
echo $page;

########################################################
#			Footer
########################################################
page=$(cat /var/www/first/footer.html)
echo $page;
 


