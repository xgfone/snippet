package snippet

import (
	"container/list"
	"reflect"
	"strings"
	"sync"
)

// Values represents a set of values.
type Values struct {
	sync.Mutex
	values map[string]interface{}
	watchs map[string]*list.List
}

// NewValues returns a new Values.
func NewValues() *Values {
	return &Values{
		values: make(map[string]interface{}),
		watchs: make(map[string]*list.List),
	}
}

// On registers a callback function, which will be called when the value
// named 'name' had been changed.
//
// If name is "", it will watch all the changed values.
//
// If name ends with ".", it will be as the prefix, and watch
// all the changed values which have the prefix.
func (v *Values) On(name string, cb func(name string, value interface{})) {
	v.Lock()
	fs := v.watchs[name]
	if fs == nil {
		fs = list.New()
		v.watchs[name] = fs
	}
	fs.PushBack(cb)
	v.Unlock()
}

// Off is the inverse operation of On.
func (v *Values) Off(name string, cb func(name string, value interface{})) {
	v.Lock()
	fs := v.watchs[name]
	if fs != nil {
		for e := fs.Front(); e != nil; e = e.Next() {
			f := e.Value.(func(string, interface{}))
			if reflect.ValueOf(f).Pointer() == reflect.ValueOf(cb).Pointer() {
				fs.Remove(e)
				if fs.Len() == 0 {
					delete(v.watchs, name)
				}
				break
			}
		}
	}
	v.Unlock()
}

func (v *Values) traverse(ls *list.List, name string, value interface{}) {
	if ls == nil || ls.Len() == 0 {
		return
	}

	for e := ls.Front(); e != nil; e = e.Next() {
		e.Value.(func(string, interface{}))(name, value)
	}
}

// Set sets the name to the value.
func (v *Values) Set(name string, value interface{}) {
	v.Lock()
	defer v.Unlock()

	v.values[name] = value
	for n, ls := range v.watchs {
		if n == "" {
			v.traverse(ls, name, value)
		} else if strings.HasSuffix(n, ".") {
			if n[:len(n)-1] == name {
				v.traverse(ls, name, value)
			}
		} else if n == name {
			v.traverse(ls, name, value)
		}
	}
}

// Get returns the value of name.
//
// Return nil if the name does not exist.
func (v *Values) Get(name string) (value interface{}) {
	v.Lock()
	value = v.values[name]
	v.Unlock()
	return
}

// Bool is the same as Get, but the value is asserted as bool.
func (v *Values) Bool(name string) bool {
	return v.Get(name).(bool)
}

// String is the same as Get, but the value is asserted as string.
func (v *Values) String(name string) string {
	return v.Get(name).(string)
}

// Bytes is the same as Get, but the value is asserted as []byte.
func (v *Values) Bytes(name string) []byte {
	return v.Get(name).([]byte)
}

// Int is the same as Get, but the value is asserted as int.
func (v *Values) Int(name string) int {
	return v.Get(name).(int)
}

// Int8 is the same as Get, but the value is asserted as int8.
func (v *Values) Int8(name string) int8 {
	return v.Get(name).(int8)
}

// Int16 is the same as Get, but the value is asserted as int16.
func (v *Values) Int16(name string) int16 {
	return v.Get(name).(int16)
}

// Int32 is the same as Get, but the value is asserted as int32.
func (v *Values) Int32(name string) int32 {
	return v.Get(name).(int32)
}

// Int64 is the same as Get, but the value is asserted as int64.
func (v *Values) Int64(name string) int64 {
	return v.Get(name).(int64)
}

// Uint is the same as Get, but the value is asserted as uint.
func (v *Values) Uint(name string) uint {
	return v.Get(name).(uint)
}

// Uint8 is the same as Get, but the value is asserted as uint8.
func (v *Values) Uint8(name string) uint8 {
	return v.Get(name).(uint8)
}

// Uint16 is the same as Get, but the value is asserted as uint16.
func (v *Values) Uint16(name string) uint16 {
	return v.Get(name).(uint16)
}

// Uint32 is the same as Get, but the value is asserted as uint32.
func (v *Values) Uint32(name string) uint32 {
	return v.Get(name).(uint32)
}

// Uint64 is the same as Get, but the value is asserted as uint64.
func (v *Values) Uint64(name string) uint64 {
	return v.Get(name).(uint64)
}

// Float32 is the same as Get, but the value is asserted as float32.
func (v *Values) Float32(name string) float32 {
	return v.Get(name).(float32)
}

// Float64 is the same as Get, but the value is asserted as float64.
func (v *Values) Float64(name string) float64 {
	return v.Get(name).(float64)
}
