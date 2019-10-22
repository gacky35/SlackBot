FROM python:3.6

LABEL maintainer="tgacky, s17t258@stu.kgawa-u.ac.jp"

#ファイルをappディレクトリに追加
COPY ./app /app/

#ルートディレクトリ設定
WORKDIR /app

RUN pip install -r requirements.txt

#コマンド実行
CMD ["python", "run.py"]
