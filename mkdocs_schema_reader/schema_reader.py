import os
import jsonschema2md
import json
import logging

from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class SchemaReader(BasePlugin):

    config_scheme = (
        ("include", config_options.Type(list, default=[])),
        ("auto_nav", config_options.Type(bool, default=True)),
        ("output", config_options.Type(str, default="schema")),
        ("nav", config_options.Type(str, default="Schema"))
        ("example_as_yaml", config_options.Type(bool, default=False))
        ("show_example", config_options.Type(str, default='all'))
    )

    def on_files(self, files, config):
        # Add json files within included files/directories to list
        locations = []

        for entry in self.config["include"]:
            if entry.endswith(".json"):
                locations.append(entry)

            elif os.path.isdir(entry):
                for root, dirs, filenames in os.walk(entry):
                    for file in filenames:
                        if file.endswith(".json"):
                            locations.append(os.path.join(root, file))

            else:
                logging.warning(f"Could not locate {entry}")

        parser = jsonschema2md.Parser()
        schema_list = []

        ## Path to Nav ##
        path=list(filter(None, self.config["nav"].split('/')))
        path.reverse()
        out_as_string = f"{{'{path.pop(0)}': schema_list}}"
        for item in path:
            out_as_string = f"{{'{item}':[{out_as_string}]}}"

        schema_dict = eval(f"{out_as_string}")

        for filepath in locations:
            file = os.path.basename(filepath)

            with open(filepath) as f:
                # Check file is a schema file
                data = f.read()
                schema_syntax = ["$schema", "$ref"]

                if any(x in data for x in schema_syntax):
                    path = f"{config['docs_dir']}/{self.config['output']}/{file[:-5]}.md"
                    # write converted markdown file to this location
                    if not os.path.isdir(f"{config['docs_dir']}/{self.config['output']}"):
                        os.makedirs(f"{config['docs_dir']}/{self.config['output']}", exist_ok=True)

                    try:
                        with open(path, "w") as md:
                            lines = parser.parse_schema(json.loads(data), example_as_yaml=self.config["example_as_yaml"], show_example=self.config["show_example"])
                            for line in lines:
                                md.write(line)

                    except Exception:
                        logging.exception(
                            f"Exception handling {filepath}\n The file may not be valid Schema, consider excluding it."
                        )
                        continue

                    # Add to Files object
                    mkdfile = File(
                        f"{self.config['output']}/{file[:-5]}.md",
                        config['docs_dir'],
                        config["site_dir"],
                        config["use_directory_urls"],
                    )
                    files.append(mkdfile)

                    # Add to schema list
                    schema_list.append({f"{mkdfile.name}": f"{mkdfile.src_path}"})

                else:
                    logging.warning(
                        f"{filepath} does not seem to be a valid Schema JSON file"
                    )

        # Add schemas to nav
        if self.config["auto_nav"]:
            config["nav"].append(schema_dict)

        return files