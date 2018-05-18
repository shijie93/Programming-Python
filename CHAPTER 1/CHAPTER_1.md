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

通过在列表中的位置来访问字段通常需要我们来记住每一个位置所代表的字段的含义，即代码中会经常出现一些幻数。为了更好地让人理解代码，通过名称和值关联通常会更好。

通常使用内建函数 `range` 来完成名称和位置的关联：
```python
NAME, AGE, PAY = range(3)
bob = ['Bob Smith', 42, 10000]
PAY, bob[PAY] # (2, 10000)
```
当记录的结构发生变化时，需要同步更新 `range` 赋值。因为它们没有直接关联，所以名称和记录可能随着时间的推移而不同步并需要维护步骤。此外，由于字段名称是独立变量，因此没有从记录列表直接映射回其字段名称的方法。 例如，原始记录列表无法在格式化显示中使用字段名称标记其值，`bob.index(42)` 的值是 1，而不是 AGE。

**使用字典**

上述以列表为基础的数据存储可以实现功能，但是需要以搜索字段名称的性能作为代价。内建对象字典可以做得更好：
```python
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}
```
此时字段名称和值会自动的建立映射，它也使我们接下来的代码更易理解和有价值。我们不需要记住字段名称在其中的偏移，也不需要在新增字段值时更新和维护一组 `range`，这些交给字典自身的特性即可。
```python
bob['name'], sue['pay'] # ('Bob Smith', 40000)
bob['name'].split()[-1] # 'Smith'
```
由于字段现在可以通过 `key` 访问，所以对于那些阅读代码的人来说，这些字段更有意义。

**其他构建字典的方式**

1. 使用构造函数
```python
bob = dict(name='Bob Smith', age=42, pay=30000, job='dev')
```

2. 逐个赋值
```python
sue = {}
sue['name'] = 'Sue Jones'
sue['age'] = 45
sue['pay'] = 40000
sue['job'] = 'hdw'
```

3. 使用内建函数`zip`
```python
names = ['name', 'age', 'pay', 'job']
values = ['Sue Jones', 45, 40000, 'hdw']
list(zip(names, values)) # [('name', 'Sue Jones'), ('age', 45), ('pay', 40000), ('job', 'hdw')]
dict(zip(names, values)) # {'job': 'hdw', 'pay': 40000, 'age': 45, 'name': 'Sue Jones'}
```

4. 初始化一个空字典
```python
fields = ('name', 'age', 'job', 'pay')
record = dict.fromkeys(fields, '?')
record # {'job': '?', 'pay': '?', 'age': '?', 'name': '?'}
```

**字典组成的列表**

上面介绍了使用字典构成单条记录，这里仍然使用列表作为记录的数据路，只要我们不需要通过key来访问顶层的记录：
```python
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}

people = [bob, sue]
for person in people:
    print(person['name'], person['pay'], sep=', ')

# Bob Smith, 30000
# Sue Jones, 40000

for person in people:
    if person['name'] == 'Sue Jones': # fetch sue's pay
        print(person['pay'])

# 40000
```
使用迭代工具：
```python
names = [person['name'] for person in people]
list(map((lambda x: x['name']), people))
sum(person['pay'] for person in people)
```
即使目前在内存对象上运行，列表解析和按需生成器表达式可以处理SQL查询：
```python
[rec['name'] for rec in people if rec['age'] >= 45] 

[(rec['age'] ** 2 if rec['age'] >= 45 else rec['age']) for rec in people] # [42, 2025]
```

**嵌套结构**

python中的所有复合数据类型都支持互相嵌套任意我们喜欢的深度，我们简单的构建相当复杂格式的数据结构。Python可以完成构建组件，链接内存结构并且后来回收他们的空间。下面的例子通过嵌套字典，列表和元祖在另一个字典中：
```python
bob2 = {'name': {'first': 'Bob', 'last': 'Smith'},
        'age': 42,
        'job': ['software', 'writing'],
        'pay': (40000, 50000)}

bob2['name']['last'] # 'Smith'
```

