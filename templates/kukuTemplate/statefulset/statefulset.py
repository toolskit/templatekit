from kubernetes import client
import yaml


def handle_env(file):
    with open(file,'r') as f:
        env_data = yaml.safe_load(f)
    f.close()
    return [client.V1EnvVar(name=key,value=value) for key,value in env_data.items()]


def template(context):
    """
    handle yml env
    """
    name = context.get("name")
    labels = {"name": name}
    image_tag=context["name"].split('-')[1]
    image = context["image_namespace"]+image_tag+":"+context["image_branch"]    
    args = [arg for arg in context["args"]] if context.get("args") else None
    limits,requests = context["resources"]["limits"],context["resources"]["requests"]
    replicas = context["replicas"][name]

    """
    handle cmdb env
    """
    filename = "env_" + name.split("-")[1] + ".yml"
    env = handle_env("/tmp/{}".format(filename))
    workingDir = context["workingDir"]

    """
    k8s yaml 组件模块
    """

    containers = [
                client.V1Container(
                    name = name, 
                    image = image,
                    env = env,
                    args = args,
                    image_pull_policy = "Always",
                    # readiness_probe=client.V1Probe(_exec=client.V1ExecAction(command=['cat','/tmp/container_ready']),initial_delay_seconds=10, period_seconds=5),
                    resources = client.V1ResourceRequirements(limits = limits,requests = requests),
                    security_context = client.V1SecurityContext(privileged=True),
                    working_dir = working_dir,
                )
    ]
    
    template = client.V1PodTemplateSpec(
                    metadata = client.V1ObjectMeta(labels=labels), 
                    spec = client.V1PodSpec(
                                containers = containers,
                                dns_policy = "ClusterFirst",
                                image_pull_secrets = [client.V1LocalObjectReference(name="image-pull-secret")],
                                restart_policy = "Always"
                            )
                    
               )
    
    spec = client.V1StatefulSetSpec(
                service_name = name,
                replicas = replicas,
                selector = client.V1LabelSelector(match_labels=labels),
                template = template
           )

    return client.V1StatefulSet(
        api_version = "apps/v1",
        kind = "StatefulSet",
        metadata = client.V1ObjectMeta(name = name,labels = labels),
        spec = spec 
    )
