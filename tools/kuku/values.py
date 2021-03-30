# from typing import List, Mapping

import yaml

# from kuku.types import Context
# from kuku.utils.dict import unroll_key, merge_deep, IGNORED_LIST_ITEM


def merge_deep(src,dst):
    """ Merge (deep) 2 dicts. If there is a conflict the `src` key overwrites the `dst` key"""

    for key, value in src.items():
        if isinstance(value, dict):
            # get node or create one
            node = dst.setdefault(key, {})
            merge_deep(value, node)
        elif isinstance(value, list):
            if key not in dst:
                dst[key] = value
            else:
                out = []
                for i in range(max(len(dst[key]), len(value))):
                    if i >= len(dst[key]):
                        out.extend(value[i:])
                        break
                    if i < len(value) and value[i] != IGNORED_LIST_ITEM:
                        out.append(value[i])
                    else:
                        out.append(dst[key][i])
                dst[key] = out
        else:
            dst[key] = value

    return dst

def resolve(values,value_files):
    context = {}
    for value_file in value_files:
            with open(value_file) as fd:
                context = merge_deep(yaml.safe_load(fd), context)
              

    # arguments from the CLI have priority
    for key_values in values:
        if "," in key_values:
            extended_key_values = key_values.split(",")
        else:
            extended_key_values = [key_values]

        for key_value in extended_key_values:
            format_error = "Invalid key=value format for: {}".format(key_value)
            if "=" not in key_value:
                raise ValueError(format_error)

            key, value = key_value.split("=")
            if not key:
                raise ValueError(format_error)

            context = merge_deep(unroll_key(key, value), context)
    return context


