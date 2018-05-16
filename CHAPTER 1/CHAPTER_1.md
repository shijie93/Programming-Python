# chapter 1.A Sneak Preview
本章节主要提供了一些你可以用Python做的事情的演示，如果你在寻找本章中应用的工具和技术的完整解释，那么你必须阅读本书后面的部分。这里选择了一个简单的应用：构建记录数据库 - 并通过多个步骤迁移它：交互式编码，命令行工具，控制台界面，GUI和简单的基于Web的界面。在此过程中，我们还将深入探讨数据表示，对象持久性和面向对象编程（OOP）等概念; 探索一些我们稍后会在书中重新讨论的替代方案; 并在阅读本书之前回顾一些您应该了解的核心Python思想。

## Step 1:如何表示一个记录
在数据库中存储之前，你需要决定如何表示这些记录。像列表和字典这样的内置对象类型通常是足够的，特别是如果我们最初对处理存储的数据不关心的话。

**使用 列表(lists)**

列表可以手机人的属性以一个`固定顺序`的方式，首先新建两条记录，代表两个人：
```python
# name, age, pay, and job 
bob = ['Bob Smith', 42, 30000, 'software']
sue = ['Sue Jones', 45, 40000, 'hardware']

sue[0] # Sue Jones
bob[2] # 30000
```
类似 `数组` 的概念，可以使用 index 进行索引。

处理记录也比较简单，可以像如下方式进行：
```python
print (bob[0].split())
# ['Bob', 'Smith']

print (bob[0].split()[0])
# 'Bob'
```
> 我们获取Bob的名字，split 将它放入子字符串列表中，并索引他的姓氏。

**一个数据库列表**

我们目前只是有了两条记录，为了收集它们，把它们放进另一个列表：
```python
bob = ['Bob Smith', 42, 30000, 'software']
sue = ['Sue Jones', 45, 40000, 'hardware']

people = [bob, sue]
for person in people:
    print(person)

# ['Bob Smith', 42, 30000, 'software']
# ['Sue Jones', 45, 40000, 'hardware']
```
此时的 `people` 代表我们的数据库，我们可以通过对应位置来获取记录并处理它们
```python
for person in people:
    print(person[0].split()[-1]) # print last names
    person[2] *= 1.20

for person in people:
    print(person[2])

# Smith
# Jones
# 36000.0
# 48000.0
```
我们还可以使用一些更强力的迭代工具：
```python
pays = [person[2] for person in people] 
print (pays)

pays = map((lambda x: x[2]), people) 
print (list(pays))

print (sum(person[2] for person in people))

# [36000.0, 48000.0]
# [36000.0, 48000.0]
# 84000.0
```
添加一个记录：
```python
people.append(['Tom', 50, 0, None])

# 显示最后一个客户的姓名
people[-1][0]
```
这种数据存储方式很明显是存放在内存之中，退出程序随即消失。

**字段标签(Field labels)**

