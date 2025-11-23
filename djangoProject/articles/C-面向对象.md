---
title: C++面向对象
date: 2025-11-18 21:26:20
tags: C++
image: 
---

111111

面向对象编程(OOP)是一种特殊的、设计程序的概念性方法，下面是最重要的OOP特性：

- 抽象
- 封装和数据隐藏
- 多态
- 继承
- 代码的可重用性

为了实现这些特性，C++提供了类。

# C++的类

类是一种将抽象转换为用户定义类型的C++工具，它将数据表示和操纵数据的方法组合成一个整洁的包。  
下面设定看一个学生的类。 

```c++
class student{
public:
	void setName(string name){}
private:
    string name;
    int age;
}

int main(){
	student stu1;
	stu1.setName();    //使用类
}
```

C++关键字`class`指出这些代码定义了一个类设计，这个声明让我们能声明一个student类型的变量--称为对象或实例。声明一个student对象：

`student stu1`

接下来存储的数据以类数据成员的形式出现。

## 访问控制

关键字`public`和`private`描述了类成员的访问控制。使用类对象的程序可以直接访问公有部分，但只能通过公有成员函数(或者友元函数)访问对象的私有成员。如上面的name只能通过在类内定义函数实现修改。因此，公有成员函数是程序和对象的私有成员之间的桥梁，提供了程序和对象之间的接口。

## 实现类成员函数

两种方法，一种是在类内直接完成。

```c++
void setName(string name){...}
```

另一种是类外实现，需要使用作用域解析符（::）来指出所属的类。

```c++
void student::setName(string name){...}
```

通常将C++的类放入到一个独立的实现文件中，为它创建为一个.h文件，并在同名的.cpp文件中实现功能。

-----------------------------

# 构造函数和析构函数

类的**构造函数**是类的一种特殊的成员函数，它会在每次创建类的新对象时执行。  
构造函数的名称与类的名称是完全相同的，并且不会返回任何类型，也不会返回 void。构造函数可用于为某些成员变量设置初始值。

类的**析构函数**是类的一种特殊的成员函数，它会在每次删除所创建的对象时执行。  
析构函数的名称与类的名称是完全相同的，只是在前面加了个波浪号（~）作为前缀，它不会返回任何值，也不能带有任何参数。析构函数有助于在跳出程序（比如关闭文件、释放内存等）前释放资源。

使用构造函数和析构函数：

```c++
#include <iostream>
using namespace std;

class Staff{
public:
    //构造函数
    Staff(){
        cout << "构造函数被调用" << endl;
    };
    //析构函数
    ~Staff(){
        cout << "析构函数被调用" << endl;
    };
};

int main(){
    Staff staff1;  //构造函数和析构函数会被自动执行
    return 0;
}
```

------------------

# 运算符重载

你可以重定义或重载大部分 C++ 内置的运算符。这样，您就能使用自定义类型的运算符。

```c++
class Staff{
public:
    int a = 10;
    int b = 20;
    Staff operator+ (Staff &p){
        Staff temp;
        temp.a = this->a + p.a;
        temp.b = this->b + p.b;
        return temp;
    }
};

int main(){
    Staff st1;
    Staff st2;
    Staff st3;
    st3 = st1 + st2;
}
```

st3 = st1 + st2; 这是运算符重载的常规写法
st3 = st1.operator+(st2);   成员函数的显式调用

-------------

# 友元

类的友元函数是定义在类外部，但有权访问类的所有私有（private）成员和保护（protected）成员。尽管友元函数的原型有在类的定义中出现过，但是友元函数并不是成员函数。

友元可以是一个函数，该函数被称为友元函数；友元也可以是一个类，该类被称为友元类，在这种情况下，整个类及其所有成员都是友元。

如果要声明函数为一个类的友元，需要在类定义中该函数原型前使用关键字 friend。

```c++
class Staff{
public:
	friend void fune();
};
```

---------------------------------

# 类继承

为了提高代码的重用性，C++允许从已有的类中派生出新的类，派生类继承原有类（或者说基类）的特征，包括方法。可以通过继承完成下面一些功能：

- 在已有类的基础上添加功能。
- 可以给类添加数据。
- 可以修改类方法的行为。

接下来设定一个人类基类：

```c++
class human{
public:
    human(int _age, string _name){...};
    ~human(){...};
    void func(){};
private:
    string name;
    int age;
}
```

派生一个学生类：

```c++
class student : public human{
public:
    student(int _num, int _grade){...};
    ~student(){...};
private:
    int stu_num;
    int grade;
}
```

上面代码中冒号指出student类的基类是human类。public表示公有继承，基类的公有成员将成为派生类的公有成员；基类的私有部分只能通过基类的公有方法访问。

当你实例化一个派生类时，会首先创建基类对象，派生类构造函数应通过成员初始化列表将基类信息传递给基类构造函数。

```c++
student::student(string _name, int _age, int _num, int _grade) : human(_age, _name){
    ...
}
```

派生类和基类直接有一些特殊的关系。派生类对象可以使用基类的方法，前提是它不是私有的：

```c++
student stu1();
stu1.func();
```

有一个特别重要的关系是：基类指针或引用可以在不进行显式类型转换的情况下指向派生类对象，但是基类的指针或引用只能调用基类方法。
