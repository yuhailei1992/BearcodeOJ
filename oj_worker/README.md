oj_worker is to be deployed on docker, which will eventually form a worker cluster to run user's code. 

# Why separate oj_worker from bearcode
The primary reason to separate oj_worker from bearcode is for security: we don't trust user code, and we cannot allow the code to run in bearcode server, which maintains connection with our database. Instead, we are running user code in oj_worker, which runs on docker, and won't cause much trouble even if malicious code is submitted. There will be eventually a cluster of docker oj_workers, with a load balancer to run the code submitted by bearcode.

# How oj_worker works
oj_worker is a individual django project. It is intended to run on a different machine than bearcode. When launched, oj_worker will expose RESTful API to the bearcode server. Instead of running usercode locally, bearcode will fire an asynchronous http request to oj_worker, and get a JSON response. The JSON response contains the result: final decision(Accepted, Wrong Answer, etc.), debugging information, etc. 

