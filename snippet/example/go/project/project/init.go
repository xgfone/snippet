package project

import "github.com/xgfone/go-utils/log"

// Start starts parse the configuration, initializing, and start the app.
func Start(version string) (err error) {
	// 1. Parse the configuration
	ParseConfig(version)

	// 2. Initialize the logging
	logger, err := log.NewLogger(Conf.Level, Conf.LogFile)
	if err != nil {
		return
	}
	log.SetDefaultLogger(logger)

	// 3. Initialize others
	// TODO

	// 4. Start the server
	// TODO

	return nil
}
