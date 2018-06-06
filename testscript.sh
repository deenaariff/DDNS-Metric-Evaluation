xterm -e java -jar Weave.jar 1 1 nodes.xml
xterm -e java -jar Weave.jar 2 1 nodes.xml
xterm -e java -jar Weave.jar 3 1 nodes.xml

cd LoadBalancer
xterm -e python loadbalancer.py

cd ..
cd Client
xterm -e python client.py
