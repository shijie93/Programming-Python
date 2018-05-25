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
bob2['job'].append('janitor')
```

**字典的字典**

我们可以使用字典嵌套字典，外层字典是数据库，而嵌套的是在它内部的记录。基于字典的数据库不单是一个简单的记录列表，而是允许我们通过 `key` 来存储和检索记录。
```python
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}

db = {}
db['bob'] = bob
db['sue'] = sue

pprint.pprint(db) # pprint 可以输出格式优美的内容

for key in db:
    print(key, '=>', db[key]['name'])

# bob => Bob Smith
# sue => Sue Jones
```
也可以直接访问字典的值
```python
for record in db.values():
    print(record['pay'])

# 30000
# 40000
```
此时的数据仍存在于内存中。

## Step 2:持续存储记录
到目前为止，我们已经解决了基于字典的记录数据库的表示方式，并且我们一直在回顾一些Python数据结构的概念。 如前所述，目前为止我们所看到的对象都是临时的，它们都存在于内存中，一旦我们退出Python或创建它们的Python程序，它们就会消失。 为了让记录持久，他们需要存储在某种文件中。

### 2.1使用格式化文件
一种存储我们数据的方式是将所有的内容以一定的格式保存在一个文本文件中。

**测试数据脚本**

我们首先来写一个脚本来初始化我们将要存储的数据：
```python
# initdata.py
# initialize data to be stored in files, pickles, shelves
# records
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}
tom = {'name': 'Tom', 'age': 50, 'pay': 0, 'job': None}

# database
db = {}
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom

if __name__ == '__main__': # when run as a script
    for key in db:
        print(key, '=> ', db[key])
```
通常，当单独运行 initdata.py 时，`__name__ == '__main__'` 表现为 true。当这个文件被调用时，表现为false，通常这方便于我们进行模块调试。

**数据格式脚本**

现在，我们所要做的就是将所有这些内存数据存储在一个文件内。 有很多方法可以实现这一点，最基本的一种是一次写入一段数据，每次我们可以在重新加载时使用分隔符来分开数据：
```python
"""
Save in-memory database object to a file with custom formatting;
assume 'endrec.', 'enddb.', and '=>' are not used in the data;
assume db is dict of dict; warning: eval can be dangerous - it
runs strings as code; could also eval() record dict all at once;
could also dbfile.write(key + '\n') vs print(key, file=dbfile);
"""
dbfilename = 'people-file'
ENDDB = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'


def storeDbase(db, dbfilename=dbfilename):
    "formatted dump of database to flat file"
    dbfile = open(dbfilename, 'w')
    for key in db:
        print(key, file=dbfile)
        for (name, value) in db[key].items():
            print(name + RECSEP + repr(value), file=dbfile)
        print(ENDREC, file=dbfile)
    print(ENDDB, file=dbfile)
    dbfile.close()


def loadDbase(dbfilename=dbfilename):
    "parse data to reconstruct database"
    dbfile = open(dbfilename)
    import sys
    sys.stdin = dbfile
    db = {}
    key = input()
    while key != ENDDB:
        rec = {}
        field = input()
        while field != ENDREC:
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = input()
        print (rec)
        db[key] = rec
        key = input()
    return db

if __name__ == '__main__':
    from initdata import db
    storeDbase(db)
    loadDbase(dbfilename)

# bob
# name=>'Bob Smith'
# age=>42
# pay=>30000
# job=>'dev'
# endrec.
# sue
# name=>'Sue Jones'
# age=>45
# pay=>40000
# job=>'hdw'
# endrec.
# tom
# name=>'Tom'
# age=>50
# pay=>0
# job=>None
# endrec.
# enddb.
```

**工具腳本**

我們通过一下脚本重载数据库的数据：
```python
from make_db_file import loadDbase
db = loadDbase()

for key in db:
    print(key, '=>\n ',db[key])
