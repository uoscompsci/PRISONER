# starts prisoner instance then demo server

python /usr/bin/prisoner-demo/demo_bootstrap.py

python /usr/bin/prisoner/server/prisoner.wsgi &
python /usr/bin/prisoner-demo/demo.py &

# map ports on VM to localhost if OS X
# if on another platform you're using boot2docker run these lines also

# echo "****** IMPORTANT ******"
# echo "If you are using Docker in OS X, or boot2docker on any platform, please run the following two lines at the command line:"
#
# echo 'VBoxManage controlvm dev natpf1 "prisoner,tcp,127.0.0.1,5000,,5000"'
# echo 'VBoxManage controlvm dev natpf1 "demo,tcp,127.0.0.1,9000,,9000"'
#
# echo "***********************"

echo "Ready! To start the experiment, visit http://localhost:9000/createDatabase"

tail -f /dev/null
