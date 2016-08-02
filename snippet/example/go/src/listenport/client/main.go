package main

import (
	"fmt"
	"net"

	"github.com/xgfone/argparse"
	"github.com/xgfone/go-tools/parse"
)

type Default struct {
	Proto string `default:"tcp" help:"The name of the protocol, such as tcp, tcp4, tcp6, udp, udp4, or udp6, etc." validate:"validate_str_array" array:"tcp,tcp4,tcp6,udp,udp4,udp6"`
	Ip    string `default:"127.0.0.1" help:"The IP to listen to." validate:"validate_ip"`
	Port  int    `default:"80" help:"The port to listen to." validate:"validate_num_range" min:"1" max:"65535"`
}

var conf Default

func udp(proto, ipport string) {
	if _conn, err := net.Dial(proto, ipport); err != nil {
		fmt.Println(err)
		return
	} else {
		conn := _conn.(*net.UDPConn)
		defer conn.Close()
		buf := []byte("test")
		conn.Write(buf)
		//conn.WriteToUDP(buf, addr)
	}
}

func tcp(proto, ipport string) {
	if _conn, err := net.Dial(proto, ipport); err != nil {
		fmt.Println(err)
		return
	} else {
		conn := _conn.(*net.TCPConn)
		defer conn.Close()
		buf := []byte("test")
		conn.Write(buf)
	}
}

func main() {
	parser := argparse.NewParser()
	parser.Register(&conf)
	parser.Parse(nil)

	ipport := net.JoinHostPort(conf.Ip, parse.String(conf.Port))
	if conf.Proto == "tcp" || conf.Proto == "tcp4" || conf.Proto == "tcp6" {
		tcp(conf.Proto, ipport)
	} else if conf.Proto == "udp" || conf.Proto == "udp4" || conf.Proto == "udp6" {
		udp(conf.Proto, ipport)
	} else {
		fmt.Printf("Don't support the protocol: %v\n", conf.Proto)
	}
}
