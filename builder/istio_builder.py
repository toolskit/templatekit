# -*- coding: UTF-8 -*-
from templatekit.tools import Templite
from templatekit.templates import istio_template as tp


class Base(object):
    def initialize(self,**env):

        self.domain_9102 = env.get("domain_9102")
        self.domain_9106 = env.get("domain_9106")
        self.gateway_name = env.get("gateway_name")
    def build(self):
        gw = Templite(tp.TemplateGateway).render(domain_9102=self.domain_9102,domain_9106=self.domain_9106,gateway_name=self.gateway_name)
        

class Primary(Base):
    def initialize(self,**env):
        super(Primary,self).initialize(**env)
        self.svc_list = env.get("svc_list")
        
        self.build_env = {
                                "domain_9106": self.domain_9106,
                                "domain_9102": self.domain_9102,
                                "gateway_name": self.gateway_name, 
                        }
    def build(self):
        super(Primary,self).build()
        for svc in self.svc_list: 
            self.build_env["svc"] = svc        
            if svc.startswith("frontend"):                
                print Templite(tp.TemplatePrimaryFrontend).render(**self.build_env)
            else:
                print Templite(tp.TemplatePrimaryBackend).render(**self.build_env)
                
                  
class Canary(Base):
    def initialize(self,**env):
        super(Canary,self).initialize(**env)
        self.svc_list = env.get("svc_list")
        self.header_type = env.get("header_type")
        self.header_value = env.get("header_value")
        self.build_env = {
                                "domain_9106": self.domain_9106,
                                "domain_9102": self.domain_9102,
                                "gateway_name": self.gateway_name, 
                                "header_type": self.header_type,
                                "header_value": self.header_value,
                        }
        

    def build(self):
        super(Canary,self).build()
        
        for svc in self.svc_list: 
            self.build_env["svc"] = svc        
            if svc.startswith("frontend"):                
                print Templite(tp.TemplateCanaryFrontend).render(**self.build_env)
            else:

                print Templite(tp.TemplateCanaryBackend).render(**self.build_env)


