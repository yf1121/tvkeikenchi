# TV Reaction

## 概要

リアルタイムツイートを取得します。

## ディレクトリ階層

```
-- tv_reaction
|- epgtools
|- twittertools
|- templates
|- app.py メイン
|- Procfile
|- requirements.txt
|- runtime.txt
|- Readme.md
|- .gitignore
```

# Tips

## 仮想環境の構築（初回のみ）

`python -m venv heroku_env`

## 仮想環境の起動

`heroku_env\Scripts\activate.bat`

### 仮想環境へのライブラリのインストール

`pip install -r requirements.txt`

## 依存関係の出力

`pip freeze > requirements.txt`

## デプロイ
`git add .`

`git commit -m"message"`

`heroku stack:set heroku-18 -a` 

`selectbook-bot`

`git push heroku master`

## Heroku環境変数の設定（初回を除き省略可）

`heroku config:set BOT_TOKEN="abc-1234-xyz" -a APP_NAME`

## Heroku環境変数の設定確認

`heroku config:get BOT_TOKEN -a APP_NAME`

## 仮想環境の終了

`heroku_env\Scripts\deactivate.bat`