# b1.py の学び：構造化出力（Structured Output）

## 概要
Gemini API で構造化出力を使用して、LLM の応答を JSON 形式に制限し、確実にパース可能にする方法を学ぶ。

---

## 1. 構造化出力とは？

### 定義
**構造化出力** = LLM の応答形式とフィールドを制限して、常に同じ JSON スキーマで返させるテクニック

### 構造化出力がない場合
```python
response_schema=None
```
- LLM が勝手に判断して応答
- 毎回異なる形式で返る可能性
- 例：`{'negative_keywords': ['...'], 'analysis': '...'}`
- ❌ アプリケーションでの処理が難しい

### 構造化出力がある場合
```python
response_mime_type="application/json"
response_schema=CommentAnalysis
```
- 常に指定されたスキーマに従う
- 形式が固定される
- 例：`{'sentiment': 'positive'}`
- ✅ 確実にパース可能

---

## 2. 構造化出力の 3 つの要素

### ① response_mime_type
```python
response_mime_type="application/json"
```
- **役割**：出力形式を JSON に指定
- **効果**：LLM が JSON 形式で応答するように強制

### ② response_schema
```python
response_schema=CommentAnalysis
```
- **役割**：応答が従うべき JSON スキーマを定義
- **効果**：Pydantic モデルに定義されたフィールドのみが返される

### ③ 各フィールドの description
```python
sentiment: Literal["positive", "negative", "neutral"] = Field(
    description="コメントの感情: positive=肯定的, negative=批判的, neutral=中立的"
)
```
- **役割**：各フィールドに「何を入れるべきか」の判定基準を説明
- **効果**：LLM の判定精度を向上させる

---

## 3. contents vs description

### contents（プロンプト）
```python
contents=f"""以下のコメントの感情をpositive/negative/neutralで判定してください: {input_text}"""
```
- **対象**：ユーザー → LLM
- **役割**：「**何をするか**」のタスク指示
- **内容**：分析対象のテキストと、実際にやってほしいこと

### description（判定基準）
```python
description="コメントの感情: positive=肯定的, negative=批判的, neutral=中立的"
```
- **対象**：スキーマ → LLM
- **役割**：「**どう判定するか**」の評価軸説明
- **内容**：各フィールドに何を入れるべきかのガイドライン

### 両者の関係
```
contents で「タスク」を説明
    ↓
LLM が description の「基準」に従って判定
    ↓
固定された JSON スキーマで応答
```

---

## 4. LLM と従来の機械学習の違い

### 従来の機械学習
```
学習フェーズ：大量データ → 規則を自動抽出 → モデル化
推測フェーズ：入力 → モデル → テキスト（形式不定）
```
- データから自動で規則を学習
- 出力形式の制御がない

### LLM（大規模言語モデル）
```
学習フェーズ：事前学習済み（すでに高度な知識を持つ）
推測フェーズ：プロンプト + スキーマ → 形式を制御した JSON で応答
```
- すでに学習済みモデルを活用
- 構造化出力で形式を制御可能
- プロンプトで指示内容を柔軟に変更可能

---

## 5. 実装のポイント

```python
# 1. Pydantic モデルでスキーマを定義
class CommentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="判定基準の詳細説明"  # ← 詳しく書くと精度UP
    )

# 2. API を呼び出し時に構造化出力を有効化
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=f"""実際のタスク指示: {input_text}""",  # ← 具体的なテキストを含める
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=CommentAnalysis,  # ← スキーマを指定
        temperature=0.1,
    ),
)

# 3. パース
result = CommentAnalysis.model_validate_json(response.text)
```

---

## 6. キーポイント

| 項目 | 構造化出力なし | 構造化出力あり |
|---|---|---|
| **出力形式** | LLM が勝手に決める | スキーマで固定 |
| **信頼性** | 低い | 高い |
| **パース** | エラーが起きやすい | 確実に成功 |
| **実用性** | アプリで処理困難 | プログラムで処理容易 |

---

## まとめ

**構造化出力** = LLM の「気まぐれさを制御」するテクニック
- ✅ 形式を固定化
- ✅ 判定基準を明示
- ✅ アプリケーション統合を容易に

これにより、LLM を実務的なアプリケーションで安定して使用できる。

---

# b1/b2/b3.py の学びと構造化出力の整理

## b1.py で学んだこと
- `response_mime_type="application/json"` と `response_schema` を使うと、出力形式を固定できる
- `contents` は「やってほしいタスク」、`description` は「判断基準」を与える役割
- `model_validate_json()` で JSON 文字列をパースし、型検証を通した結果が得られる

## b2.py で学んだこと
- **1つのフィールドに全部詰めない**。商品名・ポジティブ・ネガティブ・スコアは別フィールドにする
- `Literal` は固定値の列挙なので、型が混ざるとエラーになる
  - 例: `Literal["A", 5]` のように文字列と数値を混ぜるのはNG
- スコアなど数値は `int` フィールドとして分けて定義するのが正しい

## b3.py で学んだこと
- 1コメント内に複数カテゴリが出る場合は **リスト構造**にするのが自然
- `List[CategoryFeedback]` のように、カテゴリごとのフィードバックを配列で持たせる
- `Literal` でカテゴリの取りうる値を固定すると、後続処理が安定する

## 構造化出力の旨み（メリット）
- **後続処理が圧倒的に楽**（集計、抽出、DB保存が直結）
- **型検証で異常を検知**できる
- 仕様が固定されるため、運用が安定する

## 構造化出力のデメリット（注意点）
- スキーマ設計と変更管理が必要
- 変更時にプロンプト・モデル・後続処理を揃える手間がある
- 例外的な情報を捨てやすく、柔軟性が落ちる
