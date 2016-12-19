package main

import (
	"fmt"
	"project/project"
)

var version = "1.0.0"

func main() {
	if err := project.Start(version); err != nil {
		fmt.Println(err)
	}
}
