
资源管理——防止资源泄漏
------------------

本文由“`三界：天地人`”（`xgfone`）根据Scott Meyers的《`More Effective C++`》（侯捷 译）一书中的“`条款10`”进行整理而行。

在传统的资源管理中，我们常用的技术是：`在构造函数中申请资源，在析构函数中释放资源`。但是这有个缺点，就是当在构造函数中申请资源时，如果发生资源申请异常，就会导致构造函数失败；这样一来，当构造的对象离开作用域时，析构函数不会调用，原因是：如果构造函数不能正常完成时，析构函数就不会做相应的调用。这样一来，就会发生资源泄漏——申请了的资源无法收回。

在构造对象时，我知道一定要在构造函数中完成，但又会有资源泄漏的危机，这就需要一些技术来防止资源泄漏。

#### 方案一：传统上，在构造函数中简单地申请资源，在析构函数释放资源。
```c++
class BookEntry{
public:
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address), theImage(0), theAudioClip(0)
    {
        if(imageFileName != ""){
            theImage=new Image(imageFileName);
        }
        if(audioClipFileName != ""){
            theAudioClip=new AudioClip(audioClipFileName);
        }
    }
    /*上个构造函数的简写，如下：
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address),
     theImage(imageFileName != "" ? new Image(imageFileName) : 0),
     theAudioClip(audioClipFileName != "" ? new AudioClip(audioClipFileName) : 0)
    {}
    */

    ~BookEntry()
    {
        delete theImage;
        delete theAudioClip;
    }
    void addPhoneNumber(const PhoneNumber& number);
    .......

private:
    string theName;
    string theAddress;
    list<PhoneNumber> thePhones;
    Image *theImage;
    AudioClip *theAudioClip;
};
```
以上是常规的资源申请与释放，但是有时它并不一定能正常工作。
分析：如果在申请第一个资源——theImage=new Image(imageFileName);——成功，但在申请第二个资源—— theAudioClip=new AudioClip(audioClipFileName)——失败时，这就会导致构造函数失败，所以构造函数就不会做出正常的调用（我们也没办法完成这种情况下的析构函数的调用），这样一为，就会导致资源泄漏——申请的第一个资源无法释放。因此，这种方法并不是很完美！我们需要另外一种方法。

#### 方案二：在构造函数中捕获所有可能发生的异常，如果有异常发生，就释放已经分配的对象，并再次传播异常（即把捕获的异常从该构造函数中传播出支）。
```c++
class BookEntry{
public:
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address), theImage(0), theAudioClip(0)
    {
        try{
            if(imageFileName != ""){
                theImage=new Image(imageFileName);
            }
            if(audioClipFileName != ""){
                theAudioClip=new AudioClip(audioClipFileName);
            }
        }
        catch(...){
            delete theImage;
            delete theAudioClip;
            throw;
        }
    }
```
分析：这个方案看起来比较好极了。但是让人感觉有点臭长，不过它不失一个很好的解决方案之一。

#### 方案三：在构造函数中申请资源时，把每一个资源申请放在一个函数中，然后再捕捉是否有任何异常发生，如果有任何异常发生，就要释放以前所有申请过的资源。
```c++
class BookEntry{
public:
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address),
     theImage(initImage(imageFileName)),
     theAudioClip(initAudioClip(audioClipFileName))
    {}

    ~BookEntry()
    {
        delete theImage;
        delete theAudioClip;
    }
    void addPhoneNumber(const PhoneNumber& number);
    .......

private:
    string theName;
    string theAddress;
    list<PhoneNumber> thePhones;
    Image *theImage;
    AudioClip *theAudioClip;

    initImage(const string& imageFileName)
    {
        if(imageFileName != "")  return new Image(imageFileName);
        else  return 0;
    }

    initAudioClip(const string& audioClipFileName)
    {
        try{
            if(audioClipFileName != "")  return new AudioClip(audioClipFileName);
            else  return 0;
        }
        catch (...){
            delete theImage;
            throw;
        }
    }
};
```
分析：这个方案解决了方案一中遇到的问题，这可能是个完美的结局。但是，这个方案有个缺点是：概念上应该由constructor完成的动作现在却散布于数个函数中，在概念上却违反了construtor的作用，造成维护上的困扰。

#### 方案四：运用智能指针。在构造对象申请资源时发生了异常，当该对象离开其作用域时，智能指针指向的资源也会自动释放。
```c++
class BookEntry{
public:
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address), theImage(0), theAudioClip(0)
    {
        if (imageFileName != ""){
            theImage = new Image(imageFileName);
        }
        if (audioClipFileName != ""){
            theAudioClip = new AudioClip(audioClipFileName);
        }
    }

    /*上个构造函数的简写，如下：
    BookEntry(const string& name, const string& address="",
              const string& imageFileName="", const string& audioClipFileName="")
    :theName(name), theAddress(address),
     theImage(imageFileName != "" ? new Image(imageFileName) : 0),
     theAudioClip(audioClipFileName != "" ? new AudioClip(audioClipFileName) : 0)
    {}
    */

    ~BookEntry()
    {
        delete theImage;
        delete theAudioClip;
    }
    void addPhoneNumber(const PhoneNumber& number);
    .......

private:
    string theName;
    string theAddress;
    list<PhoneNumber> thePhones;

    const auto_ptr<Image>  theImage;
    const auto_ptr<AudioClip>  theAudioClip;
};
```
分析：处理“构造过程中可能发生的exceptions”相当棘手。但是，通过auto_prt（以及与auto_ptr相似的classes），可以消除大部分劳役；使用它们，不仅能够让代码更容易理解，也使程序在面对exceptions时更健壮。**_智能指针使用的是RAII理论_**。

RAII是“**资源获取就是初始化**”的缩语（Resource Acquisition Is Initialization），是一种利用对象生命周期来控制程序资源（如内存、文件句柄、网络连接、互斥量等等）的简单技术。 　　

RAII 的一般做法是这样的：在对象构造时获取资源，接着控制对资源的访问使之在对象的生命周期内始终保持有效，最后在对象析构的时候释放资源。借此，我们实际上把管理一份资源的责任托管给了一个对象。这种做法有两大好处： 　
　
    (1) 我们不需要显式地释放资源。 　
    (2) 采用这种方式，对象所需的资源在其生命期内始终保持有效。
        我们可以说，此时这个类维护了一个 invariant。
        这样，通过该类对象使用资源时，就不必检查资源有效性的问题，可以简化逻辑、提高效率。
