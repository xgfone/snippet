package main

import (
	"log"

	"github.com/clbanning/mxj"
)

var xmldata = []byte(`
<books>
    <book Order="1">
        <!-- comment1 -->
        book1
        <Author>William H. Gaddis</Author>
        <Title>The Recognitions</Title>
        <Review>One of the great seminal American novels of the 20th century.</Review>
    </book>
    <book Order="2">
        <!-- comment2 -->
        book2
        <Author>Austin Tappan Wright</Author>
        <Title>Islandia</Title>
        <Review>An example of earlier 20th century American utopian fiction.</Review>
    </book>
    <book Order="3">
        <!-- comment3 -->
        book3
        <Author>John Hawkes</Author>
        <Title>The Beetle Leg</Title>
        <Review>A lyrical novel about the construction of Ft. Peck Dam in Montana.</Review>
    </book>
    <book Order="4">
        <!-- comment4 -->
        book3
        <Author>T.E. Porter</Author>
        <Title>King's Day</Title>
        <Review>A magical novella.</Review>
    </book>
</books>
`)

func main() {
	// mxj.CoerceKeysToLower(true)
	// mxj.IncludeTagSeqNum(true)
	mxj.SetAttrPrefix("@")
	m, err := mxj.NewMapXml(xmldata, true)
	if err != nil {
		log.Fatal("err:", err.Error())
	}

	// js, _ := m.Json()
	js, _ := m.JsonIndent("", "    ")
	log.Println(string(js))

	// Output:
	// {
	//     "books": {
	//         "book": [
	//             {
	//                 "#text": "book1",
	//                 "@Order": 1,
	//                 "Author": "William H. Gaddis",
	//                 "Review": "One of the great seminal American novels of the 20th century.",
	//                 "Title": "The Recognitions"
	//             },
	//             {
	//                 "#text": "book2",
	//                 "@Order": 2,
	//                 "Author": "Austin Tappan Wright",
	//                 "Review": "An example of earlier 20th century American utopian fiction.",
	//                 "Title": "Islandia"
	//             },
	//             {
	//                 "#text": "book3",
	//                 "@Order": 3,
	//                 "Author": "John Hawkes",
	//                 "Review": "A lyrical novel about the construction of Ft. Peck Dam in Montana.",
	//                 "Title": "The Beetle Leg"
	//             },
	//             {
	//                 "#text": "book3",
	//                 "@Order": 4,
	//                 "Author": "T.E. Porter",
	//                 "Review": "A magical novella.",
	//                 "Title": "King's Day"
	//             }
	//         ]
	//     }
	// }
}
