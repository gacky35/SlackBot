# slackbot

Slackでのユーザグループの利用をサポートするbot <br>
This is a Slackbot which support using usergroup.

## Requirement

まず，以下のページからワークスペースに導入するアプリの基盤を作ってください． <br>
First, please make the base app from following URL which invite to your workspace. <br>
[Slack API](https://api.slack.com/)

次に，このリポジトリをクローンしてください． <br>
Second, please clone this repository. <br>
```
$ git clone git://github.com/gacky35/SlackBot.git
```

また，これを利用するためには以下の2つが必要になります． <br>
And, you need these library to use this bot. <br>
[slackbot](https://github.com/lins05/slackbot) <br>
[python-slackclient](https://github.com/slackapi/python-slackclient) <br>

最後に，アプリのトークンをファイルに保存します． <br>
Finally, regist app token on the files. <br>
```
$ echo {Bot User OAuth Access Token} >> app/access_token.txt
$ echo {OAuth Access Token} >> app/plugins/client_token.txt
```

以下のコマンドで実行できます． <br>
You can run this program with this command. <br>
```
$ bash run.sh
```
