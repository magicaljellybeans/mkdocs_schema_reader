# mkdocs schema reader plugin 

This is a plugin that scans the specified directories and files for JSON Schema files, converts them to markdown and builds them into your documentation.

## Setup

Install the plugin using pip:

`pip install mkdocs-schema-reader`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - schema-reader
```

Then, specify folders and files that you want to include in `mkdocs.yml` relative to it's location, like so:
```yaml
plugins:
  - search
  - schema-reader:
      include: 
        - "../JSONSchema/"
        - "../example/directory/schema.json"
```

Specified directories will be scanned for schema json files, so consider specifying individual files for expansive directories.

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Usage

Just activate the plugin, specify directories and files in the manner shown above, and it will operate when normal mkdocs commands are used like `mkdocs serve'