print(db['sue']['name'])
```

更新数据库
```python
from make_db_file import loadDbase, storeDbase
db = loadDbase()
db['sue']['pay'] *= 1.10
db['tom']['name'] = 'Tom Tom'
storeDbase(db)
```

### 2.2.Using Pickle Files
前文提到的格式化的文本文件是有效地，但是它也有一些限制。即使仅仅需要其中一个记录，我们每次也需要完整读取整个数据库文件，而且每次更新都需要重新写回整个数据库到文件。另一方面，文本文件的方法假定它写入文件的数据分隔符不会出现在要存储的数据中：例如，如果字符=>出现在数据中，方案将失败。我们可以通过生成XML文本来代替文本文件中的记录来解决这个问题，使用Python的XML解析工具（本文稍后将要讨论）来重新加载; XML标签将避免与实际数据的文本发生冲突，但创建和解析XML会大大增加程序的复杂性。也许最糟糕的是，格式化的文本文件方案已经很复杂而不是一般的了：它与字典嵌套字典绑定在一起，并且不经过很大的扩展就无法处理其他任何东西。 如果有一种通用工具可以将任何类型的Python数据转换为可以在一个步骤中保存在文件中的格式，那将会很不错。

这就是 `pickle` 模块所做的事情。`pickle` 模块将内存中的Python对象转换为 `序列化的字节流` - 可以写入任何文件类对象的字节串。在序列化字节流的情况下，pickle模块也知道如何重建内存中的原始对象：能够找回完全相同的对象。从某种意义上说，`pickle`模块取代了专有数据格式 - 串行格式对于任何程序来说都是一般而且高效的。 通过 `pickle`，在永久存储对象时不需要手动将对象转换为数据，也不需要手动解析复杂的格式以将其恢复。 `pickle` 在精神上与XML表示类似，但它更具Python特性，并且更易于编码。


```python
# make_db_pickle.py
from initdata import db
import pickle

dbfile = open('people-pickle','wb')
pickle.dump(db,dbfile)
dbfile.close()
```
当以上脚本运行时，整个数据库的内容将被存储在名为 `people-pickle` 文件中。 `pickle` 模块处理将 object 对象转化为 string 的工作。下面的脚本 `dump_db_pickle.py` 展示了访问 pickled 数据库，我们只需打开文件并将其内容传递回 pickle 以从其序列化的字符串重新创建对象。
```python
# dump_db_pickle.py
import pickle
dbfile = open('people-pickle','rb')
db = pickle.load(dbfile)
for key in db:
    print(key,'=>\n ',db[key])
print(db['sue']['name'])
```
数据库更新如下：

```python
# update-db-pickle.py
import pickle
dbfile = open('people-pickle', 'rb')
db = pickle.load(dbfile)
dbfile.close()
db['sue']['pay'] *= 1.10
db['tom']['name'] = 'Tom Tom'
dbfile = open('people-pickle', 'wb')
pickle.dump(db, dbfile)
dbfile.close()
```
> 注意记录在内存中更改后整个数据库是如何写回文件的，就像手动格式化的方法一样; 对于非常大的数据库来说，这可能会变慢，但我们暂时忽略它

### 2.3.使用每个记录的 pickle 文件
正如我们早些时候提及的，到目前为止上面的例子的一个潜在的弊端是对于非常庞大的数据库，存取会变得异常慢，因为仅仅更新一条记录，都需要将整个数据库导出和重写，这种方法很浪费时间。我们可以通过将数据库中的每一条记录存储在各自的文件中以改善这个问题。
此方法不予展示

### 2.4.使用 Shelves
如上一节所示，将对象`Pickling`到文件是许多应用程序的最佳方案。 实际上，一些应用程序使用网络套接字中的Python对象作为网络协议（比如SOAP和XML-RPC Web服务体系结构（在Python中也支持，但比pickle更重））的简单替代方法。此外，假设您的文件系统可以处理您需要的文件数量，那么为每个文件挑选一个记录也可避免为每次更新加载和存储整个数据库。 但是，如果我们确实需要对记录进行键控访问，那么Python标准库提供了更高层次的工具：`shelves`。

`shelves` 自动从 以key访问的文件系统中存取对象。它们的行为非常像必须打开的字典，并且在每个程序退出后它们仍然存在。因为他们使我们能够访问存储的记录，所以不需要为每个记录手动管理一个flat文件。 `shelves`系统会自动分割存储的记录，提取并更新仅仅需要访问和更改的记录。通过这种方式，`shelves` 可以提供类似于每条记录的pickle文件的实用程序，但它们通常更容易编码。

`shelves` 和 `pickle` 接口一样简单：它与字典一样，但有额外的 open 和 close 调用。实际上，对于你的代码来说，`shelves` 确实看起来似乎是持久对象的持久字典; Python完成将内容映射到和从文件d的所有工作。下面我们通过 `shelves` 创建数据库：
```python
# make_db_shelve.py
from initdata import bob, sue
import shelve
db = shelve.open('people-shelve')
db['bob'] = bob
db['sue'] = sue
db.close()
```
这个脚本创建了文件people-shelve.bak, people-shelve.dat, 和 people-shelve.dir。他们是数据库的一部分，任何一个文件都不应被删除。下面是读取数据库的内容
```python
# dump_db_shelve.py
import shelve
db = shelve.open('people-shelve')
for key in db:
    print(key, '=>\n ', db[key])
