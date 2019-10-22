docker build -t secretary .
docker run -v ~/slackbot/data:/data -d secretary
