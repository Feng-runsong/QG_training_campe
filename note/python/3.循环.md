while循环:
格式:

while	条件表达式:
			条件成立时,执行的操作

else:
			循环正常结束时,执行的操作

eg:

```python
#1~100所有偶数累加之和
total=0
a=1
while a<=100:
    if a%2==0:
        total+=a
    else:
        print("a不是偶数")
    a+=1
else:
    print("循环结束")
print(f"1~100所有偶数累加之和为{total}")
```

注意事项:

- 条件表达式的结果为布尔类型
- 通过空格缩进表述层级关系
- 规划好循环终止的条件,否则将无限循环
- while True可无限循环
- else不是必须的

---

for循环:
格式:

for	元素	in	待处理数据集

​		循环体代码(对元素进行处理)

else:

​		不满足循环条件时,执行的操作,不是必须的

eg:

```python
#九九乘法表
for i in range(1,10):
    for j in range(1,i+1):
        print(f'{j}*{i}={i*j}',end="\t")
    print()
```

---

for循环与while循环的场景:

- while循环：用于在某个条件满足时一直循环，循环的次数通常是未知的，只知道循环开始/结束的条件。(关注的是循环的条件)
- for循环：用于对一个已知的数据集进行遍历或已知次数的循环。(关注的是遍历每一个元素)

---

range语句

- 作用：生成指定规则的数字序列
- 用法1:range(end)-〉获取一个从e开始，到end结束的数字序列(不含end本身).range(5)获取的数据就是 0,1,2,3,
- 用法2:range(start,end)-〉获取一个从start开始，到end结束的数字序列(不含end本身).range(2,8)获取的数据就是 2,3,4,5,6,7
- 用法3:range(start,end,step)-〉获取一个从start开始，到end结束的数字序列，step步长(不含end本身).range(0,10,2)获取的数据就是 0,2,4,6,8

---

random.randint(1,100)可用于生成1~100的随机数(包括1,100)

eg:

```python
import random

# 方法1：randint - 包含两端
a = random.randint(1, 100)      # 可能得到 1 或 100

# 方法2：randrange - 不包含结束值
b = random.randrange(1, 101)     # 等价于 randint(1, 100)
c = random.randrange(1, 100)     # 范围是 1~99，不包含100

# 方法3：uniform - 生成浮点数
d = random.uniform(1, 100)       # 生成1.0到100.0之间的浮点数
```

---

- break关键字的作用:
  不能够单独书写，只能出现循环中，表示结束，跳出的意思。
- continue关键字的作用:
  不能够单独书写，只能出现循环中，表示中断本次循环，直接进入下一次循环。

