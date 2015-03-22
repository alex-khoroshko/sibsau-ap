# установка flightgear
## под Linux (на базе debian)
набрать в консоли `apt-get install flightgear`
скопировать файл fg2comm.xml в папку /usr/share/games/flightgear/Protocol/
fgfs --generic=socket,out,10,localhost,12345,udp,fg2comm