---
title: C++杂篇
date: 2025-08-28 17:11:49
tags: [C++]
image: 'cover/cover-17.jpg'
---

# vector容器

`std::vector` 是 C++ 中最常用的动态数组容器，提供了自动内存管理和丰富的操作功能。

```c++
#include <vector>        //头文件
#include <iostream>

//基本声明
std::vector<int> vec1;              // 空vector
std::vector<int> vec2(5);           // 5个元素，默认值0
std::vector<int> vec3(5, 10);       // 5个元素，每个都是10
std::vector<int> vec4 = {1, 2, 3};  // 初始化列表
std::vector<int> vec5(vec4);        // 拷贝构造

//二维vector
std::vector<std::vector<int>> matrix(3, std::vector<int>(4)); // 3x4矩阵
std::vector<std::vector<int>> matrix2 = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

//添加元素
vec.push_back(10);    // 在末尾添加元素10
vec.insert(vec.begin()+1, 6);  //在第二位添加6

// 各种访问方式
std::cout << vec[0];       // 下标访问（不检查边界）
std::cout << vec.at(1);    // 带边界检查的访问
std::cout << vec.front();  // 第一个元素
std::cout << vec.back();   // 最后一个元素

// 遍历访问
for (int i = 0; i < vec.size(); ++i) {
    std::cout << vec[i] << " ";
}

//修改元素
vec[0] = 100;        // 修改第一个元素
vec.at(1) = 200;     // 修改第二个元素

//删除元素
cpp
vec.pop_back();       // 删除最后一个元素
vec.clear();          // 清空所有元素

// 删除特定位置的元素
vec.erase(vec.begin() + 2);        // 删除第三个元素
vec.erase(vec.begin(), vec.begin() + 2); // 删除前两个元素
```

## 重要注意事项

1. **自动内存管理**：vector会自动处理内存分配和释放
2. **动态扩容**：当容量不足时，vector会自动扩容（通常是2倍）
3. **迭代器失效**：在修改vector后，迭代器可能会失效
4. **性能考虑**：`push_back()` 平均O(1)，但扩容时是O(n)
