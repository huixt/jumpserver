BASE=$(dirname $0)
cd $BASE/..
. env/bin/activate
nohup python run_server.py 
