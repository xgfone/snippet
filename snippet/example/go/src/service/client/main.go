package main

import (
	"bytes"
	"fmt"
	"io"
	"net"
	"os"
	"time"

	"github.com/xgfone/argparse"
	"github.com/xgfone/go-tools/tbucket"
)

type Default struct {
	Ip      string `default:"127.0.0.1" help:"The ip to connect to"`
	Port    string `default:"8000" help:"The port to connnect to"`
	Single  bool   `name:"tcp_single" help:"Enable the one way to send or receive the date"`
	Send    bool   `name:"tcp_send" help:"If true, send the data to the server"`
	Rsize   int    `default:"8192" help:"The size of the buffer to receive the data from the client"`
	Ssize   int    `default:"1024" help:"The size of the sent data"`
	Verbose bool   `help:"Output the verbose information"`
	Rate    uint   `help:"The rate to send the data, Mbit/s" validate:"validate_num_range" min:"0" max:"1000"`
	End     bool   `strategy:"skip"`
	Addr    string `strategy:"skip"`

	TB *tbucket.TokenBucket `strategy:"skip"`
}

func (d Default) Debug(format string, args ...interface{}) {
	if d.Verbose {
		d.Error(format, args...)
	}
}

func (d Default) Error(format string, args ...interface{}) {
	f := fmt.Sprintf("[Client] %v\n", format)
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

type TcpClient struct {
}

// Send the data in a certain rate.
func (t TcpClient) sendData(conn *net.TCPConn, data []byte) (int, error) {
	if args.TB != nil {
		args.TB.Get()
	}
	if n, err := conn.Write(data); err != nil {
		return 0, err
	} else {
		return n, nil
	}
}

func (t TcpClient) sender(conn *net.TCPConn) {
	args.Error("Start a goroutine to send the data")

	data := setData(args.Ssize, 'a')
	for !args.End {
		if n, err := t.sendData(conn, data); err != nil {
			args.Error("%v", err)
			args.End = true
			return
		} else {
			args.Debug("Send %v bytes", n)
		}
	}
}

func (t TcpClient) receiver(conn *net.TCPConn) {
	args.Error("Start a goroutine to receive the data")

	buf := make([]byte, args.Rsize)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				args.End = true
				args.Error("Conn broke off")
				return
			}
			args.Error("%v", err)
		} else {
			args.Debug("Receive %v bytes\n", n)
		}
	}
}

func (t TcpClient) Start() {
	conn, err := net.Dial("tcp4", args.Addr)
	if err != nil {
		args.Error("%v", err)
		os.Exit(1)
	}

	tcp := conn.(*net.TCPConn)
	args.Debug("Connect to %v", args.Addr)

	if !args.Single {
		go t.sender(tcp)
		go t.receiver(tcp)
	} else if args.Send {
		go t.sender(tcp)
	} else {
		go t.receiver(tcp)
	}
	for !args.End {
		time.Sleep(time.Second)
	}
}

func info() {
	buf := bytes.NewBufferString("[Debug] Enable ")
	buf.WriteString(fmt.Sprintf("TCP, Addr[%v], ", args.Addr))
	if args.Single {
		if args.Send {
			s := fmt.Sprintf("One-Way to send, data size to send[%v]", args.Rsize)
			buf.WriteString(s)
		} else {
			buf.WriteString("One-Way toreceive")
		}
	} else {
		s := fmt.Sprintf("Two-Way to send and receive, data size to send[%v]", args.Rsize)
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
	info()
	h := TcpClient{}
	h.Start()
}
