package snippet

import (
	"fmt"
)

func ExamplePortRuleMasking() {
	ports := PortRuleMasking(1000, 1999)
	fmt.Println(ports[:3])
	fmt.Println(ports[3:])
	// fmt.Println(hexFmt(22))

	// Output:
	// [0x03e8/0xfff8 0x03f0/0xfff0 0x0400/0xfe00]
	// [0x0600/0xff00 0x0700/0xff80 0x0780/0xffc0 0x07c0/0xfff0]
}
