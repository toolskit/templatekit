import sys
import os
import struct
import re


from builder.istio_builder import Primary,Canary 
from builder.kuku_builder import Kuku

class AbstractTemplateFactory(object):
    def start_build(self,**env):
        self.env = env 
        temp = self.create_template()
        temp.initialize(**env)
        return temp.build()
    def create_template(self,class_type):
        pass

class IstioTemplateFactory(AbstractTemplateFactory):
    def create_template(self):
        if self.env.get("mode") == "primary":
            return Primary()
        else:
            return Canary()

class KukuTemplateFactory(AbstractTemplateFactory):
    def create_template(self):
        return Kuku()
