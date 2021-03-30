
import sys,os
# sys.path.append("..")

from templatekit.tools.kuku.dump import dump
from templatekit.tools.kuku.templates import find,render
from templatekit.tools.kuku.values import resolve


class Kuku(object):
    def initialize(self,**env):
        self.__dict__ = env
    def build(self):
        try:
            current_path = os.getcwd()
            if self.type == "deployment":
                templates = find("{}/templatekit/templates/kukuTemplate/deployment".format(current_path))
            else:
                templates = find("{}/templatekit/templates/kukuTemplate/statefulset".format(current_path))
        except ValueError as e:
            print(e)   
            raise
        try:
            # Resolve values
            context = resolve([],self.context_file)
            
            if self.canary_deployment: 
                context["name"] = context["name"] + "-v2"
                context["version"] = "v2"
        except ValueError as e:
            print(e)
            raise

        rendering = render(context, templates)
        output = dump(rendering)
        return output


# k=Kuku()
# k.initialize(context_file=["/root/kuku-bmg/common_module/yml/deployment/value_game.yml","/tmp/common.yml"])
# k.build()