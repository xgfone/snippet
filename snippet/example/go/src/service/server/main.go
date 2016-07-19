package main

import (
	"bytes"
	"fmt"
	"io"
	"net"
	"time"

	"github.com/xgfone/argparse"
	"github.com/xgfone/go-tools/net/server"
	"github.com/xgfone/go-tools/tbucket"
)

type Default struct {
	Ip      string `default:"0.0.0.0" help:"The ip to listen to"`
	Port    string `default:"8000" help:"The port to listen to"`
	Single  bool   `name:"tcp_single" help:"Enable the one way to send or receive the date"`
	Send    bool   `name:"tcp_send" help:"If true, send the data to the client"`
	Rsize   int    `default:"8192" help:"The size of the buffer to receive the data from the client"`
	Ssize   int    `default:"1024" help:"The size of the sent data"`
	Verbose bool   `help:"Output the verbose information"`
	Rate    uint   `help:"The rate to send the data, Mbit/s" validate:"validate_num_range" min:"0" max:"1000"`
	End     bool   `strategy:"skip"`
	Addr    string `strategy:"skip"`
	IsIPv4  bool   `strategy:"skip"`

	TB *tbucket.TokenBucket `strategy:"skip"`
}

func (d Default) Debug(format string, args ...interface{}) {
	if d.Verbose {
		d.Error(format, args...)
	}
}

func (d Default) Error(format string, args ...interface{}) {
	f := fmt.Sprintf("[Server] %v\n", format)
	fmt.Printf(f, args...)
}

var (
	args = Default{}
)

func setData(num int, b byte) []byte {
	data := make([]byte, num)
	for i := 0; i < num; i++ {
		data[i] = b
	}
	return data
}

type TCPHandler struct {
}

func (t TCPHandler) Handle(conn *net.TCPConn) {
	if !args.Single { // Send and Receive
		t.PingPong(conn)
	} else if args.Send { // Send only
		t.sender(conn)
	} else { // Receive only
		t.receiver(conn)
	}
}

func (t TCPHandler) PingPong(conn *net.TCPConn) {
	buf := make([]byte, args.Rsize)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				args.Error("Connection broke off")
				return
			}
			args.Error("%v", err)
		} else {
			args.Debug("Receive %v bytes", n)
			if n, err := conn.Write(buf[:n]); err != nil {
				args.Error("Failed to send the data to the client: %v", err)
			} else {
				args.Debug("Send %v bytes", n)
			}
		}
	}
}

// Send the data in a certain rate.
func (t TCPHandler) sendData(conn *net.TCPConn, data []byte) (int, error) {
	if args.TB != nil {
		args.TB.Get()
	}
	if n, err := conn.Write(data); err != nil {
		return 0, err
	} else {
		return n, nil
	}
}

func (t TCPHandler) sender(conn *net.TCPConn) {
	data := setData(args.Ssize, 'a')
	for {
		if n, err := t.sendData(conn, data); err != nil {
			args.Error("TCP Sender: ", err)
			return
		} else {
			args.Debug("Send %v bytes", n)
		}
	}
}

func (t TCPHandler) receiver(conn *net.TCPConn) {
	buf := make([]byte, args.Rsize)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				args.Error("Connection broke off")
				return
			}
			args.Error("%v", err)
		} else {
			args.Debug("Receive %v bytes", n)
		}
	}
}

func (t TCPHandler) Start() {
	info()
	go fmt.Println(server.TCPServerForever("tcp4", args.Addr, 0, t))
	for !args.End {
		time.Sleep(time.Second)
	}
}

func info() {
	buf := bytes.NewBufferString("[Debug] Enable ")
	buf.WriteString(fmt.Sprintf("TCP, Addr[%v], ", args.Addr))
	if args.Single {
		if args.Send {
			s := fmt.Sprintf("One-Way to send, data size to send[%v]", args.Ssize)
			buf.WriteString(s)
		} else {
			buf.WriteString("One-Way to receive")
		}
	} else {
		s := fmt.Sprintf("Two-Way to send and receive, data size to send[%v]", args.Ssize)
		buf.WriteString(s)
	}
	fmt.Println(buf.String())
}

func main() {
	parser := argparse.NewParser()
	parser.Register(&args)
	parser.Parse(nil)

	if args.Ssize < 64 || args.Ssize > 32768 {
		args.Ssize = 1024
	}

	if args.Rsize < 1024 || args.Rsize > 65535 {
		args.Rsize = 8192
	}

	if args.Rate != 0 {
		rate := args.Rate * 1024 / 8                   // Convert MBit/s to KByte/s
		args.TB = tbucket.NewTokenBucket(uint64(rate)) // 1 token stands for 1KB/s
		args.TB.Start()
	}

	args.Addr = net.JoinHostPort(args.Ip, args.Port)

	fmt.Printf("%+v\n", args)
	server.Debug = true
	//argparse.Debug = true

	tcp := TCPHandler{}
	tcp.Start()
}
