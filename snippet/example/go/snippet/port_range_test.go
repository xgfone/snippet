package snippet

import (
	"fmt"
)

func ExamplePortRuleMasking() {
	ports := PortRuleMasking(1000, 1999)
	fmt.Println(len(ports))
	fmt.Println(ports[0])
	fmt.Println(ports[1])
	fmt.Println(ports[2])
	fmt.Println(ports[3])
	fmt.Println(ports[4])
	fmt.Println(ports[5])
	fmt.Println(ports[6])

	// Unordered output:
	// 7
	// 0x03e8/0xfff8
	// 0x03f0/0xfff0
	// 0x0400/0xfe00
	// 0x0600/0xff00
	// 0x0700/0xff80
	// 0x0780/0xffc0
	// 0x07c0/0xfff0
}