print(db['sue']['name'])
db.close()
```
我们在这里仍然维护一个字典的字典，但是顶层的字典是一个 `shelve` 映射到文件中。 当你访问`shelve`的key时会发生很多事情 - 它在内部使用pickle来序列化和反序列化存储的对象，并且与键控访问文件系统进行接口。从你的角度来看，这只是一个持久的字典。
```python
# update_db_shelve.py
from initdata import tom
import shelve
db = shelve.open('people-shelve')
sue = db['sue'] # fetch sue
sue['pay'] *= 1.50
db['sue'] = sue # update sue
db['tom'] = tom # add a new record
db.close()
```
> `shelve.open` 也有一个 `writeback` 的参数，如果传递为true，那么会导致所有从 shelve 加载的记录被缓存在内存中，并且会自动化的写回shelve当他close时。这可以避免手动回写更改，但会消耗内存并使 close 关闭

## Step 3:Stepping Up to OOP
此时，我们创建了一个记录的数据库：`shelve` 足以完成基本的数据存储任务。 现在，我们的记录被表示为简单字典，它比列表（通过关键字而不是位置）提供对字段更容易理解的访问。 然而，程序随着时间的推移，字典仍然有一些限制可能变得更加严峻。

首先，我们没有集中的地方来收集记录处理逻辑。 举例来说，提取姓氏并给与增长可以通过以下代码完成：
```python
import shelve
db = shelve.open('people-shelve')
bob = db['bob']
bob['name'].split()[-1] # get bob's last name
# 'Smith'
sue = db['sue']
sue['pay'] *= 1.25 # give sue a raise
sue['pay']
# 75000.0
db['sue'] = sue
db.close()
```
这种方式对于简短的程序来说已经足够了，但是如果我们需要更改获取和修改数据库内数据的实施方式，我们也许需要更新程序中多出代码。事实上，即使找到所有这些神奇的代码片段也可能是一个挑战。 在不止一个地方对此进行硬编码或剪切和粘贴冗余逻辑几乎总是会重复地出现。以某种方式隐藏 - 也就是`封装` - 这些代码比较好。 模块中的功能将允许我们在单个地方执行这些操作，从而避免代码冗余，但仍然不会自然地将它们与记录本身相关联。 我们想要的是将处理逻辑与存储在数据库中的数据绑定的方式，以便更易于理解，调试和重用。

使用字典记录的另一个缺点是它们很难随着时间的推移而扩展。 例如，假设对于不同类型的人来说，数据字段集合或收入类型是不同的（也许一些人每年获得奖金，有些人不会获得奖金）。 如果我们需要扩展我们的程序，就没有自然的方式来定制简单的字典。 为了未来的发展，我们也希望我们的软件以自然的方式支持扩展和定制。

如果您已经深入研究过Python，那么您可能已经知道这是其OOP支持开始变得有吸引力的地方：

 * 结构体：使用OOP，我们自然可以将处理逻辑与记录数据相关联 - 类提供了将逻辑和数据组合在一个程序包中的程序单元，以及允许轻松分解代码以避免冗余的层次结构。
 * 封装：通过OOP，我们还可以完成诸如名称处理和增加薪酬等细节，我们可以自由地更改方法实现而不会破坏用户。
 * 定制化：与OOP一起，我们有一条自然的成长之路。 可以通过编写新的子类来扩展和定制类（继承），而不必更改或破坏已经运行的代码。

