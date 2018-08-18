#!/bin/sh

no_go_back_check()
{
tried=$1;
last=$(cat /etc/setup-step)

if [ "$last" = "" ]|| [ "$tried" -ge "$last" ]; then
    return 0;
fi

case $last in
2)
    echo '<meta http-equiv="refresh" content="0; url=02-bis-check-tor.cgi">'
    ;;
5)    
    echo '<meta http-equiv="refresh" content="0; url=05-choose-domain.cgi">'
    ;;    
7)    
    echo '<meta http-equiv="refresh" content="0; url=07-summary.cgi">'
    ;;   
10)    
    echo '<meta http-equiv="refresh" content="0; url=10-final.cgi">'
    ;; 
11)    
    echo '<meta http-equiv="refresh" content="0; url=11-final-real.cgi">'
    ;;        
esac

return 1;
}

no_go_back_check_set()
{
no_go_back_check $1;
res=$?

if [ "$res" -eq "0" ]; then
    echo "$1"> /etc/setup-step
fi

return $res;

}
