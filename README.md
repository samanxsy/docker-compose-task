# Hey, This is Saman speaking!

## Appreciation
First of all, I want to thank you for the opportunity, and for providing me with this task! It means a lot, and I really, really appreciate it and As with the interview I both enjoyed and learned a lot doing it.❤️

### The Task
“Csinálj egy docker container-t amiben van egy futó Httpd szerver ami /index.html re visszaadja a docker container ID-ját.
Csinálj egy másik docker container-t amiben van egy load balancer
Csinálj egy docker compose file-t ami elindít egy load balancer-t és két web szervert
A web szerverek csak a LB keresztül érhetőek el
A docker image lehetőleg ne fussanak root user el
CentOS linux ajánlott“

### prerequisites
- Docker desktop
- kubectl
- AWS CLI

### My challenges
- Finding the right centOS image for the purpose of my task
- using the right package manager for installations | ```yum```
- Specifying a non-root user with necessary permissions, and run the images with the non-root user
- Correct configurations for the HAproxy.cfg file
- EKS Deployment (Extra)

### My Process
1. I started with reading about the centOS, and learning about its specifications and differents with other Linux distros I was familiar with.
2.  Searched about the best Loadbalancer I could use for the purpose, and after deciding to go with HAproxy, I learned about the required configurations, and how to apply them. >> [haproxy.cfg](https://github.com/samanxsy/docker-compose-task/blob/master/haproxy.cfg)
3. Wrote the Dockerfiles for the webserver and the load balancer. >> [Dockerfile-web](https://github.com/samanxsy/docker-compose-task/blob/master/Dockerfile-web) | [Dockerfile-LB](https://github.com/samanxsy/docker-compose-task/blob/master/Dockerfile-lb)
4.  Wrote the Docker-compose file, and after some back and forth debugging, I could access the containers via the Loadbalancer, and the container ID was displayed. >> ![Docker-Task](https://user-images.githubusercontent.com/118216325/235300204-a29be5db-1017-47f6-87e2-074cce6c24ac.png)

* Extra steps:
5. Created a Kubernetes cluster in AWS
6. Pushed the webserver Image to the AWS ECR >> [Public ECR](public.ecr.aws/i8f8t1r2/saman-docker-task)
7. Created a Deployment file, declaring for two instances of the webserver and a LoadBalancer >> [deployment,yaml](https://github.com/samanxsy/docker-compose-task/blob/master/deployment.yaml)
8. Applying the deployment to my AWS EKS cluster >> (I SHUT THEM DOWN DURING THE WEEKEND)

### AWS EKS
After finishing the task, I decided to take one more step, and write a yaml file, and deploy the same functionality required by the Task, but utilizing AWS EKS, and Accessible through internet.

- Here is the LoadBalancer service description ( Note That Due to the Costs I had to shut EKS resources down eventually )
```
Name:                     webserver-loadbalancer
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=webserver
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.100.151.60
IPs:                      10.100.151.60
LoadBalancer Ingress:     aa6a5f2d138ca4e8bba9bce9854aa724-404076512.eu-central-1.elb.amazonaws.com
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31795/TCP
Endpoints:                172.31.13.237:80,172.31.21.123:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

### The Errors I faced & How I fixed them
1. The package manager and the mirror list:
```
=> ERROR [ptc-docker-task-web2 2/6] RUN dnf -y update && dnf -y install httpd                                                                                                                       1.3s
 => ERROR [ptc-docker-task-loadbalancer 2/5] RUN dnf -y update && dnf -y install haproxy                                                                                                             1.3s
------
 > [ptc-docker-task-web2 2/6] RUN dnf -y update && dnf -y install httpd:
#0 0.948 CentOS Linux 8 - AppStream                      140  B/s |  38  B     00:00    
#0 0.952 Error: Failed to download metadata for repo 'appstream': Cannot prepare internal mirrorlist: No URLs in mirrorlist
```
- Solution:
    - Changed the base image to centOS:7
    - used ```yum``` instead of ```dnf```

2. Configuration file errors:
```
ALERT]    (1) : config : parsing [/usr/local/etc/haproxy/haproxy.cfg:17]: Missing LF on last line, file might have been truncated at position 34.
[ALERT]    (1) : config : Error(s) found in configuration file : /usr/local/etc/haproxy/haproxy.cfg
[ALERT]    (1) : config : Fatal errors found in configuration.
```
- Solution
    - Added a blank line at the end of the haproxy.cfg file (Seriously)

3. Invalid address:
```
ptc-docker-task-loadbalancer-1  | [ALERT] 114/210628 (1) : parsing [/etc/haproxy/haproxy.cfg:16] : 'server web1' : invalid address: 'httpd' in 'httpd:80'
ptc-docker-task-loadbalancer-1  | 
ptc-docker-task-loadbalancer-1  | [ALERT] 114/210628 (1) : parsing [/etc/haproxy/haproxy.cfg:17] : 'server web2' : invalid address: 'httpd' in 'httpd:80'
```
- Solution:
    - A typo in HAproxy config file's backend servers section. (Modified the server names to the correct names)

4. Permission Denied
```
(13)Permission denied: AH00072: make_sock: could not bind to address [::]:80
(13)Permission denied: AH00072: make_sock: could not bind to address 0.0.0.0:80
no listening sockets available, shutting down
AH00015: Unable to open logs
```
- Solution
    - Granted the httpd binary the capability to bind privileged ports (Ports below 1024, in our case 80)
    ```
    setcap 'cap_net_bind_service=+ep' /usr/sbin/httpd
    ```

### Useful Commands that helped me along the way
1. Finding the containers IP address:
```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id> 
```

2. Kubernetes services description:
```
kubectl describe services <service-name>
```
3. Getting Logs for the pods:
```
kubectl logs <pod-name>
```
---

### Quick test of the docker-compose task:
```
git clone https://github.com/samanxsy/docker-compose-task.git
cd docker-compose-task
docker-compose build && docker-compose up
```
---
### Thats it!
Once again, thanks for the opportunity, and thanks for your time! I'm Looking forward to talk about the task process and other stuff!
##### Cheers, 
##### Saman
