package main

import (
	"flag"
	"fmt"
	"io"
	"net"
	"os"
)

var (
	ip   = flag.String("ip", "127.0.0.1", "ip")
	port = flag.String("port", "80", "port")
	send = flag.Bool("send", false, "Send the data to the server")
)

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

func main() {
	flag.Parse()
	addr := net.JoinHostPort(*ip, *port)
	fmt.Printf("Addr[%v] Send[%v]\n", addr, *send)
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	tcp, _ := conn.(*net.TCPConn)
	if *send {
		sender(tcp)
	} else {
		receiver(tcp)
	}
}
