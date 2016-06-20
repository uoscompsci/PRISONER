# script to run docker image
# includes some OS X shims for port forwarding

# try the b2d default vm to map ports on os x
# TODO: detect these to make this cleaner
if [[ "$OSTYPE" == "darwin"* ]]; then
 echo "It looks like you're running OS X."
 echo "I'm going to try map some ports..."
 VBoxManage controlvm default natpf1 "prisoner,tcp,127.0.0.1,5000,,5000"
 VBoxManage controlvm default natpf1 "demo,tcp,127.0.0.1,9000,,9000"
fi

echo "PRISONER Demo: Getting image (this may take a while...)"
docker run -i -t -p 9000:9000 -p 5000:5000 --name prisoner-demo lhutton/prisoner-demo 
