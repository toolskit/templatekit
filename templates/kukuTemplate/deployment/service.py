
from kubernetes import client
import os

def template(context):
    name = context["name"]
    selector = {"app": name.strip("-v2")}
    labels= selector
    
    ports = context.get("ports")
    # istio dispatch protocol
    if name.startswith("frontend-dispatch"):
        for port in ports:
            port.update(name="http-{}-{}".format(port["port"],port["targetPort"]))
    elif name.startswith("backend-clientupdate"):
        for port in ports:
            port.update(name="http-{}-{}".format(port["port"],port["targetPort"]))
    elif name.startswith("backend-logproxy"):
        for port in ports:
            port.update(name="udp-{}-{}".format(port["port"],port["targetPort"]))
    else:
        for port in ports:
            port.update(name="tcp-{}-{}".format(port["port"],port["targetPort"]))
        
    type = "NodePort" if ports[0].get("nodePort") else "ClusterIP"
    

    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name = name, labels = labels),
        spec=client.V1ServiceSpec(
            type=type,
            ports=ports,
            selector=selector,
        ),
    )
