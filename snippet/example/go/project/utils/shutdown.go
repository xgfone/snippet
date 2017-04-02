package utils

var shouldShutdown = make(chan bool, 1)

// RunForever runs for ever.
func RunForever() {
	<-shouldShutdown
}

// Shutdown shutdowns the server gracefully.
func Shutdown() {
	shouldShutdown <- true
}
