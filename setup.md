# 環境設定
今日ここが一番むずかしいですw  
Pythonを使いますが、ここを乗り越えれば後は穴埋め問題形式です。

## Vertex AI Gemini
GCPのVertex AI Geminiを使います。

普段はキーの管理の複雑性から、自分自身の認証情報でAPIを呼ぶ方法を案内している:
```sh
gcloud auth login
gcloud auth application-default login
```
のですが、今回は**運営の都合上APIキーをSlackで配布**します。（勉強会終了後、使えなくなります。）


## Python環境構築
コマンドの実行には「ターミナル」を使います。
![](fig/terminal.png)

ターミナル上で次を実行してください。
```sh
cd ~/Downloads/llm-study/
cp .env.sample .env
```

[uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)のインストール:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.11
uv sync
```

環境変数の設定:
`.env`というファイルを次のように修正してください:
```sh
GOOGLE_APPLICATION_CREDENTIALS="ここにSlackからダウンロードしたAPIキーのjsonのパスを記入してください"
```

LLMを叩く:
```sh
uv run python src/check.py
```

![](fig/setup-complete.png)
このようにLLMに関する説明が出るところまでいけば完了！

どうしても環境構築できない方はクラウド上のNotebook環境を案内しますので、Slackで伝えてください。


## n8nアカウントのセットアップ（一番最後の演習で使うGUIのツールです）
1. n8n招待リストの**自分の招待リンク**から登録を進める
2. 名/姓/パスワードを埋めて進める（パスワードは適当に決めて覚えておいてください）
    ![](fig/n8n-register.png)
3. アンケートはそのままスキップして「Get started」でOK
    ![](fig/n8n-skip.png)
4. この画面までこれば一旦OK。
    ![](fig/n8n-workflow.png)

時間余った人は以下を進めてください（演習の最後でやるので時間無かった人は後でOK）

5. 右上のオレンジのボタン「Create Workflow」を押す
6. 中央に出ている大きな「+」ボタンを押して右側の検索窓に「vertex」と入力し、「Google Vertex Chat Model」を選択
    ![](fig/n8n-vertex.png)
7. 現れた項目の「Credential to connect with」をクリックして「+Create new credential」を選択
    ![](fig/n8n-vertex-setting1.png)
8. 「Service Account Email」をVertex AI APIキーの`client_email`で埋めてください
    ![](fig/n8n-vertex-setting2.png)
9. 「Private Key」にはVertex AI APIキーの`private_key`で埋めてください
    （`-----BEGIN PRIVATE KEY-----`から`-----END PRIVATE KEY-----\n`まで全部含めます）
    ![](fig/n8n-vertex-setting3.png)
10. 右上の「Saved」を押すと元の画面に戻るので、以下のように「Project ID」と「Model Name」も埋めましょう
    - Project ID: 「From list」の状態になっていればAPIキーに書かれていた`project_id`をプルダウンから選べる
    - Model Name: gemini-2.5-flash
    ![](fig/n8n-vertex-setting4.png)
11. 左上の余白部分か「Back to canvas」を押してワークフローの画面に戻ります。  
    ![](fig/n8n-vertex-setting5.png)
12. 真ん中の下にあるオレンジの「Open chat」を押して開いたチャット画面に「こんにちは」と入力して反応が返ってこれば完了
    ![](fig/n8n-vertex-setting6.png)


## クラウドNotebook環境（環境構築失敗した方向けのバックアッププラン）
権限付与するので連絡ください。
1. 「JupyterLabを開く」を押す（共通のインスタンスを使います）
    ![](fig/notebook1.png)
2. 「+」を押すとLauncherが開く
    ![](fig/notebook2.png)
3. 「Terminal」を押して次のコマンドを**自分の名前に変えて**実行
    ```sh
    cp -r llm-study/ your-name/
    ```
    - `your-name`は**あなたの名前**など他の人と被らない名前をアルファベットで書いてください(例: yoshida)
4. 作成した自分のフォルダに入って動作確認
    ```sh
    cd your-name/
    uv run python src/check.py
    ```
    ![](fig/notebook3.png)
5. これ以降自分のフォルダの中で作業していただきます
    左側のGUIで直感的にファイルアクセスして開くことができます
    ![](fig/notebook4.png)
