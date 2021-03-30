#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from kubernetes import client
import yaml
import os

def handle_env(file):
      with open(file,'r') as f:
         env_data = yaml.safe_load(f)
      f.close()
      return [client.V1EnvVar(name=key,value=value) for key,value in env_data.items()]

def handle_configmap(*args):
    try:
      parentDir = args[0]
      os.system("rm -r /tmp/{}".format(parentDir))
    except Exception as e:
      print ("{} dir is not exist".format(parentDir))
    for arg in args:
        if arg != args[0]:          
            os.makedirs("/tmp/{}/{}".format(parentDir,arg))
        else:
            os.makedirs("/tmp/{}".format(parentDir))
    
    for root, dirs, files in os.walk("/tmp/{}".format(parentDir)):
         subDir = [dir for dir in dirs if not dir[0] == "."]
         #mainfiles=[file for file in files if not file[0] == '.']
         break
    return parentDir,subDir
        

def template(context):
    """
    handle yml env
    """
    name = context.get("name")
    version = context.get("version")
    labels = {"app": name,"version":"v1"} if not version else {"app": name.strip("-v2"),"version":version}
    image_tag=context["name"].split('-')[1]
    image = context["image_namespace"]+image_tag+":"+context["image_branch"]    
    args = [arg for arg in context["args"]] if context.get("args") else None
    limits,requests = context["resources"]["limits"],context["resources"]["requests"]
    replicas = context.get("replicas",1)
    workingDir = context["workingDir"]
    if name == "backend-logproxy":
         annotations = {"sidecar.istio.io/inject": "false"}
    else:
        annotations = {"traffic.sidecar.istio.io/excludeOutboundPorts": "6379"}
    
    """
    handle cmdb env
    """
    filename = "env_" + name.split("-")[1] + ".yml"
    env = handle_env("/tmp/{}".format(filename))
    

    """
    k8s yaml 组件模块
    """
    
    #从svn分支configmap目录中获取相关的目录结构
    parentDir,subdir = handle_configmap("configmap")
    volumemounts=[
                    client.V1VolumeMount(mount_path="/{}".format(parentDir),name="mainfiles")
            ]
    volumes=[
             client.V1Volume(name="mainfiles",config_map=client.V1ConfigMapVolumeSource(name="mainfiles"))
            ]

    for dir in subdir:
        volumemounts.append(client.V1VolumeMount(mount_path="/{}/{}".format(parentDir,dir),name=dir))
        volumes.append(client.V1Volume(name=dir,config_map=client.V1ConfigMapVolumeSource(name=dir)))
 
    if name.startswith("frontend-dispatch"):
           containers = [
                client.V1Container(
                    name = name, 
                    image = image,
                    env = env,
                    args = args,
                    volume_mounts=volumemounts,
                    image_pull_policy = "Always",
                    lifecycle = client.V1Lifecycle(pre_stop=client.V1Handler(_exec=client.V1ExecAction(command=["nginx","-s","quit"]))),
                    readiness_probe=client.V1Probe(_exec=client.V1ExecAction(command=['cat','/tmp/container_ready']),initial_delay_seconds=10, period_seconds=5),
                    resources = client.V1ResourceRequirements(limits = limits,requests = requests),
                    security_context = client.V1SecurityContext(privileged=True),
                    working_dir = workingDir,
                )
    ]
    else:
        containers = [
                    client.V1Container(
                        name = name, 
                        image = image,
                        env = env,
                        args = args,
                        volume_mounts=volumemounts,
                        image_pull_policy = "Always",
                        readiness_probe=client.V1Probe(_exec=client.V1ExecAction(command=['cat','/tmp/container_ready']),initial_delay_seconds=10, period_seconds=5),
                        resources = client.V1ResourceRequirements(limits = limits,requests = requests),
                        security_context = client.V1SecurityContext(privileged=True),
                        working_dir = workingDir,
                    )
        ]


    template = client.V1PodTemplateSpec(
                    metadata = client.V1ObjectMeta(labels=labels,annotations=annotations),
                    spec = client.V1PodSpec(
                                containers = containers,
                                dns_policy = "ClusterFirst",
                                image_pull_secrets = [client.V1LocalObjectReference(name="image-pull-secret")],
                                restart_policy = "Always",
                                volumes=volumes
                            )

               )

             
    
    spec = client.V1DeploymentSpec(
                replicas = replicas,
                selector = client.V1LabelSelector(match_labels=labels),
                template = template,
                strategy=client.ExtensionsV1beta1DeploymentStrategy(
                            rolling_update=client.ExtensionsV1beta1RollingUpdateDeployment(max_surge=1,max_unavailable='25%'),
                            type="RollingUpdate",
                        ),
           )

    return client.V1Deployment(
        api_version = "apps/v1",
        kind = "Deployment",
        metadata = client.V1ObjectMeta(name=name,labels=labels),
        spec = spec 
    )

