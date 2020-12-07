import os
import jsonschema2md
import json

from mkdocs.structure.files import File
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin


class SchemaReader(BasePlugin):

    def on_files(self, files, config):
        parser = jsonschema2md.Parser()
        excludedirs = set(['venv', 'env', '__pycache__'])

        for root, dirs, filenames in os.walk('../'):
            dirs[:] = [d for d in dirs if d not in excludedirs]
            for file in filenames:
                if file.endswith('.json'):
                    with open(os.path.join(root, file)) as f:
                        data = f.read()
                        schema_syntax = ["$schema", "$ref"]
                        if any(x in data for x in schema_syntax):
                            # generate markdown file in site
                            path = f"./site/schema/{file[:-5]}.md"
                            with open(path, "w") as md:
                                lines = parser.parse_schema(json.loads(data))
                                for line in lines:
                                    md.write(line)
                                files.append(File(path, config["docs_dir"], config["site_dir"], config["use_directory_urls"]))
        return files
