package main

import (
	"fmt"
	"net"

	"github.com/xgfone/argparse"
	"github.com/xgfone/go-tools/net/server"
	"github.com/xgfone/go-tools/parse"
)

type Default struct {
	Proto string `default:"tcp" help:"The name of the protocol, such as tcp, tcp4, tcp6, udp, udp4, or udp6, etc." validate:"validate_str_array" array:"tcp,tcp4,tcp6,udp,udp4,udp6"`
	Ip    string `default:"0.0.0.0" help:"The IP to listen to." validate:"validate_ip"`
	Port  int    `default:"80" help:"The port to listen to." validate:"validate_num_range" min:"1" max:"65535"`
}

var (
	conf Default
)

func tcp(conn *net.TCPConn) {
	addr := conn.RemoteAddr()
	fmt.Printf("Receives an connection: %v\n", addr)

	buf := make([]byte, 1024)
	for {
		if n, err := conn.Read(buf); err != nil {
			if err.Error() == "EOF" {
				fmt.Printf("The connection [%v] close\n", addr)
			} else {
				fmt.Println(err)
			}

			break
		} else {
			fmt.Printf("Receive the data from %v: %v\n", addr, buf[:n])
		}
	}
}

func udp(buf []byte, addr *net.UDPAddr) []byte {
	fmt.Printf("Receive the data from %v: %v\n", addr, buf)
	return nil
}

func main() {
	parser := argparse.NewParser()
	parser.Register(&conf)
	parser.Parse(nil)

	var err error
	ipport := net.JoinHostPort(conf.Ip, parse.String(conf.Port))

	if conf.Proto == "tcp" || conf.Proto == "tcp4" || conf.Proto == "tcp6" {
		err = server.TCPServerForever(conf.Proto, ipport, 0, tcp)
	} else if conf.Proto == "udp" || conf.Proto == "udp4" || conf.Proto == "udp6" {
		err = server.UDPServerForever(conf.Proto, ipport, 8192, udp, nil)
	} else {
		fmt.Printf("Don't support the protocol: %v\n", conf.Proto)
	}

	if err != nil {
		fmt.Println(err)
	}
}
