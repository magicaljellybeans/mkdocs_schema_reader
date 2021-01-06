import os
import jsonschema2md
import json
import logging

from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin


class SchemaReader(BasePlugin):
    def on_files(self, files, config):
        parser = jsonschema2md.Parser()
        excludedirs = set(["venv", "env", "__pycache__"])
        schema_list = []
        schema_dict = {"Schema": schema_list}

        # Look for json files
        for root, dirs, filenames in os.walk("../"):
            dirs[:] = [d for d in dirs if d not in excludedirs]

            for file in filenames:
                jsonpath = os.path.join(root, file)
                if file.endswith(".json"):

                    with open(jsonpath) as f:
                        # Check file is a schema file
                        data = f.read()
                        schema_syntax = ["$schema", "$ref"]

                        if any(x in data for x in schema_syntax):
                            # write converted markdown file to this location
                            path = f"site/schema/{file[:-5]}.md"
                            if not os.path.isdir("./site/schema"):
                                os.mkdirs("./site/schema", exist_ok=True)

                            try:
                                with open(path, "w") as md:
                                    lines = parser.parse_schema(json.loads(data))
                                    for line in lines:
                                        md.write(line)
                            except Exception:
                                logging.exception(f"Error handling {jsonpath}")
                                print("The file may not be valid Schema, consider excluding it.")
                                continue

                            # Add to Files object
                            mkdfile = File(
                                f"schema/{file[:-5]}.md",
                                f"{os.getcwd()}/site",
                                config["site_dir"],
                                config["use_directory_urls"],
                            )
                            files.append(mkdfile)

                            # Add to schema list
                            schema_list.append(
                                {f"{mkdfile.name}": f"{mkdfile.src_path}"}
                            )

        # Add schemas to nav
        config["nav"].append(schema_dict)

        return files
