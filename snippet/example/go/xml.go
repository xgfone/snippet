package main

import (
	"encoding/xml"
	"fmt"
	"strings"
)

/*
 * <?xml version="1.0" encoding="UTF-8"?>
 * <resources>
 *     <!-- Comment 1 -->
 *     <string name="VideoLoading">Loading video…</string>
 *     <string name="ApplicationName">what</string>
 * </resources>
 */
var xmls = `<?xml version="1.0" encoding="UTF-8"?> <!-- Comment 1 --> <resources> <string name="VideoLoading">Loading video…</string> <string name="ApplicationName">what</string> </resources>`

func main() {
	buf := strings.NewReader(xmls)
	decoder := xml.NewDecoder(buf)

	for t, err := decoder.Token(); err == nil; t, err = decoder.Token() {
		switch token := t.(type) {
		case xml.StartElement:
			fmt.Printf("StartElement: Name=%s Attr=[", token.Name)
			for _, attr := range token.Attr {
				fmt.Printf("Name=%s Value=%s, ", attr.Name, attr.Value)
			}
			fmt.Printf("]\n")
		case xml.EndElement:
			fmt.Printf("EndElement:   Name: %s\n", token.Name)
		case xml.CharData:
			fmt.Printf("CharData:     %s\n", string(token))
		case xml.Comment:
			fmt.Printf("Comment:      %s\n", string(token))
		case xml.ProcInst:
			fmt.Printf("ProcInst:     Target=%v Inst=%s\n", token.Target, string(token.Inst))
		case xml.Directive:
			fmt.Printf("Directive:    %s\n", string(token))
		default:
			fmt.Printf("Error\n")
		}
	}
	// Output:
	/*
		ProcInst:     Target=xml Inst=version="1.0" encoding="UTF-8"
		CharData:
		Comment:       Comment 1
		CharData:
		StartElement: Name={ resources} Attr=[]
		CharData:
		StartElement: Name={ string} Attr=[Name={ name} Value=VideoLoading, ]
		CharData:     Loading video…
		EndElement:   Name: { string}
		CharData:
		StartElement: Name={ string} Attr=[Name={ name} Value=ApplicationName, ]
		CharData:     what
		EndElement:   Name: { string}
		CharData:
		EndElement:   Name: { resources}
	*/
}
