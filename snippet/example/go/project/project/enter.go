package project

import (
	"fmt"
	"os"
	"os/signal"
	"project/project/conf"
	"syscall"

	"github.com/xgfone/go-tools/lifecycle"
	"github.com/xgfone/go-tools/lifecycle/server"
	"github.com/xgfone/go-utils/log"
)

var version = "1.0.0"

// Main the enter of the cmd tracerapi.
func Main() {
	// Parse the configuration
	conf.ParseConfig(version)

	// Initialize the logging
	logger, err := log.NewLogger(conf.Conf.Level, conf.Conf.LogFile)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to initialize logging:", err)
		os.Exit(-1)
	}
	log.SetDefaultLogger(logger)

	go func() {
		ss := make(chan os.Signal, 1)
		signal.Notify(ss, os.Interrupt, syscall.SIGTERM, syscall.SIGQUIT)
		<-ss
		server.Shutdown()
	}()

	// Run for ever
	server.RunForever()
	lifecycle.Stop()
	log.Info("The program exits")
}
