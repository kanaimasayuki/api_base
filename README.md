# api_base

シンプルなapiです

## 編集が必要な箇所
ai_script内のファイルとapi.py、message.iniはプロジェクトごとに編集が必要。このリポジトリではサンプル用になっていて一応そのままでも使える。
### ai_script
この中にAIエンジンに相当するスクリプト(.pyファイル)を配置する。呼び出される側は関数になっている必要がある。
### api.py
apiサーバのメインモジュール。エンドポイントや呼び出す関数、ステータスコードなどを編集する。
### message.ini
error_codeに応じたメッセージを登録したファイル。ApiExceptionが発生した場合、呼び出し側にerror_codeに応じたメッセージが出力される。

## デプロイ方法
```
docker build -t api_base:{xxx} .
docker run -itd -p 8080:8080 -v $PWD/:/data/project api_base:{xxx}
```
{xxx}は適宜変更してください。

これでapiサーバが起動します。
```テストコマンド
curl http://0.0.0.0:8080/
curl http://0.0.0.0:8080/api/test
curl -X POST localhost:8080/api/ai_script -H 'Content-type: application/json' -d '{"test_key":"test_value"}'
```

