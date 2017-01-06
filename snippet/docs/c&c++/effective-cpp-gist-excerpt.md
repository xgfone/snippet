
##### 1、除非你想要让构造函数用于隐式类型转换，否则，请把它声明为explicit。——“导读”

##### 2、C++有四部分组成：C、Object-Oriented C++、Template C++、STL。 ——“条款01”
对内置（也就是C-lile）类型而言，pass-by-value通常比pass-by-reference高效，但当你从C part of C++移往Object-Oriented C++，由于用户自定义构造函数和析构函数的存在，pass-by-reference=to-const往往更好。运用Template C++时尤其如此，因为彼时你甚至不知道所处理的对象的类型。然而一旦跨入STL你就会了解，迭代器和函数对象都是在C指针之上塑出来的，所以对STL的 迭代器和函数对象而言，旧式的C pass-by-value守则再次适用。

C++高效编程守则视状况而变化，取决于你使用C++的哪一部分。

##### 3、尽量以const, enum, inline, 替换#define。 ——“条款02”
对于单纯变量，最好以const对象或者enum替换#define。
对于形似函数的宏，最好改用inline函数替换#define。

##### 4、尽量使用const。——“条款03”

##### 5、确定对象在被使用之前已经先被初始化。——“条款04”
C++规定，对象的成员变量的初始化动作发生在进入构造函数本体之前，即在初始化列表中进行初始化变量。

构造函数最好使用成员初始化列表，而不是在构造函数本体内使用赋值操作。初始化列表列出的成员变量，其排列次序应该和它们在class中的声明次序相同。

C++有着十分固定的“成员初始化次序”。是的，次序总是相同的：base classes更早于其derived classes被初始化，而class的成员变量总是以其声明次序被初始化。

C++对“定义于不同编译单元内的non-local static对象”的初始化相对次序并无明确定义。C++保证，函数内的local static对象会在“该函数被调用期间”“首次遇上该对象之定义式”时被初始化。
为免除“跨编译单元之初始化次序”问题，请以local static对象替换non-local static对象。

##### 6、了解C++默认编写并调用哪些函数。——“条款05”
如果没有为类声明（或定义）default构造函数、copy构造函数、copy assignment操作符、析构函数，那么编译器自动生成它们，并且默认生成的这些函数都是public且inline，另外编译器产生的析构函数是个 non-virtual，除非这个class的base class自身声明有virtual析构函数。

一般而言只有当生出的代码合法且有适当机会证明它有意义，编译器才会为class生出operator=；否则，只要两个条件中有一个不符合，编译器就会拒绝为class生出operator=。
如果某个base classes将copy assignment操作符声明为private，编译器将拒绝为其derived classes生成一个copy assignment操作符。

##### 7、为了不让编译器自动（暗自）生成某些函数，可将相应的成员函数声明为private，以使得阻止别人调用它；并且不去实现相应的成员函数。 ——“条款06”

##### 8、polymorphic（带多态性质的）base classes应该声明一个virtual析构函数。如果class带有任何virtual函数，它就应该拥有一个virtual析构函数。 ——“条款07”

Classes 的设计目的如果不是作为base classes使用，或者不是为了具备多态性（polymorphically），就不该声明virtual析构函数。另外，如果说一个类没有 virtual析构函数，那么它就不能作为base classes；要想作为base classes，就必须把析构函数声明virtual。

##### 9、别让异常逃离析构函数。——条款“08”
C++并不禁止析构函数吐出异常，但是绝对不能让析构函数吐出异常。如果一个被析构函数调用的函数可能抛出异常，析构函数就应该捕捉所有的异常，然后吞下它们（不传播）或结束程序。

如果客房需要对某个操作函数运行期间抛出的异常做出反应，那么class应该提供一个普通函数（而非在析构函数中）执行该操作。

##### 10、绝不要在构造函数和析构函数过程中调用virtual函数，因为这类调用从不下降到继承类（比起当前执行构造函数和析构函数的那层）。——“条款9”

##### 11、令赋值操作符返回一个reference to *this。——“条款10”
注：这只是个协议，并无强制性；如果不遵循它，代码一样可以通过编译。

##### 12、在operator=中处理“自我赋值”。——“条款11”
确保当对象自我赋值时operator有良好行为。其中技术包括比较“来源对象”和“目标对象”的地址、精心周到的语句顺序、以及copy-and-swap。

确定任何函数如果操作一个以上的对象，而其中多个对象是同一个对象时，其行为仍然正确。
不能令copy assignment操作符调用copy构造函数；同样，不能令copy构造函数调用copy assignment操作符。如果copy构造函数和copy assignment操作符有相似的代码，消除重复代码的做法是，建立一个新的成员函数给两者调用。这样的函数往往是private而且常被命名为 init。 ——“条款12”

##### 13、以对象管理资源。为了防止资源泄漏，请使用RAII（Resource Acquisition Is Initialization，资源取得时便是初始化时）对象，它们在构造函数中获得资源并在析构函数中释放资源。也就是当使用资源时，请 把资源封装在一个对象当中。两个常被使用的RAII classes分别是trl::shared_ptr和auto_ptr，而前者通常是较佳选择。 ——“条款13”

复制RAII对象必须一并复制它所管理的资源，所以资源的copying行为决定RAII对象的copying行为。普遍而常见的RAII class copying行为是：抑制copying、施行引用计数法。不过其他行为也都可能被实现。 ——“条款14”

