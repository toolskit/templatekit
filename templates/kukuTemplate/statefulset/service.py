
from kubernetes import client


def template(context):
    name = context["name"]
    labels={"name": name}

    ports = context["ports"]
    for port in ports:
        port.update(name="tcp-{}-{}".format(port["port"],port["targetPort"]))

    type = "NodePort" if ports[0].get("nodePort") else "ClusterIP"


    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name = name,labels = labels),
        spec=client.V1ServiceSpec(
            type=type,
            ports=ports,
            selector={"name": name},
        ),
    )
