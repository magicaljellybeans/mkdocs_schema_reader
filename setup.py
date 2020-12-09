from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs_schema_reader",
    version="0.1.0",
    description="A MkDocs plugin to collate json schema files and convert them into markdown files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs, schema, json",
    url="https://github.com/magicaljellybeans/mkdocs_schema_reader",
    author="Tom Robinson",
    author_email="tome.robin@gmail.com",
    license="MIT",
    python_requires=">=2.7",
    install_requires=["mkdocs>=1.0.4", "jsonschema2md"],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "schema_reader = mkdocs_schema_reader.schema_reader:SchemaReader"
        ]
    },
)
