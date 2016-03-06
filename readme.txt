1. Deployについて：
	・kadai.zipを解答し、kadaiフォルダに移動
	・pythonバーチャル環境を作成（sqlite3, python 2.7.10, pip, virtualenv必要）
		# virtualenv venv
	・virtualenvをアクティベート
		# source venv/bin/activate 
	・必要なパケージをインストール
		# pip install -r requirements.txt
	・データベースを初期化
		# python init_db.py
	・アプリケーションを起動
		# python run.py 

2. 仕様について：
	・アプリケーションurl: localhost:5000
	・Signupにおいてメール認証を行わず、各項目を入力すればsignup可能
	・プロフィール画像は、画像上をクリックすれば画像を変更できる
	・Photosボタンをクリックし、画像閲覧・アップロード・削除できる

3. Deployにおいて問題が発生した場合：
	・AWSにdeployされています
	・url：http://ec2-52-25-104-208.us-west-2.compute.amazonaws.com
	・デフォルトユーザ：
		User ID：user1, user2
		Password：password1, password2
