from setuptools import setup, find_packages


setup(
    name='mkdocs_schema_reader',
    version='0.1.0',
    description='A MkDocs plugin to collate json schema files and convert them into markdown files',
    long_description='',
    keywords='mkdocs, schema, json',
    url='',
    author='Tom Robinson',
    author_email='tome.robin@gail.com',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'jsonschema2md'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'schema_reader = mkdocs_schema_reader.schema_reader:SchemaReader'
        ]
    }
)
