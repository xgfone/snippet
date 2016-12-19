package project

import (
	"fmt"
	"os"

	flags "github.com/jessevdk/go-flags"
)

// Config is the type of the global configuration.
type Config struct {
	Version bool   `short:"v" long:"version" description:"Print the version information"`
	Workers int    `short:"w" long:"workers" value-name:"WORKERS" default:"" description:"The number of CPU to use"`
	Level   string `short:"l" long:"level" value-name:"LEVEL" default:"debug" description:"The level of the logging"`
	LogFile string `short:"f" long:"logfile" value-name:"LOGFILE" default:"/log/project/asg.log" description:"The path of the logging file"`

	// ...
}

// Conf is the global configuration option.
var Conf = Config{}

// ParseConfig parses the configuration.
func ParseConfig(version string) {
	if _, err := flags.Parse(&Conf); err != nil {
		if err.(*flags.Error).Type == flags.ErrTag {
			fmt.Println(err)
		}
		os.Exit(1)
	}

	if Conf.Version && len(version) > 0 {
		fmt.Printf("Version: %v\n", version)
		os.Exit(0)
	}

	// TODO ...
}
