# Django Diary

## 概要

Djangoで作成した日記管理アプリです。

ログインしたユーザーが、自分の日記を作成・閲覧・編集・削除できます。

ポートフォリオとして、Djangoの基本的なCRUD処理だけでなく、ユーザー認証、ユーザーごとのデータアクセス制御、画像アップロード、自動テスト、コード品質管理などを実装しています。

## 主な機能

* ユーザー認証

  * ログイン
  * ログアウト
* 日記の作成
* 日記一覧の表示
* 日記詳細の表示
* 日記の編集
* 日記の削除
* 日記への画像アップロード
* 画像差し替え時の古い画像ファイル削除
* ユーザーごとの日記データのアクセス制御
* 自動テスト
* Ruffによるコード品質管理

## 使用技術

* Python 3.12
* Django 6.1
* SQLite
* Pillow
* python-dotenv
* Ruff
* HTML / CSS / JavaScript

## ディレクトリ構成

```text
diary_project/
├── accounts/
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── diary/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_page_picture.py
│   │   ├── 0003_page_user.py
│   │   ├── 0004_alter_page_user.py
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── static/
│   └── diary/
│       ├── css/
│       │   └── base.css
│       └── js/
│           └── base.js
├── templates/
│   ├── base/
│   │   └── diary_base.html
│   ├── diary/
│   │   ├── index.html
│   │   ├── page_confirm_delete.html
│   │   ├── page_detail.html
│   │   ├── page_form.html
│   │   ├── page_list.html
│   │   └── page_update.html
│   └── registration/
│       └── login.html
├── .env.example
├── .gitignore
├── manage.py
├── pyproject.toml
└── README.md
```

## セットアップ

### 1. リポジトリを取得

```bash
git clone https://github.com/chatora0330/diary_project
cd diary_project
```

### 2. 仮想環境を作成

Windows PowerShellの場合：

```powershell
python -m venv .venv
```

仮想環境を有効化します。

```powershell
.venv\Scripts\Activate.ps1
```

### 3. パッケージをインストール

```powershell
pip install django==6.1 pillow==12.3.0 python-dotenv==1.2.3 ruff==0.16.4
```

### 4. `.env`を作成

`.env.example`を参考に、プロジェクト直下に`.env`を作成します。

```text
DJANGO_SECRET_KEY=ここにSecret Keyを設定
```

`.env`はGit管理対象外です。

### 5. マイグレーション

```powershell
python manage.py migrate
```

### 6. 開発サーバーを起動

```powershell
python manage.py runserver
```

ブラウザから以下にアクセスします。

```text
http://127.0.0.1:8000/diary/
```

## テスト

Djangoのテスト機能を使用しています。

```powershell
python manage.py test
```

現在、ユーザーごとのアクセス制御や画像ファイルの差し替えなどをテストしています。

## コード品質管理

Ruffを使用してコードのチェックとフォーマットを行っています。

チェック：

```powershell
ruff check .
```

フォーマットチェック：

```powershell
ruff format --check .
```

設定は`pyproject.toml`で管理しています。

## 工夫した点

### 1. ユーザーごとのデータアクセス制御

`Page`モデルにDjangoの`User`モデルとのForeignKeyを設定し、日記とユーザーを関連付けています。

また、一覧・詳細・編集・削除の処理でログインユーザー本人の日記だけを取得するようにしています。

### 2. 日記作成時のユーザー設定

日記作成時にはフォームからユーザーを入力させず、ログイン中のユーザーをView側で設定しています。

これにより、フォームから別ユーザーの日記として登録されることを防いでいます。

### 3. 画像差し替え時の古いファイル削除

日記の画像を変更した場合、古い画像ファイルが`media`ディレクトリに残り続けないようにしています。

画像の差し替え時には古いファイルを削除し、日記自体を削除した場合にも関連する画像ファイルを削除するようにしています。

### 4. 自動テストによるアクセス制御の確認

ユーザーAの日記をユーザーBが閲覧・編集・削除できないことをテストしています。

また、画像差し替え時に古い画像ファイルが削除され、新しい画像ファイルが存在することもテストしています。

### 5. 環境変数によるSecret Keyの管理

Djangoの`SECRET_KEY`をコードに直接記述せず、`.env`から読み込むようにしています。

`.env`はGit管理対象外とし、`.env.example`だけをリポジトリに含めています。

### 6. Ruffによるコード品質管理

Ruffを使用して、コードの静的チェックとフォーマットを行っています。

現在、`ruff check .`と`ruff format --check .`の両方を通過する状態にしています。

## 今後追加したい機能

今後の学習やポートフォリオの発展に合わせて、以下の機能追加を検討しています。

* 日記一覧のページネーション
* 日記の検索・絞り込み
* 画像アップロード時のファイルサイズ・形式のバリデーション
* ユーザープロフィール機能
* GitHub Actionsによる自動テスト
* 本番環境へのデプロイ
* UI・レスポンシブデザインの改善
