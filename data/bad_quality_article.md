# Python入門

Pythonは簡単で人気のプログラミング言語です。使い方を覚えましょう。

## 変数

変数にはいろんな値を入れられます。

```python
x = 10
name = "太郎"
```

## リスト

複数の値をまとめて扱えます。

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[0])
```

## for文

繰り返し処理ができます。

```python
for i in range(5):
    print(i)
```

リストも繰り返せます。

```python
fruits = ['apple', 'banana', 'orange']
for fruit in fruits:
    print(fruit)
```

## if文

条件分岐ができます。

```python
x = 10
if x > 5:
    print("大きい")
```

## 関数

処理をまとめられます。

```python
def greet(name):
    print("こんにちは、" + name)

greet("太郎")
```

## 辞書

キーと値のペアで管理できます。

```python
person = {'name': '太郎', 'age': 25}
print(person['name'])
```

## クラス

オブジェクト指向プログラミングができます。

```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        print("ワン！")

dog = Dog("ポチ")
dog.bark()
```

## エラー処理

エラーが起きても大丈夫。

```python
try:
    result = 10 / 0
except:
    print("エラーです")
```

## ファイルを扱う

ファイルの読み書きもできます。

### ファイルを読む

ファイルを読むにはopen関数を使います。

```python
f = open('data.txt', 'r')
content = f.read()
print(content)
f.close()
```

これでファイルの中身が読めます。

### ファイルに書き込む

書き込みもopen関数です。

```python
f = open('output.txt', 'w')
f.write('Hello, World!')
f.close()
```

'w'モードで書き込みができます。

### 1行ずつ読む

大きいファイルは1行ずつ読むと良いです。

```python
f = open('large_file.txt', 'r')
for line in f:
    print(line)
f.close()
```

### ファイルの存在確認

ファイルがあるか確認できます。

```python
import os
if os.path.exists('file.txt'):
    print('ファイルあります')
```

### CSVファイルを読む

CSVファイルも読めます。

```python
import csv
f = open('data.csv', 'r')
reader = csv.reader(f)
for row in reader:
    print(row)
f.close()
```

## まとめ

Pythonの基本を紹介しました。変数、リスト、for文、if文、関数、クラス、エラー処理、ファイル操作などがあります。これらを使えば色々なプログラムが作れます。頑張って勉強してください。

