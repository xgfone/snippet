package main

import (
	"flag"
	"fmt"
	"io"
	"net"

	"github.com/xgfone/go-tools/net/server"
)

var (
	handler TCPHandler
)

func receiver(conn *net.TCPConn) {
	buf := make([]byte, 8192)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				fmt.Println("Conn broke off")
				return
			}
			fmt.Println(err)
		} else {
			fmt.Printf("Receive %v bytes\n", n)
		}
	}
}

func setData(num int, b byte) []byte {
	data := make([]byte, num)
	for i := 0; i < num; i++ {
		data[i] = b
	}
	return data
}

func sender(conn *net.TCPConn) {
	data := setData(1024, 'a')
	for {
		if n, err := conn.Write(data); err != nil {
			fmt.Println(err)
			return
		} else {
			fmt.Printf("Send %v bytes\n", n)
		}
	}
}

type TCPHandler struct {
	ip   string
	port string
	send bool
}

func (h TCPHandler) Handle(conn *net.TCPConn) {
	if h.send {
		sender(conn)
	} else {
		receiver(conn)
	}
}

func init() {
	flag.StringVar(&handler.ip, "ip", "0.0.0.0", "ip")
	flag.StringVar(&handler.port, "port", "80", "port")
	flag.BoolVar(&handler.send, "send", false, "Send the data to the client")
}

func main() {
	flag.Parse()
	addr := net.JoinHostPort(handler.ip, handler.port)
	fmt.Printf("Addr[%v] Send[%v]\n", addr, handler.send)
	err := server.TCPServerForever("tcp", addr, handler)
	fmt.Println(err)
}
