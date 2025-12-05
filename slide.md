---
marp: true
theme: default
paginate: true
header: 'LLM勉強会 〜基礎からエージェント設計まで〜'
footer: 'Tomoki Yoshida (birder)🐦️ - DeNA'
style: @import "styles/slide.css"
---

<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# LLM勉強会
## 基礎からエージェント設計まで
### Tomoki Yoshida (birder)🐦️
DeNA
AI技術開発部AIイノベーショングループ

2025-12-01 (月) 13:00-16:00

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# みなさんの3時間絶対に無駄にしません！
本気で準備しました！
どうか今日だけは内職ご遠慮ください🙏

---

# 今日の流れ
- イントロダクション
- 前半
    - 知識
    - 実践演習（ハンズオン）
- 後半
    - 知識
    - 実践演習（ハンズオン）
- 案件の実例紹介

→ [詳細時間配分](./README.md)

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# イントロダクション
Slackでぜひ盛り上がってください！

---
# こんなこと思ったことありませんか？
- 難しいタスクのプロンプトをチューニングしているけどうまくいかない
- Web版Gemini/ChatGPTとAPI実装時の差分がわからないので、Webでやった技術検証をどこまで信じていいかわからない
- DeepResearch/NotebookLMってすごいけど、内部どうなっているの？
- **LLMプロダクトのパーソナライズ**って何を考えればいいの？

今日はこれらの解決を目指します！

---

# 背景
- AIの普及で非エンジニアでも誰でもなんでもできる時代になった
- LLMを使うだけなら**APIを呼ぶだけ**（非エンジニアでも簡単）
- 案件の数に比べて圧倒的に**AIエンジニアの数が少ない**

# 狙い
- 誰でも**LLMを組み合わせた設計**をイメージできる
- 簡単なPoCを誰でもできる
- プロダクトの**フィードバックループの設計イメージ**ができる

---
# 今日みなさんが目指す姿
<div class="grid cols2">

<div>

## エンジニア
- <span class="red">**適切に問題を分解し、LLMを組み合わせて問題を解ける**</span>
- コンテキストエンジニアリングできる
- データを活用した設計ができる
- 今日の演習問題すべて解ける

→ **設計し、実装までできる**
</div>

<div>

## 非エンジニア
- <span class="red">**データを活用したプロダクト設計をイメージできる**</span>
- （AI）エンジニアの業務理解
- 用語や概念の理解
- 簡単なPoCならできる

→ **理解してイメージできる**
</div>
</div>

---

