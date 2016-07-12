package main

import (
	"fmt"
	"io"
	"net"

	"github.com/xgfone/go-tools/net/server"
)

func handle(conn *net.TCPConn) {
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				fmt.Println("Conn broke off")
				return
			}
			fmt.Println(err)
		} else {
			fmt.Printf("Receive %v bytes: %v\n", n, string(buf[:n]))
		}
	}
}

func main() {
	err := server.TCPServerForever("tcp", ":8000", handle)
	fmt.Println(err)
}
