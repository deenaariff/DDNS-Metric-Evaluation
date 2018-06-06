xterm -e java -jar Weave.jar 1 1 nodes.xml
xterm -e java -jar Weave.jar 2 1 nodes.xml
xterm -e java -jar Weave.jar 3 1 nodes.xml

cd LoadBalancer
start cmd /k python loadbalancer.py

cd ..
cd Client
start cmd /k python client.py
