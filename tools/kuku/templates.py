import os,sys
import pkgutil
from copy import deepcopy



TEMPLATE_FUNCTION_NAME = "template"


def find(templates_dir):
    """Given a templates directory and import all python templates"""

    templates = {}

    for module_info, name, ispkg in pkgutil.walk_packages([templates_dir]):  
        module = module_info.find_module(name).load_module(name)
        template_path = os.path.join(templates_dir, name + ".py")
        # only consider python modules with a template function
        template_func = getattr(module, TEMPLATE_FUNCTION_NAME, None)
        if template_func:
            templates[template_path] = template_func

    if not templates:
        raise ValueError(
            "No kuku python templates files found in {}".format(templates_dir)
        )

    return templates

def render(context,templates):
    """Given a `context` of values and a list of `templates` render them to k8s objects"""

    rendering = {}
    for template_path, template_func in templates.items():
        # pass a copy of the context to the template function and get it's k8s objects
        k8s_objects = template_func(deepcopy(context))
        if not isinstance(k8s_objects, (list, tuple)):
            k8s_objects = [k8s_objects]
        rendering[template_path] = k8s_objects
    
    return rendering