##### 14、在规划或设计“接口”时，一定要注意接口的一致性，以及与内置类型的行为兼容。      ——“条款18”

##### 15、对于类对象，尽量以pass-by-reference-to-const替换pass-by-value，前者通常比较高效，并可避免切割问题 （slicing problem）。但是对于内置类型、STL的迭代器和函数对象，pass-by-value往往比较高效。 ——“条款20”

##### 16、宁可拿non-member non-friend函数替换member函数。这样做可以增加封装性、包裹弹性（packaging flexibility）和机能扩充性。 ——“条款23”

##### 17、如果你需要为某个函数的所有参数（包括被this指针所指的那个隐喻参数）进行类型转换，那么这个函数必须是个non-member。——“条款24”

##### 18、尽可能延后变量定义式的出现。 ——“条款26”

##### 19、尽量少做转型动作。——“条款27”
如果可以，尽量避免转型，特别是在注重效率的代码中避免dynamic_casts。如果有个设计需要转型动作，试着发展无需转型的替代设计。

如果转型是必要的，试着将它隐藏于某个函数的背后。

宁可使用C++-style（新式）转型，也不要使用旧式转型。

##### 20、避免返回handles（包括references、指针、迭代器）指向对象内部。增加这个条款可增加封装性，使const成员函数的行为更像个const，并将发生“虚吊号码牌”（dangling handles）的可能性降至最低。——“条款28”

##### 21、确定你的public继承塑模出is-a关系。——“条款32”
“public继承”意味着is-a。适用于基类身上的每一件事情一定也适用于派生类身上，因为每一个派生类对象也都是一个基类对象。

##### 22、 derived classes内的名字会遮掩base classes内的名称。为了让被遮掩的名称重见天日，可使用using声明式（目的是在当前作用域中引入被遮掩的名称标识符）或转交函数 （forwarding functions，在遮掩函数中调用被遮掩的函数，以隐式的引入被遮掩的函数名称标识符）。 ——“条款33”

##### 23、接口继承和实现继承是不同的。声明一个pure virtual函数的目的是为了让derived classes只继承函数接口；声明简朴的（即非纯）impure virtual函数的目的是让derived classes继承该函数的接口和缺省实现（但还可以改变缺省实现）；声明non-virtual函数的目的是为了让derived classes继承函数的接口及一份强制性实现（这份实现，derived classes不能改变）。   ——“条款34”

##### 24、考虑virtual函数以外的其他选择。——“条款35”（详查条款35）

##### 25、绝对不要重新定义继承而来的non-virtual函数。 ——“条款36”
说明：B——基类类型，D——派生类类型，mf——B中的non-virtual成员函数。
如果D重新定义mf，你的设计便出现了矛盾。如果D真有必要实现出与B不同的mf，并且如果每一个B对象——不管多么特化——真的必须使用B所提供的mf实现码，那么“每个D都是一个B”就不为真。既然如此，D就不该以public形式继承自B。另一方面，如果D真的必须以public方式继承自B，并且如果D真有需要实现出与B不同的mf，那么mf就无法为B反映出“不变性凌驾于特异性”的性质。既然这样，mf应该声明为virtual函数。最后，如果每个D真的是一个B，并且如果mf真的为B反映出“不变性凌驾于特异性”的性质，那么D便不需要重新定义mf，而且它也不应该尝试这样做。

##### 26、绝对不要重新定义一个继承而来的缺省参数值，因为缺省参数值都是静态绑定的，而virtual函数——你唯一应该覆写的东西——却是动态绑定的。静态绑定下的函数并不从其base classes继承缺省参数值，动态绑定下的函数会从其base classes继承缺省参数值。 ——“条款37”

##### 27、明智而审慎地使用private继承。——“条款39”
private继承的首要规则是，如果classes之间的继承关系是private，编译器不会自动将一个derived classes对象转换为一个base classes对象；第二条规则是，由private base class继承而来的所有成员，在derived class中都会变成private属性，纵使它们在base class中原本是protected或public属性。

Private 继承意味着implemented-in-terms-of（根据某物实现出）。private继承意味着只有实现部分被继承，接口部分应略去。如果D以 private形式继承B，意思是Ｄ对象根据Ｂ对象实现而得，再也没有其他意涵了。private继承在软件“设计”层面上没有意义，其意义只及于软件实 现层面。

##### 28、明智而审慎地使用多重继承。——“条款40”
对virtual base classes（变相当于对virtual继承）的忠告：第一，非必要时不要使用virtual bases，平常请使用non-virtual继承；第二，如果必须使用virtual base classes，尽可能避免在其中放置数据。

virtual 继承会增加大小、速度、初始化（及赋值）复杂度等等成本。如果virtual base classes不带任何数据，将是最具有实用价值的情况。多重继承的确有正当用途：其中一个情节涉及“public继承某个Interface class“和”public继承某个协助实现的class“的两相组合。

##### 29、classes和templates都支持接口和多态。对classes而言，接口是显示的，以函数签名为中心；多态则是通过virtual函数发生于运行期。对template参数而言，接口是隐式的， 奠基于有效表达式；多态则是通过template具现化和函数重载解析发生于编译期。——“条款41”

##### 30、当我们编写一个class template，而它所提供之“与此template相关的”函数支持“所有参数之隐式类型转换”时，请将那些函数定义为“class template内部的friend函数”。——“条款46”

##### 31、TMP(Template metaprogramming，模板元编程)已被证明是个“图灵完全”（Turing-complete）机器，意思是说它的威力大到足以计算任何事物。——“条款48”
