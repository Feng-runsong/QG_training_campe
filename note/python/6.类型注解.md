类型注解

- 类型注解:Python中的一种语法特性，用于明确标识变量，函数参数和返回值的数据类型，从而使代码更清晰，更安全，更易维护。
- 类型推断:Python解释器自动推断出变量，表达式或函数返回值的数据类型的能力，而无需开发者显式声明。
  注意：在对变量进行直接赋值，或者涉及到变量的运算，容器的推导等场景时，解释器会自动推导出变量的类型。
- 类型注解的写法:
  变量：数据类型(如 a:int)
- 常见类型的写法:

1. int , float , bool , str , None , list , set , tuple , dict
2. str | in  |  ...     (表示n种都可)

- 为什么要使用类型注解，有什么好处呢:
  a.代码结构更清晰，代码逻辑更安全，易维护
  b.更准确的代码自动提示
  c.提前发现代码潜在问题
- 如果对变量直接赋值，变量运算等场景，Python会自动进行类型推断
  Python是动态类型语言，添加的类型注解只是提示，并不是强制约束!!!

- 函数中类型注解的语法

  ```python
  def calc_data(scores: list[int])->tuple[int,int,float]
  max_V = max(scores)		
  min_v = min(scores)
  avg_v - sum(scores) / len(scores)
  return max_v,min_v,avg_v
  ```

  