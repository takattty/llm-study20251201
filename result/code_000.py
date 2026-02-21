import matplotlib.pyplot as plt
import numpy as np

# xの値の範囲を定義
x = np.linspace(-10, 10, 400)

# yの値を計算
y = x**2

# グラフをプロット
plt.figure(figsize=(8, 6)) # グラフのサイズを設定
plt.plot(x, y, label=r'$y=x^2$', color='blue') # プロットとラベル、色を設定

# グラフのタイトルと軸ラベルを設定
plt.title('Graph of $y=x^2$', fontsize=16)
plt.xlabel('x-axis', fontsize=12)
plt.ylabel('y-axis', fontsize=12)

# グリッドを追加
plt.grid(True)

# 凡例を表示
plt.legend(fontsize=10)

# グラフをファイルに保存
file_name = 'parabola_graph.png'
plt.savefig(file_name)
plt.close() # メモリを解放

print(f"グラフ '{file_name}' が正常に生成され、保存されました。")
