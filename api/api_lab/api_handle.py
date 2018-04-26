def post_json_key_to_list_handle(target, name=None):
    key_list = []
    for key in target.keys():
        if name:
            newname = "%s.%s" % (name, key)
        else:
            newname = key
        if isinstance(target[key], str):
            key_list.append(newname)
        if isinstance(target[key], dict):
            key_list.append(post_json_key_to_list_handle(target[newname]))
        elif isinstance(target[key], list):
            i = 0
            for item in target[key]:
                list_newname = "%s.[%s]" % (newname, i)
                if isinstance(item, str):
                    key_list.append(list_newname)
                i = i + 1
                if isinstance(item, dict):
                    key_list.append(post_json_key_to_list_handle(item, list_newname))
    return key_list


def post_json_level1_key_to_dict_handle(target):
    re_dict = {}
    for key in target.keys():
        if isinstance(target[key], str):
            value_type = "str"
        elif isinstance(target[key], int):
            value_type = "int"
        elif isinstance(target[key], list):
            value_type = "list"
        elif isinstance(target[key], dict):
            value_type = "dict"
        else:
            value_type = "unkown_type"
        re_dict[key] = value_type
    return re_dict