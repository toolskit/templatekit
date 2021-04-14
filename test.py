import sys,os 
sys.path.append("..")
from templatekit import IstioTemplateFactory
from templatekit import KukuTemplateFactory

# env = {
#         "domain_9106": "bmgcn-alpha1206-9106.ddd.com",
#         "domain_9102": "bmgcn-alpha1206-9102.ddd.com",
#         "gateway_name": "bmgcn-gateway",
#         "header_type": "openid",
#         "header_value": "bmg_.*[0-1]$",
#         "svc_list": ["backend-game","backend-clientupdate"],
#         "mode": "primary",
#     }



env = {
    "context_file": ["/root/bmg_devops/k8s/kuku/kuku-bmg/yml/deployment/value_dispatch.yml","/tmp/common.yml"],
    "type": "deployment",
    "canary_deployment": False
}

def start(template_type):
   factorys = dict(istio=IstioTemplateFactory,kuku=KukuTemplateFactory)
   temp = factorys[template_type]()
   print temp.start_build(**env)
   
if __name__ == "__main__":
    start("kuku")