# 環境設定
- [別資料へ](./setup.md)
- [レポジトリ](https://github.com/DeNA/llm-study20251201/)

# 情報の取り扱い注意
## 今日の勉強会では業務データ入力禁止
## 後半演習の一部でn8nを使いますが見られても良いデータのみ可

---

<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 知識 ～前半～

---
# いろんなLLM
<div class="small grid cols3">
<div>

- [OpenAI](https://openai.com/ja-JP/)
    - GPT-5.1
    - GPT-4o
    - o3
    - o1
</div>

<div>

- Google
    - Gemini-2.5-Pro
    - Gemini-2.5-Flash
    - Gemini-2.5-Flash-Lite
</div>
<div>

- [Anthropic](https://www.anthropic.com/)
    - Claude Opus 4
    - Claude Sonnet 4
</div>

</div>


## 何がどう優れているの？どう違うの？
「LLM Leaderboard」で検索！
<div class="small">

- https://artificialanalysis.ai/leaderboards/models
- https://www.vellum.ai/llm-leaderboard
- https://lmarena.ai/leaderboard
</div>

---
# LLMの仕組み
## Next Token Prediction
次のカッコに入るのは何？
<p class="text-center">例：This is a (　　　)</p>
を解いている

![](fig/next_token_prediction.svg)


---

<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# こんなのでうまく答えられるの？

---

# Instruction Tuning
- 指示に従うようにするためのファインチューニング
![](fig/instruction_tuning.svg)

- [オープンな](https://huggingface.co/models?other=LLM)LLMで`-Instruct`や`-it`って付いているのはこれ

---

# Reasoning / Thinking とは？
- **推論/思考してから応答**するように学習されている（GPT-5, o1, Gemini-2.5-Pro等）
- 推論/思考が無いモデルはそのまま応答を出力（GPT-4o, Gemini-2.5-Flash-Lite等）

[DeepSeek-R1](https://arxiv.org/pdf/2501.12948)では思考を`<think></think>`で出力後、実際の応答が返ってくる

|  | 内容 |
| :---: | :--- |
| **入力** | `日本の首都は？` |
| **出力** | `<think>ユーザーは日本の首都について質問している。これは事実に基づく知識（Fact-based QA）である。私の知識によれば、日本の首都は東京である。</think>東京です。` |

---

# プロンプトエンジニアリング

## 基本テクニック
<div class="grid cols2">
<div>

- **Markdown/XML**記法で書く
- **構造化出力**を使う
- **適切な単位でプロンプトを分ける**
- **入出力例を与える（Few-shot）**
- ステップの明示（Chain of Thought）
- 理由を説明させてから回答させる

</div>

<div>

- 役割付与
（「あなたは優秀な〇〇です」）
- 否定語の代わりに肯定文
（「しないで」→「禁止する」）
- ハルシネーション対策（「答えがない場合、無理に回答は禁止します」）

</div>

</div>

これはMUSTですが覚えるだけ

---


<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# プロンプトチューニングでうまくいかないときに...
## 指示をどんどん足しまくらないで！！！
## AIに適当に修正させないで！！
（修正させたなら必ず全部自分で見て）

---

# プロンプトの洗練
うまく動かない時、指示を足すのではなく、**一度全体を見直すことが大切**
- **重複語彙** / **冗長な表現**の削除
- 重要な指示は前方か後方へ
- 改行位置を意味のあるまとまりで調整
- 長い文を箇条書きで整理する
- 重要な部分にだけ強調`**`を使う

無駄に長いプロンプトは、コストと応答時間の増加、**内容の把握が困難に**なる

---


<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 良い例と悪い例をいくつか紹介


---

# 悪いプロンプト例1

```
# 指示
新入社員向けのビジネスマナー研修で使う、プレゼンテーション資料（1時間枠）の構成案を作成してください。

## 研修の目的
この研修のゴールは、新しく入社した社員たちが社会人としての基本的なマナーを身につけることです。
彼らが学生気分を払拭し、プロフェッショナルとして振る舞えるようになることが重要です。
対象は新入社員なので、とにかく分かりやすく、平易な言葉で説明することが求められます。

## ターゲット層
対象者は、当然ながら新卒入社の社員です。
彼らはビジネスの現場経験がまったくないことを前提に資料を作る必要があります。
したがって、専門用語や業界用語は絶対に使わず、具体的な事例をたくさん出して説明するようにしてください。
新入社員は集中力が続きにくいので、一方的な講義にならないよう工夫も必要です。

## 資料で扱うべき内容
資料全体は1時間程度で終わるようにしてください。
内容は、社会人としての基本である「挨拶と言葉遣い」「正しい身だしなみ」「電話応対の基本」「ビジネスメール作成のルール」を網羅的に含めてほしいです。
あと、これが一番大事なのですが、昨今の情勢を鑑み、情報セキュリティとコンプライアンスの重要性を理解してもらうため、
個人情報の取り扱いやSNS利用に関する簡単なクイズを、絶対に資料の最後に入れてください。これは必須項目です。
彼らが飽きないように、途中で簡単なグループワークやディスカッションを入れる案も欲しいです。

## トーン＆マナー
新入社員が萎縮しないよう、基本的には親しみやすいトーンがいいですが、ビジネスマナーという真面目な内容を教える場なので、ある程度の緊張感も必要です。
堅苦しすぎず、かつ馴れ馴れしくない、バランスの取れた文体でお願いします。新入社員が飽きずに最後まで参加できるような雰囲気作りが大切です。
```

---
# 先程のプロンプトの悪いところ

#### 同じ指示の重複
→ 「新入社員向け・分かりやすく・専門用語NG」という指示が、`## 研修の目的` と `## ターゲット層` に重複して存在している。（セクション分けしているのは良いが、）同じような内容を何箇所にも書いてプロンプトが無駄に膨らんでしまう

#### 重要な指示が真ん中に来ている
→ 最も厳守すべき「コンプライアンスに関するクイズを絶対に入れる」という指示が、プロンプトの真ん中に埋もれて、無視されやすい

#### 長々と書いている
→ 重要な指示が効きにくい上、<span class="red">**人間が把握できなく**</span>なりチューニングできなくなる

---

# 改善したプロンプト例1

```
# 指示
新入社員向け「ビジネスマナー研修（1時間）」のプレゼンテーション資料の構成案を作成してください。

# 必須要件
資料の最後に、必ず**「情報セキュリティとコンプライアンス（個人情報、SNS利用）に関するクイズ」を設ける**こと。

# 研修の概要
- ターゲット: 新卒社員（ビジネス経験ゼロ）
- 目的: 社会人としての基本マナー習得、プロ意識の醸成（脱・学生気分）
- トーン: 堅苦しすぎず、親しみやすいが緊張感も保つ

# 資料で扱う内容
- 挨拶と言葉遣い
- 身だしなみ
- 電話応対の基本
- ビジネスメールのルール

# 構成上の指示
- 専門用語は使用禁止。具体的な例を多用すること。
- 一方的な講義を避け、飽きさせない工夫（例：グループワーク案）を盛り込むこと。
```


---


<div class="grid cols2">


<div>

# 悪い例2

```
# 指示
来週開催する社内AI勉強会について、
告知文（Slack投稿用）を作成してください。

# 記載事項
* **目的:**
    * 全社員のAIリテラシー向上と、業務効率化のアイデア発見。
* **日時:**
    * 12月1日（月）13:00〜16:00。この日時は絶対に間違えないでください。
* **場所:**
    * オンライン。URLは別途案内することを記載。
* **対象者:**
    * 全社員（エンジニア以外も歓迎）。
* **内容:**
    * 「ChatGPTの基本的な使い方」と「現場での活用事例紹介」。
* **補足:**
    * この勉強会は参加必須ではなく、あくまで任意参加であることを明記してください。
```

- 冒頭の同じ1文なのに無駄な改行
- 箇条書き項目をすべて強調（AIに書かせるとこうなる）

</div>


<div>

# 改善例2

```
# 指示
来週開催する社内AI勉強会のSlack投稿用告知文を作成してください。

# 記載事項
- 目的: 全社員のAIリテラシー向上と、業務効率化のアイデア発見
- 日時: **12月1日（月）13:00〜16:00**（日時厳守）
- 場所: オンライン（URLは別途案内）
- 対象者: 全社員（エンジニア以外も歓迎）
- 内容: 「ChatGPTの基本的な使い方」と「現場での活用事例紹介」
- 補足: この勉強会は**任意参加であることを必ず明記**すること
```

- 意味のない改行を削除
- 重要部分だけ強調
- 肯定文に変更

</div>

</div>

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 実践演習（ハンズオン）〜前半〜
- **穴埋め問題**になっている`./practice/`を編集して進めてみよう
- `uv run python practice/genai_ver/a1.py`のように実行できます
- 困ったらAIに聞いたり、答えの`./src/`を見ながら進めてOK

<div class="small">

**エンジニア向け**: Google公式SDKの`genai_ver`とLangChainの`langchain_ver`を用意しています。速く終わったら両方見てみよう。
</div>

---

# 基礎: APIを呼ぶ
#### 演習A1: 入力された文から趣味を単語で抽出してみよう
→ `./practice/genai_ver/a1.py`を埋める

#### 演習A2: 温度を調整して出力の差を感じよう
→ `./practice/genai_ver/a2.py`を埋める

1. いくつかキーワードを与えて小説を書いてもらおう
2. 文を与えて翻訳させてみよう

- [温度を調整](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-generation-parameters?hl=ja#temperature)して、何回か実行してみよう
- どんなタスクにどんな温度が適切かわかりましたか？

---

# 基礎: APIを呼ぶ

#### 演習A3: 思考のON/OFFを切り替えてレイテンシの差を感じよう
1. 思考モデルで[思考](https://ai.google.dev/gemini-api/docs/thinking?hl=ja)を切ってみよう
2. 思考過程を表示してみよう

#### 演習A4: 連続的な対話の履歴を管理しよう
- 連続的な会話でちゃんと覚えているかどうか確認しよう
- LLMには**毎回全ての会話履歴が送られている**ことを体験する


<span class="small">参考：マルチターンは[SDKで用意されている](https://ai.google.dev/gemini-api/docs/text-generation?hl=ja#multi-turn-conversations)が、プロダクト実装では使わないと思う</span>

---

# 構造化出力を体験する

### 演習B: ECサイトに寄せられたコメントを処理する
入力文サンプル:
```
スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。
```
入力サンプルはいろんなパターンで試してみよう（人力 or Web Gemini）

#### 演習B1: コメントがポジティブかネガティブかクラス分類してみよう
- ニュートラルなコメントをどうするかも考えてみよう
- 参考: [公式ドキュメント](https://ai.google.dev/gemini-api/docs/structured-output?hl=ja&example=recipe)

---

# 構造化出力を体験する
#### 演習B2: コメントから「商品名」 「ポジティブな点」 「ネガティブな点」を抽出して「5段階のスコア」をつけてみよう
- 複数項目といろんな型を体験する


#### 演習B3: コメントをカテゴリ別に分類し、各カテゴリでポジティブ/ネガティブな点を抽出してみよう
- カテゴリ（機能、品質、価格、デザイン、使い勝手）ごとに、ポジティブな点とネガティブな点を抽出
- ネスト構造化出力を体験する

---

# 複数LLMに分ける
- 複雑なタスクを1つのLLMにやらせると、性能が足りなかったり、速度が落ちる
- タスクを分解して、複数LLMを組み合わせる体験をしよう

### 演習C: 技術記事のドラフトを多角的に分析・改善するシステムを作ろう

機能要件:
<div class="flex cols2 small">
<div>

- **記事の評価**
   - 技術的正確性（コードの妥当性、説明の正確さ）
   - わかりやすさ（初心者への配慮、説明の丁寧さ）
   - 構成・論理展開（目次構成、話の流れ）
   - SEO最適化（タイトル、見出し、キーワード）
</div>

<div>

- **問題点の特定と改善案の生成**
- **修正版の作成**
- **フィードバックループ**

入力: 技術記事のドラフト（マークダウン形式）
出力: 評価結果、改善提案、修正版
</div>

</div>

</div>

これを見たときあなたならどう設計しますか？

---

# 複数LLMに分ける

<div class="flex grid2 small">
<div>

たとえばこんな感じ
- 機能要件の
**問題点の特定と改善案の生成**
は評価側に根拠として含める
- **問題点の特定**を評価側で
**改善案の生成**は修正側で多段など
設計思想によってさまざま

また、他のLLMを分けるケースとして
**場合分けがプロンプトに入る場合**、
も挙げられる。
（プログラム側で制御しよう）
</div>
<div>

![width:700](fig/c.svg)

</div>
</div>

---

# 複数LLMに分ける

#### 演習C1: 複数の評価軸を別々で処理してみよう
- 独立している処理は分割できる
- 逐次実行と並列実行の実行時間を比較してみよう (エンジニアのみ)

#### 演習C2: 評価結果を使って、記事を修正してみよう
- C1の4つの評価結果を受け取って記事を修正

#### 演習C3: 修正・評価ループを作る（エンジニアのみ）
- C1を修正が必要かどうかも出力させてループを抜けるルートを作る
- 最大3回まで繰り返す（**無限ループ注意**）

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 解説A
## （ネタバレしたくない方はここで戻ってください）
ソースコード:
- genai: [A1](./src/genai_ver/a1.py), [A2](./src/genai_ver/a2.py), [A3](./src/genai_ver/a3.py), [A4](./src/genai_ver/a4.py)
- LangChain: [A1](./src/langchain_ver/a1.py), [A2](./src/langchain_ver/a2.py), [A3](./src/langchain_ver/a3.py), [A4](./src/langchain_ver/a4.py)

---

# 解説A1~A3: 基本, 温度, 思考の設定（genai）
```python
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

client = genai.Client(vertexai=True)

input_text = "私はサッカーを趣味にしています。"
response = client.models.generate_content(
    model="gemini-2.5-flash", # A1: contentsにプロンプトを渡す（pythonの文法で変数は｛}で埋め込める）
    contents=f"""入力文から趣味を単語で抽出してください。
入力文: {input_text}
""",
    config=GenerateContentConfig(
        temperature=0.1,           # A2: 温度の調整
        thinking_config=ThinkingConfig(
            thinking_budget=0,     # A3: 思考の上限を0にする
            include_thoughts=True, # A3: レスポンスに思考過程を含める（thinking_budgetが0の場合は使えない）
        ),
    ),
)
```
このプロンプトを変えて実行するだけでWeb版Geminiとの差分を吸収できますね！

---

# 解説A1~A3: 基本, 温度, 思考の設定（LangChain）
```python
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate

llm = ChatVertexAI(
    temperature=1,         # A2: 温度の調整
    model="gemini-2.5-flash",
    thinking_budget=0,     # A3: 思考の上限を0にする
    include_thoughts=True, # A3: レスポンスに思考過程を含める（thinking_budgetが0の場合は使えない）
)
prompt = PromptTemplate.from_template( # A1: プロンプトを渡す（{}は自動で変数化される）
    """入力文から趣味を単語で抽出してください。
入力文: {input_text}"""
)
chain = prompt | llm

# 実行時に変数を渡す
result = chain.invoke({"input_text": "私はサッカーを趣味にしています。"})# A1: 実行時に変数へ代入できる
print(result.content)
```
LangChainだと事前に定義した変数を呼び出し時に埋める書き方が自然にできる

---
# 解説A4: 対話（genai）

```python
history = []
while True:
    user_input = input("入力してください: ")
    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=history,
        config=types.GenerateContentConfig(system_instruction="必ず英語で応答してください"),
    )

    history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    print(response.text)
```

同じセッションの対話は**毎回すべてLLMに入力されている**のを実感しよう
→ Web版Geminiで検証するときにコンテキストをリセットする大切さがわかりますね
（長くなるほど性能が落ちます）

---
# 解説A4: 対話（LangChain）

```python
llm = ChatVertexAI(model="gemini-2.5-flash-lite")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "必ず英語で応答してください"),
        MessagesPlaceholder(variable_name="history"),
    ]
)
chain = prompt | llm | StrOutputParser()

history = []
while True:
    user_input = input("入力してください: ")
    history.append(HumanMessage(content=user_input))
    response = chain.invoke({"history": history})
    history.append(AIMessage(content=response))
    print(response)
```

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 解説B
## （ネタバレしたくない方はここで戻ってください）
ソースコード:
- genai: [B1](./src/genai_ver/b1.py), [B2](./src/genai_ver/b2.py), [B3](./src/genai_ver/b3.py)
- LangChain: [B1](./src/langchain_ver/b1.py), [B2](./src/langchain_ver/b2.py), [B3](./src/langchain_ver/b3.py)

---

# 解説B1: 構造化出力（genai）
```python
from pydantic import BaseModel, Field
class CommentAnalysis(BaseModel): # 出力したい形式をクラスで定義する
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="判定結果。positive: ポジティブ、negative: ネガティブ、neutral: ニュートラル"
    )

input_text = "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。"
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=f"""次のコメントがポジティブかネガティブかニュートラルか判定してください。
`{input_text}`
""",
    config=GenerateContentConfig(
        response_mime_type="application/json",  # Json Output
        response_schema=CommentAnalysis,        # 構造化出力クラスを指定
    ),
)
comment_result = CommentAnalysis.model_validate_json(response.text)
```
プロンプトで出力を指示するのではなく、**APIとして構造化出力をサポート**している！

---

# 解説B1: 構造化出力（LangChain）
```python
from pydantic import BaseModel, Field
class CommentAnalysis(BaseModel): # 出力したい形式をクラスで定義する
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="判定結果。positive: ポジティブ、negative: ネガティブ、neutral: ニュートラル"
    )

llm = ChatVertexAI(model="gemini-2.5-flash-lite")
prompt = PromptTemplate.from_template(
    """次のコメントを分析して、商品名、ポジティブな点、ネガティブな点、5段階のスコアを返してください。
`{input_text}`
"""
)
chain = prompt | llm.with_structured_output(CommentAnalysis) # 構造化出力
result = chain.invoke(
    {
        "input_text": "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。"
    }
)
```
当然LangChainでもサポート。OpenAIでもOllamaでも同じ書き方できるのが嬉しい。

---

# 解説B2,B3: より複雑な構造化出力
```python
# 【B2】 str（文字列）の他にint（整数）も使える
class CommentAnalysis(BaseModel):
    product_name: str = Field(description="商品名")
    positive_points: str = Field(description="ポジティブな点")
    negative_points: str = Field(description="ネガティブな点")
    score: int = Field(description="5段階のスコア", ge=1, le=5)

# 【B3】 クラスを入れ子にもできる
class CategoryFeedback(BaseModel): # str（文字列）の他にint（整数）も使える
    category: Literal["機能", "品質", "価格", "デザイン", "使い勝手"] = Field(description="カテゴリ")
    positive_points: str = Field(description="そのカテゴリに関するポジティブな点")
    negative_points: str = Field(description="そのカテゴリに関するネガティブな点")
class CommentAnalysis(BaseModel):
    product_name: str = Field(description="商品名")
    categories: list[CategoryFeedback] = Field(description="カテゴリ別のフィードバック")
    overall_score: int = Field(description="5段階の総合スコア", ge=1, le=5)
```
任意の型を出力に定義できるので、「文字列で返ってきたらどうしよう」の心配が不要

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 解説C
## （ネタバレしたくない方はここで戻ってください）
ソースコード:
- genai: [C1](./src/genai_ver/c1.py), [C2](./src/genai_ver/c2.py), [C3](./src/genai_ver/c3.py)
- LangChain: [C1](./src/langchain_ver/c1.py), [C2](./src/langchain_ver/c2.py), [C3](./src/langchain_ver/c3.py)

---

# 解説C: 構造化出力の組み合わせ
<div class="small">

- C1: 各評価項目について次のような評価を出力させる
    ```python
    class Evaluation(BaseModel):
        """評価結果"""
        needs_revision: bool = Field(description="修正が必要かどうか")
        good_points: list[str] = Field(description="優れている点")
        bad_points: list[str] = Field(description="改善が必要な点")
    ```
    ```python
    # エンジニア向け: LangChainだと並列処理を楽に書ける
    parallel_chain = RunnableParallel({
        "technical_accuracy": create_evaluation_chain(TECHNICAL_ACCURACY_PROMPT),
        "clarity": create_evaluation_chain(CLARITY_PROMPT),
        "structure": create_evaluation_chain(STRUCTURE_PROMPT),
        "seo": create_evaluation_chain(SEO_PROMPT),
    })
    ```
- C2: レビュー結果をプロンプトに入れて修正させる
- C3: C1で出力した修正必要の有無に応じて終了基準を作ってループを作るだけ



</div>

---

<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 知識 ～後半～

---

<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# フィードバックループを持ち成長するプロダクト
## 作りたいですよね？

---

# LLM時代のデータ活用
## プロダクト全体の最適化
- **ファインチューニング（FT）**
- 強化学習（RL）
- プロンプト最適化

## <span class="red">ユーザー個人への最適化（パーソナライズ）</span>
- **コンテキストエンジニアリング**
- RAG

ユーザーごとにモデル保持するのは非現実的なので、基本このパターンになるはず

---

# モデル学習の種類とイメージ
STEP: 事前学習 → ファインチューニング → 強化学習

| 手法 | 例え | 学習のさせ方 |
| :---: | :---: | :--- |
| **事前学習** | 義務教育 | 言葉、計算、一般常識を学ぶ。まだ料理はできない |
| **ファインチューニング** | 料理学校 | 「このレシピ通りに作りなさい」と教わる <br>→ **基礎的な調理スキルと知識を身につける** |
| **強化学習** | 実地研修 | 客に出した料理に対して「美味しい」「塩辛い」と評価される → **客が喜ぶ味付けや、好まれる接客を身につける** |

LLMを使う多くの企業は、プロンプトチューニングとファインチューニングだけやる

---

# ファインチューニングと強化学習の比較

<div class="small">

| 比較項目 | **ファインチューニング** | **強化学習** |
| :---: | :--- | :--- |
| **主な目的** | **指示従順性の獲得**: 特定の形式や知識を教え込む | **人間との調和**: 安全性、有用性、ニュアンスを調整する |
| **データ形式** | **「入力」と「正解」のペア**<br>例：`Q:首都は?` `A:東京` | **回答の「比較」や「採点」**<br>例：`回答A > 回答B`、`GOOD/BAD`など |
| **学習の仕組み** | **次単語の予測 (Token Level)**<br>正解データと一言一句合わせようとする | **報酬スコアの最大化 (Sentence Level)**<br>文章全体としての良し悪しを評価 |
| **得意なこと** | ・新しい知識の注入<br>・JSONなど特殊形式の出力<br>・口調（キャラ付け）の固定 | ・嘘（ハルシネーション）の抑制<br>・有害な回答の回避<br>・「もっと丁寧に」など曖昧な指示への対応 |


プロンプトチューニングで限界ならファインチューニングが候補に入る。強化学習まで必要なケースは稀。
参考：[Geminiのファインチューニングは簡単にできる](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning?hl=ja)

</div>

---

## ファインチューニング
事前学習済みモデルを特定タスクに微調整する

![](fig/ft.svg)

低ランクの**小さな重みを付け加える**PEFT（Parameter-Efficient Fine Tuning）のLoRA（Low-Rank Adaptation）が主流

---

# 強化学習（理解しなくて良い。飛ばします）

<div class="flex">


![height:450](fig/human.svg)
<span class="tiny">強化学習でもLoRAを使う</span>

![height:450](fig/rl.svg)
<span class="tiny">RLHF (Reinforcement Learning from Human Feedback) / DPO (Direct Preference Optimization)</span>

</div>

---


<!-- タイトルのみページ番号スキップ -->
<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 本当に重要なのはここからです！！
## パーソナライズへ

---

# コンテキストエンジニアリングの必要性
## LLMの限界
- [コンテキストウィンドウ（入力上限）](https://ai.google.dev/gemini-api/docs/long-context?hl=ja)がある（小説8冊分とか入る）
- 詰め込みすぎると指示を無視したり、性能劣化する

↓ **LLMに与える情報を管理してあげる必要がある**
## コンテキストエンジニアリング
無数に増えていく（ユーザーの）情報を
- どう保存するか（そのまま？ラベル付け？集計？圧縮？）
- どう検索するか（最新N件？関連度？重要度？）

---
# プロダクト作りで気にするところ
![height:300](fig/context-engineering.svg)
- データ取得時の**検索クエリ** / データ保存時の**加工処理**が案件ごとの設計ポイント！

<div class="small">

このあとコンテキストエンジニアリングの一種とみなせるRAGの説明をしますが、一般的なRAGは[既にいろんなクラウドサービスが実装](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview?hl=ja)しています。非エンジニアは完全に理解する必要はありません。コンテキストエンジニアリングの理解をするための例として考えてください。
</div>

---

# RAG（Retrieval-Augmented Generation）
- 外部データを検索して応答する

典型的なRAGシステムの全体像：
![](fig/rag.svg)

- RAGはコンテキストエンジニアリングの一種と言える
- LLMは**応答インターフェースでしかない**（いかにうまく情報取ってこれるか勝負）

---

# RAGの構成要素: 1. クエリ拡張
- ユーザーの曖昧な入力を、LLM等を使って具体的かつ<span class="red">**検索しやすい形に変換**</span>する

<div class="grid cols2">
<div>

##### 簡単な文脈補完
```
USER: 社内の経費精算の締め切りはいつ？
AI: 月末です
USER: それを過ぎたらどうなる？
```
- `それを過ぎたらどうなる？`を検索しても関連ドキュメントを探せない
- `経費精算の締め切りを過ぎた場合のペナルティや対応`を検索する

</div>
<div>

##### 言い換えや解答予測
```
USER: PCが重いときの対処法は？
```
- `PC 動作 遅い 対処`、`システム パフォーマンス 低下 原因`、`メモリ不足 解消方法`、`CPU使用率 高い`などを並列で検索して結果を統合する


</div>

</div>

---

# RAGの構成要素: 2. ハイブリッド検索
- <span class="red">**DBの情報すべてLLMに渡すのは無理**</span>なので、LLMに渡す情報の絞り込み

**全文検索**: 文字列完全一致で検索（インデックスで高速化）
**ベクトル検索**:
<div class="grid cols2">

<div>

##### **Embedding**: 文字列からベクトル空間へ

![](fig/embedding.svg)
</div>

<div>

##### **ベクトル検索**: 大量のレコードから近い表現を高速に検索できる（近似最近傍探索）

![](fig/vector.svg)

</div>

<div>

---

# RAGの構成要素: 3. リランキング 4. グラウンディング
**3. リランキング**: <span class="red">**さらなる絞り込み！**</span>
- 検索でヒットした多数の候補から、本当に関連する文書を**高精度なモデル**で並び替え、上位のものだけを抽出
- 高精度なモデル
    - **クロスエンコーダー**（入力: 質問と文書のペア, 出力: 関係度スコア）
    - 多段階にするならLLMが使われることも

**4. 応答 + グラウンディング**:
- 抽出した情報をコンテキストに入れて、ユーザーの質問に応答
- **グラウンディング**: 情報ソースとの紐づけ（<span class="red">**回答の根拠**</span>）

---

# RAGの前処理: ドキュメント保存時の前処理
- 必要な情報をうまく検索するためには、**保存の仕方も重要**になる

**チャンキング**:
- ドキュメントをチャンクに分割してDBに格納
- 切り方: ファイル単位、文書構造単位（章とか）、文字数、意味のまとまり
- 切られて**文脈が途切れる問題**への対策例:
    - チャンクを階層的にして親チャンクをLLMに渡す
    - チャンクに「全体から見たそのチャンクの要約や文脈」を含める
    - Agenticに足りない情報を取りに行く

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# エージェントについて知ろう
## 世の中のすごいプロダクトの中身を推測できるようになる
実はさっきのRAGはNotebookLMの中身の推測でした
（OSSでNotebookLMを目指しているレポジトリは先程のような構成）

<span class="small">

ここからの話は非エンジニアの方は「へーそんなのもあるんだ」くらいで聞いてください。
</span>

---

# ReAct（Reasoning + Acting） Agent
- エージェントの基礎
- [ReAct](https://arxiv.org/abs/2210.03629): Thought (思考)→Action (行動)→Observation (観察)

![](fig/react.svg)

ツール群: Web検索, コード実行, 画像生成, ファイル検索, コンテキスト取得
→ ツール群にコンテキスト取得が入ると**Agentic RAG**になる

---
# Reflexion（内省）
- [Reflexion](https://arxiv.org/abs/2303.11366): 結果の振り返りを行い次の試行に活かす

![](fig/reflexion.svg)

- 先程のReActと組み合わせることもできる
- プランを立てて結果に基づきプランを修正する[Adaptive Planning](https://arxiv.org/pdf/2305.16653)もある
    - <span class="small">CursorやClaude Codeもプラン立てて修正しながら動きますよね</span>

<!-- ---

# マルチエージェントの構成
-  -->

---


<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 実践演習（ハンズオン）〜後半〜
- 前半と同様、穴埋め問題になっている`./practice/`を編集して進めてみよう
- `uv run python practice/genai_ver/a1.py`のように実行できます
- 困ったらAIに聞いたり、答えの`./src/`を見ながら進めてOK

---

# APIで使えるその他のオプション
- Web版で普通にサポートしている機能をAPIでも使ってみよう
- D1のみ必須、その他はオプション

<div class="grid cols2">

<div>

#### 演習D1: マルチモーダル入力
- [画像を解釈](https://ai.google.dev/gemini-api/docs/image-understanding?hl=ja)させてみよう

#### 演習D2: グラウンディング（検索）
- 今日の東京の天気を調べさせよう

</div>

<div>

#### 演習D3: Pythonコード実行
- $y=x^2$のグラフを描かせてみよう

#### 演習D4: Tool Calling
- [自動関数呼び出し](https://ai.google.dev/gemini-api/docs/function-calling?hl=ja&example=meeting#automatic_function_calling_python_only)を体験しよう

</div>

</div>

---

# LLMを支える周辺技術
### 演習E1: 2つの文の意味的類似度を計算してみよう
- [Embedding API](https://ai.google.dev/gemini-api/docs/embeddings?hl=ja)を呼んでベクトル化してコサイン類似度を計算する

### 演習E2: Google DeepResearchを再現するために必要な設計を考えよう
- 設計問題でコード不要（非エンジニアはスキップしてもOK）

### 演習E3: LangChainの[ReAct Agent](/oss/python/langchain/agents)を使ってみよう（エンジニアのみ）
- カスタムで適当な関数を与えて挙動を見る

---

# 便利なツール
### 演習F1: n8nを使って構造化出力したLLMを組み合わせてみよう
- 入力の「名前と趣味を抽出」後、「趣味は英語に」、「名前の姓/名判定」をしよう
- GUIで簡単に構築できることを体験する

### 演習F2: LLMのトレースを経験してみよう (エンジニアのみ)
- ReAct Agentをトレースで観察してみよう（以下どちらか）

<div class="grid cols2 small">

<div>

[LangSmith](https://www.langchain.com/langsmith/observability): SaaS
- 登録後`.env`にAPIキー設定するだけ
- **データが送信されるので注意**
</div>

<div>

[LangFuse](https://github.com/langfuse/langfuse): ローカルホスト
- `docker compose up`して`localhost:3000`でkey発行し`.env`へ
- langchainのcallbacksに設定
</div>

</div>


---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 解説D
## （ネタバレしたくない方はここで戻ってください）
ソースコード:
- genai: [D1](./src/genai_ver/d1.py), [D2](./src/genai_ver/d2.py), [D3](./src/genai_ver/d3.py), [D4](./src/genai_ver/d4.py)
- LangChain: [D1](./src/langchain_ver/d1.py)

---
# 解説D1~D4: オプション機能

```python
def get_current_temperature(location: str) -> str:
    """今日の気温を調べる関数"""   # docstringがコンテキストとして渡る
    return "今日の気温は25度です"
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"), # D1: 画像入力
        "画像の内容を説明してください",
    ],
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(google_search=types.GoogleSearch()), # D2: Google検索
            types.Tool(code_execution=types.ToolCodeExecution), # D3: コード実行
            get_current_temperature, # D4: 自作関数も渡せれる
        ]
    ),
)
```
各々、1行加えるだけでできるので簡単！Web版Geminiで検証が不安ならAPIでも簡単

---

<!-- _paginate: skip -->
<!-- 中央寄せ -->
<!-- _class: vertical-center -->
# 解説E&F
## （ネタバレしたくない方はここで戻ってください）
ソースコード:
- genai: [E1](./src/genai_ver/e1.py)
- LangChain: [E1](./src/langchain_ver/e1.py), [E3](./src/langchain_ver/e3.py)

---
# 解説E1: コサイン類似度（genai）
```python
target_texts = ["漫画", "アニメ"]
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=target_texts,
    config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
)

embedding1 = np.array(result.embeddings[0].values)
embedding2 = np.array(result.embeddings[1].values)

normed_embedding1 = embedding1 / np.linalg.norm(embedding1)
normed_embedding2 = embedding2 / np.linalg.norm(embedding2)
print("cosine similarity: ", np.dot(normed_embedding1, normed_embedding2))
```
自然言語が数値ベクトルに変換されて、類似性を比較できることを実感できたらOK

---
# 解説E1: コサイン類似度（LangChain）
```python
target_texts = ["漫画", "アニメ"]
model = VertexAIEmbeddings(model="gemini-embedding-001")
results = model.embed(
    target_texts,
    embeddings_task_type="SEMANTIC_SIMILARITY",
)

embedding1 = np.array(results[0])
embedding2 = np.array(results[1])

normed_embedding1 = embedding1 / np.linalg.norm(embedding1)
normed_embedding2 = embedding2 / np.linalg.norm(embedding2)
print("cosine similarity: ", np.dot(normed_embedding1, normed_embedding2))
```


---

# 解説E2: Deep Research設計
たとえばこんな感じに設計できます:
![](./fig/deep-research.svg)

オープンソースでもいくつか出ています
- [gemini-fullstack-langgraph-quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart)
- [open_deep_research](https://github.com/langchain-ai/open_deep_research)

---

# 解説F1: n8nを使ってみよう
<div class="flex cols2">

<div>

![height:470](./fig/n8n.png)
</div>

<div>

LLMはどちらでもOK:
- Basic LLM Chain
- AI Agent

Structured Output Parserを
うまく使おう
</div>

</div>

---
# 解説E3&F2: ReAct Agentのトレース
```python
@tool
def func_add(a: int, b: int) -> int:     # 自作関数
    """足し算をする"""                     # Agentは、docstringを読んで判定してくれる
    print("called func_add")
    return a + b
@tool
def func_mul(a: int, b: int) -> int:
    """掛け算をする"""
    print("called func_mul")
    return a * b
agent = create_agent( # 関数を渡す
    model=ChatVertexAI(model="gemini-2.5-flash-lite"), tools = [func_add, func_mul]
)
result = agent.invoke(
    {"messages": [("human", "3と4を足した値に1+3を足した値同士を掛け算するとどうなる？")]}
)
```
たとえばこんな例だと中身はどうなるでしょうか？

---
# 解説E3&F2: ReAct Agentのトレース
<div class="flex cols2">

<div>

![height:450](fig/trace.png)
</div>
<div>

内部でループが回り、
3回LLMが呼ばれている
事がわかる

トレースのLangSmithは
**環境変数設定するだけ**
（LangChainの場合）
[`.env.sample`](.env.sample)参照
</div>

</div>

---
# 解説F2: トレースツールLangSmithについて
[LangSmith](https://smith.langchain.com/): LangChainが提供しているLLM OpsのSaaS
- LLM実行結果のトレース
    - 結果に手動アノテーションできる → **質の良いデータセットを作れる**
    - 自動評価（LLM as a Judge）も仕込める
- プロンプトバージョン管理
    - Web UIからもコードからも呼べる → **サーバーの更新を待たずに更新ができる**
- プロンプトチューニング画面
    - 変数の入力がUIからできる → **本番プロンプトをPdMがチューニングしやすい**
    - 実行結果に即時アノテーションできる → **自分の評価を残しておける**

→ データが整えば[ファインチューニング](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning?hl=ja) / [プロンプト最適化](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer?hl=ja)の可能性がある

---

# 締め
- 全員LLM設計できるようになった
- 全員PoCできるようになった
- 全員AIフィードバックループをイメージできるようになった

## 今日のコードはすべてレポジトリにあるので、各案件でコピペして行うとPoC/実装が速くなります！
## n8n/LangSmithなど使いたい需要あれば一緒にツール申請まわり進めましょう！
