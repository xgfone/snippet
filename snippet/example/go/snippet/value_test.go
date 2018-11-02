package snippet

import "fmt"

func ExampleValues() {
	vs := NewValues()
	vs.Set("name", 123)
	value := vs.Get("name")

	fmt.Println(value)

	// Output:
	// 123
}

func ExampleValues_On() {
	vs := NewValues()
	vs.On("", func(n string, v interface{}) { fmt.Println("all", n, v) })
	vs.On("n1", func(n string, v interface{}) { fmt.Println("name1", n, v) })
	vs.On("n2", func(n string, v interface{}) { fmt.Println("name2", n, v) })
	vs.Set("n1", 123)

	// Output:
	// all n1 123
	// name1 n1 123
}

func ExampleValues_Off() {
	vs := NewValues()

	cb := func(n string, v interface{}) { fmt.Println("on1", n, v) }
	vs.On("", func(n string, v interface{}) { fmt.Println("all", n, v) })
	vs.On("n1", cb)
	vs.On("n2", func(n string, v interface{}) { fmt.Println("on2", n, v) })
	vs.Set("n1", 123)
	vs.Off("n1", cb)
	vs.Set("n1", 456)

	// Output:
	// all n1 123
	// on1 n1 123
	// all n1 456
}
