import json
import os
from pprint import pprint
from typing import Dict

from baiduspider._spider import BaseSpider


class Generator(BaseSpider):
    def __init__(self, basemodule: str) -> None:
        super().__init__()
        self.spider_name = "generator"
        self.BASE_TYPES = [str, int, bool]
        self.base_module = basemodule
        self.base_template = '''"""移动端xx搜索结果模型类型注释文件

此模块中定义了所有现有移动端xx搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime, time
from typing import List, Union


'''

    def _reformat_type(self, x: str) -> str:
        return str(x).replace("<class '", "").replace("'>", "")

    def generate(
        self,
        filepath: str,
        jsonpath: str,
        basename: str,
        json_plain: Dict = None,
        write_template: bool = True,
    ):
        if json_plain:
            data = json_plain
        else:
            with open(jsonpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        if write_template:
            data = data["results"]
        out = ""
        if write_template:
            pre_out = self.base_template
        else:
            pre_out = ""
        try:
            new_basename = basename + (data["type"].capitalize())
        except Exception:
            new_basename = basename
        # if type(data) != list:
        #     print(new_basename, data["type"])
        #     pprint(data)
        out += f"""class {new_basename}(object):
    \"\"\"xxx搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.{self.base_module}.{new_basename}`类。
    \"\"\"

    def __init__(self) -> None:
"""
        if type(data) != list:
            data = [data]
        for _ in data:
            for i in _:
                if i == "type":
                    continue
                out += f"        self.{i}: "
                # print(_)
                # try:
                #     print(_[i])
                # except Exception:
                #     print(data)
                if type(_[i]) in self.BASE_TYPES:
                    out += self._reformat_type(type(_[i]))
                else:
                    if type(_[i]) == list:
                        try:
                            _[i] = _[i][0]
                        except Exception:
                            _[i] = None
                        if type(_[i]) in self.BASE_TYPES:
                            out += f"List[{self._reformat_type((type(_[i])))}]\n"
                            continue
                    elif not _[i]:
                        out += "None\n"
                        continue
                    # print(data[i])
                    if not _[i]:
                        out += "None\n"
                        continue
                    _[i]["type"] = _["type"]
                    print(new_basename, _["type"], i)
                    if new_basename.endswith(_["type"].capitalize()):
                        _[i]["type"] = i
                    pre_out += self.generate(filepath, None, new_basename, _[i], False)
                    out += new_basename + _[i]["type"].capitalize()
                out += "\n"
        out = pre_out + out + "\n\n"
        # print(out)
        if not write_template:
            return out
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(out)
        return out

    def generate_build_instance(self, filepath: str, class_name: str):
        file_data = open(filepath, "r", encoding="utf-8").read().split("\n")
        data = []
        for d in file_data:
            name = d.split("self.")[-1].split(":")[0]
            type_ = d.split(": ")[-1]
            if name == "plain":
                continue
            data.append({"name": name, "type": type_})
        out = f"    @staticmethod\n    def _build_instance(plain: Dict) -> {class_name}:\n        __returns = {class_name}()\n"
        out += "        __returns.plain = plain\n"
        for d in data:
            out += "        "
            if "List" not in d["type"]:
                out += f"__returns.{d['name']} = "
            if d["type"] in ["str", "int", "bool"]:
                out += f"get_attr(plain, \"{d['name']}\")"
            elif "List" in d["type"]:
                out += f"for i in get_attr(plain, \"{d['name']}\"):\n            "
                out += f"__returns.{d['name']}.append"
                if not d["type"].split("[")[-1].split("]")[0] in ["str", "int", "bool"]:
                    out += f"({class_name}{d['name'].capitalize()}._build_instance(i))"
                else:
                    out += "(i)"
            elif d["type"] == "time":
                out += f"time(get_attr(plain, \"{d['name']}\").split(\":\")[0], get_attr(plain, \"{d['name']}\").split(\":\")[1])"
            elif d["type"] == "datetime":
                out += f"convert_time(get_attr(plain, \"{d['name']}\"))"
            else:
                out += f""
            out += "\n"
        return out

    def generate_api_docs(self, path: str, outputpath: str) -> None:
        files = os.listdir(path)
        for f in files:
            if "." not in f:
                continue
            try:
                with open(
                    outputpath + f.split(".")[0] + ".md", "w", encoding="utf-8"
                ) as file:
                    name = (
                        path.strip(".").replace("/", ".").lstrip(".") + f.split(".")[0]
                    )
                    file.write(
                        f"::: {name}\n    rendering:\n      show_root_heading: true\n      show_source: true"
                    )
            except FileNotFoundError:
                os.mkdir(outputpath)
                with open(
                    outputpath + f.split(".")[0] + ".md", "w", encoding="utf-8"
                ) as file:
                    name = (
                        path.strip(".").replace("/", ".").lstrip(".") + f.split(".")[0]
                    )
                    file.write(
                        f"::: {name}\n    rendering:\n      show_root_heading: true\n      show_source: true"
                    )
            t = f.split(".")[0]
            t2 = outputpath.split("/", 2)[-1]
            print(f"        - {f}: {t2}{t}.md")


if __name__ == "__main__":
    generator = Generator("web")
    generator.generate_api_docs(
        "./baiduspider/mobile/models/typings/",
        "./docs/api/baiduspider/mobile/models/typings/",
    )
