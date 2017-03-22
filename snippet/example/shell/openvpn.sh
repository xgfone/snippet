CONFIG_PATH=~/bin/openvpn/config/group
PASSWD_FILE=~/bin/openvpn/pass.txt
NAME=biggeryun
VPN_IP=127.0.0.1
VPN_PORT=1194

sudo openvpn \
--client \
--dev tun \
--proto tcp \
--daemon ${NAME} \
--remote ${VPN_IP} ${VPN_PORT} \
--resolv-retry infinite \
--nobind \
--persist-key \
--persist-tun \
--ca ${CONFIG_PATH}/ca.crt \
--tls-auth ${CONFIG_PATH}/ta.key 1 \
--auth-user-pass ${PASSWD_FILE} \
--comp-lzo \
--verb 5

ps aux | grep "openvpn" | grep "$NAME" | grep -v "grep" >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "Failed to connect to openvpn[$NAME]"
else
	echo "Connect to openvpn[$NAME] successfully"
fi
