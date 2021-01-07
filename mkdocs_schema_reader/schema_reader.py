import os
import jsonschema2md
import json
import logging

from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class SchemaReader(BasePlugin):

    config_scheme = (("include", config_options.Type(list, default=[])),)

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
        schema_dict = {"Schema": schema_list}

        for filepath in locations:
            file = os.path.basename(filepath)

            with open(filepath) as f:
                # Check file is a schema file
                data = f.read()
                schema_syntax = ["$schema", "$ref"]

                if any(x in data for x in schema_syntax):
                    # write converted markdown file to this location
                    path = f"site/schema/{file[:-5]}.md"
                    if not os.path.isdir("./site/schema"):
                        os.makedirs("./site/schema", exist_ok=True)

                    try:
                        with open(path, "w") as md:
                            lines = parser.parse_schema(json.loads(data))
                            for line in lines:
                                md.write(line)

                    except Exception:
                        logging.exception(
                            f"Exception handling {filepath}\n The file may not be valid Schema, consider excluding it."
                        )
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
                    schema_list.append({f"{mkdfile.name}": f"{mkdfile.src_path}"})

                else:
                    logging.warning(
                        f"{filepath} does not seem to be a valid Schema JSON file"
                    )

        # Add schemas to nav
        config["nav"].append(schema_dict)

        return files
