文件操作入门

- 日常操作文件时，基本分为三步操作：打开，读/写，关闭。

  读文件:

  ```python
  # 1.打开文件
  f = open("resources/望庐山瀑布。txt","r",encoding="utf-8")
  
  # 2.读取文件
  content = f.read()
  print(content)
  
  # 3.关闭文件
  f.close()	
  ```

  写文件:

  ```python
  # 1.打开文件
  f = open("resources/静夜思。txt","w",encoding="utf-8")	
  
  # 2.写入文件
  f.write("窗前明月光，\n")
  f.write("疑是地上霜。\n")
  f.write("举头望明月，\n")	
  f.write("低头思故乡。\n")
  
  # 3关闭文件
  f.close()
  ```

编码：是将字符(文字，数字，符号)转换为计算机能够存储O处理的数字代码的规则系统，如：ASCII,GBK,UTF-8.
注意：如果操作完文件，并未调用close方法关闭文件，同时程序没有停止运行，那么这个文件将一直被Python程序占用，无法操作。

---

CSV

- CSV:(Comma-Separated Values，逗号分隔值)，是一种简单，通用的文本文件格式，用于存储表格数据，可以直接使用Excel打开。

- 一般方式读/写csv文件:

  ```python
  # 写
  with open("csv_data/01.csv","w",encoding-"utf-8")as f:
  	f,write("姓名，年龄，性别，爱好\n")#写入表头
  	f.write("小李，18，文，Python\n")#写入教据
      f.write("小，18，男，football,Java\n")
  	f.write("小米，18，男，C++\n")
      
  # 读
  with open("csv_data/01.csv","r",encoding-"utf-8")as f:
  	for line in f:	
  	print(line.strip())
  ```

  

- 导入csv模块读/写csv文件:

  ```python
  import csv
  
  #写
  with open("csv_data/02.csv","w",encoding="utf-8", newline="") as f:
  writer =csv.DictWriter(f,fieldnames=["姓名","年龄","性别","爱好"]) 
  writer.writeheader()#写入表头
  writer.writerow({"姓名":"小王","年龄":18,"主别":"男","爱好":"football,Java"})#写入数据 writer.writerow({"姓名":"小李","年龄'':18,"性别":"女","爱好":"Python"}) writer.writerow({"姓名":"小张","年龄":18,"性别":"男","爱好":"C++"})
  writer.writerow({"姓名":"涛哥","年龄":19,"性别":"男","爱好":"Python,Java"})
  
  #读
  with open("csv_data/02.csv","r",encoding="utf-8") as f:
  	reader = csv.DictReader(f)
  	for row in reader:
  		print(row)I
  ```

  