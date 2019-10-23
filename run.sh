if [ ! -d data ]
then
    mkdir data
fi
if [ ! -f data/usergroup_list.txt ]
then
    touch data/usergroup_list.txt
fi
docker build -t secretary .
docker run -v ~/slackbot/data:/data -d secretary
