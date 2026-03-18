if条件判断

格式:
if	要判断的条件 :
		条件成立时,要执行的操作

elif	要判断的条件 :
		条件成立时,要执行的操作

else :
		要执行的操作



注意事项:

- 判断条件的结果一定要是布尔类型

- 不要忘记判断条件后面的冒号(:)

- if语句里面的代码块,需要在前方缩进空格(建议4个空格),通过缩进来描述代码的层级关系(归属)

- elif ,else不是必须的,elif可以有多个,else必须放在最后

  

---

pass是一个空语句,起语法占位作用,eg:

```python
if a>1:
    pass
```



---

match-case模式匹配:

```python
a=int(input('请输入一个数:'))
match a:
	case 1:
		pass
	case 2:
		pass
	case _:#匹配其他情况
		pass
```

---

