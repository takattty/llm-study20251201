# マルチモーダル入力
```sh
-> % time uv run python3 practice/genai_ver/d1.py
この画像は、プレゼンテーションやイベントのタイトルのように見えます。表示されているテキストは以下の通りです。

* **LLM勉強会** (上部左、および中央の大きなテキスト)
* **LLM設計を学ぼう** (中央、大きなテキスト)
* **Tomoki Yoshida (birder)** (中央、名前)
* **DeNA** (中央、所属)
* **AI技術開発部AIイノベーショングループ** (中央、部署名)
* **2025-12-01 (月) 13:00-16:00** (中央、日時)
* **Tomoki Yoshida (birder) - DeNA** (下部左、クレジット)

全体として、これは「LLM勉強会」というタイトルのイベントで、「LLM設計を学ぼう」というテーマで、Tomoki Yoshida氏（DeNA所属）が、2025年12月1日（月）の13時から16時まで講演する内容を示していると考えられます。
uv run python3 practice/genai_ver/d1.py  0.34s user 0.08s system 9% cpu 4.587 total
```

# グラウンディング
```sh
-> % time uv run python3 practice/genai_ver/d2.py
東京の今日の天気は晴れです。現在の気温は8℃（体感温度は7℃）で、湿度は77%です。

日中の最高気温は15℃から18℃、最低気温は1℃から3℃の範囲で予想されています。 降水確率は約10%です。 風は西南西から6km/h、突風は9km/hと予想されています。
uv run python3 practice/genai_ver/d2.py  0.35s user 0.05s system 6% cpu 6.092 total
```