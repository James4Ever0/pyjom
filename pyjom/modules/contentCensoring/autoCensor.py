from tkinter import *
from pyjom.commons import *
from pyjom.medialang.core import *


def dummyAutoCensor(contentPath, meta, semiauto=False):
    mdata = {
        "dummyAutoCensor": {
            "input": {"path": contentPath, "meta": meta},
            "result": "some content here!",
        }
    }
    return mdata


def autoCensor(contentPath, meta, template_names=[], semiauto=False, args={}):
    mdata = {}
    template_dirs = ["medialang", "autoCensor"]
    medialang_template_paths = template_names  # not always need all templates.
    semiauto_key_blacklist = []
    semiauto_template_path_blacklist = []
    if semiauto:
        medialang_template_paths = [
            x
            for x in medialang_template_paths
            if x not in semiauto_template_path_blacklist
        ]
    for template_name in medialang_template_paths:
        name = template_name.split(".")[0]  # check if starts with meta.
        template_path = getTemplatePath(template_dirs, template_name)
        template_args = {} if name not in args.keys() else args[name]
        assert type(template_args) == dict
        if name.startswith("meta_"):
            template_args.update({"meta": meta})  # you can access it by keys.
        template_args.update({"mediafile": contentPath})
        # print("template_args")
        # breakpoint()
        medialang = Medialang(
            script_path=template_path,
            template=True,
            template_args=template_args,  # config inside the template args. None to use the default.
        )
        script = medialang.prettify()
        print(script)
        # breakpoint()
        data = medialang.execute()
        data = data[0][0]  # language feature.
        # what the fuck is wrong?

        mdata.update({name: data})  # this is not so good, though.
    if semiauto:  # need some modification.
        for key in semiauto_key_blacklist:
            mdata.pop(key)
    return mdata
