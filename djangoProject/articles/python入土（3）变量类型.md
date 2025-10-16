---
title: python入土（3）变量类型
date: 2024-10-11 19:36:07
tags: python
image: 'cover/cover-5.jpg'
---

1. # 整数（int）

  整数是没有小数部分的数字。在 Python 中，可以直接使用整数进行数学运算，如加法、减法、乘法和除法。
  例如：

```python
a = 10
b = 20
c = a + b
print(c)  # 输出 30
```

----------------------------------------------------

2. # 浮点数（float）
    
  浮点数是带有小数部分的数字。同样，也可以对浮点数进行各种数学运算。
    例如：

```python
d = 3.14
e = 2.5
f = d * e
print(f)  # 输出 7.85
```

----------------------------------------------------

# 3.字符串（str）

字符串是由字符组成的序列，可以是字母、数字、符号等。在 Python 中，字符串可以用单引号（‘）、双引号（"）或三引号（’‘’ 或"“”）来表示。
例如：

```python
g = 'Hello, world!'
h = "Python is great."
i = '''This is a multi-line
string.'''
print(g)
print(h)
print(i)
```

可以对字符串进行拼接、切片等操作。

拼接：

```python
j = 'Hello'
k = 'world'
l = j + ', ' + k + '!'
print(l)  # 输出 Hello, world!
```

切片：

```python
m = 'Python'
print(m[1:4])  # 输出 yth
```

------------------------------------------------------------------

4. # 列表（List）

   ## 定义和基本概念

   列表是 Python 中最常用的数据类型之一，它是一个有序的可变序列。
   可以将多个不同类型的数据元素组合在一起，用方括号[]来表示。
   例如：my_list = [1, 2.5, 'hello', True]，这个列表包含了一个整数、一个浮点数、一个字符串和一个布尔值。

   ## 列表的操作

   ### 索引和切片

列表中的每个元素都有一个索引，索引从 0 开始。可以通过索引来访问列表中的元素，例如：my_list[0]将返回列表中的第一个元素 1。

切片操作可以获取列表中的一部分元素。语法是my_list[start:stop:step]，其中start是起始索引（包含），stop是结束索引（不包含），step是步长。例如：my_list[1:3]将返回[2.5, ‘hello’]；my_list[::2]将返回[1, ‘hello’]（从第一个元素开始，每隔一个元素取一个）。

### 添加元素

可以使用append()方法在列表的末尾添加一个元素。例如：

```python
my_list = [1, 2, 3]
my_list.append(4)
print(my_list)  
#输出 [1, 2, 3, 4]
```

也可以使用insert()方法在指定位置插入一个元素。语法是my_list.insert(index, element)，例如：

```python
my_list = [1, 2, 3]
my_list.insert(1, 'new')
print(my_list)  
# 输出 [1,"new,2,3]"
```

### 删除元素

使用remove()方法可以删除列表中指定的元素。例如

```python
my_list = [1, 2, 3]
my_list.remove(2)
print(my_list)  
#输出 [1, 3]
```

还可以使用pop()方法删除指定索引位置的元素，并返回被删除的元素。例如：

```python
my_list = [1, 2, 3]
popped_element = my_list.pop(1)
print(popped_element)  
# 输出 2
print(my_list)  
# 输出 [1, 3]
```

3. ## 列表的排序和反转

  sort()方法可以对列表中的元素进行排序。如果列表中的元素是数字，将按照数字大小排序；如果是字符串，将按照字母顺序排序。例如：

```python
num_list = [3, 1, 4, 1.5]
num_list.sort()
print(num_list)  
#输出 [1, 1.5, 3, 4]
```


reverse()方法可以反转列表中元素的顺序。例如：

```
my_list = [1, 2, 3]
my_list.reverse()
print(my_list)  

# 输出 [3, 2, 1]
```

--------------------------------------------------------------------

5. # 元组（Tuple）

   ## 定义和基本概念

   元组是有序的不可变序列，用圆括号()来表示。例如：my_tuple=(1, 2.5,
   ‘hello’)。一旦元组被创建，其元素不能被修改、添加或删除。

   ## 元组的操作

   ### 索引和切片

与列表类似，元组中的元素也有索引，从 0 开始。可以通过索引访问元组中的元素，如my_tuple[0]将返回 1。

也可以进行切片操作，语法和列表相同。例如：my_tuple[1:3]将返回(2.5, ‘hello’)。

元组的优点
由于元组是不可变的，所以在处理一些不希望被修改的数据时非常有用。例如，函数返回多个值时，可以将这些值包装成一个元组返回，保证数据的完整性和一致性。例如：

```python
def get_info():
    name = "Alice"
    age = 25
    return (name, age)
info = get_info()
print(info[0])  

# 输出Alice

print(info[1])  

# 输出25
```

--------------------------------------------------------------------

6. # 字典（Dictionary）

   ## 定义和基本概念
   
   字典是一种无序的可变容器数据类型，它以键 - 值（key - value）对的形式存储数据。用花括号{}来表示。例如：my_dict ={‘name’: ‘Alice’, ‘age’: 25, ‘city’: ‘NewYork’}，
   
   其中’name’、‘age’、'city’是键，‘Alice’、25、'New York’是对应的值。字典的操作
   访问和修改值

可以通过键来访问字典中的值，例如：my_dict[‘name’]将返回’Alice’。

修改值也很简单，例如：my_dict[‘age’] = 26，此时字典中的年龄值就被修改为 26。

## 添加和删除键 - 值对

添加键 - 值对可以直接通过赋值操作来完成。例如：my_dict[‘job’] = ‘Engineer’，
此时字典中就添加了一个新的键 - 值对’job’: ‘Engineer’。

删除键 - 值对可以使用del关键字。例如：del my_dict[‘city’]，这样就删除了’city’这个键以及对应的’NewYork’这个值。

遍历字典

可以使用for循环来遍历字典的键。例如：

```
my_dict = {'name': 'Alice', 'age': 25, 'city': 'New York'}
for key in my_dict.keys():
    print(key)
# 输出 name、age、city
```

也可以遍历字典的值。例如

```
for value in my_dict.values():
    print(value)
# 输出 Alice、25、New York
```

