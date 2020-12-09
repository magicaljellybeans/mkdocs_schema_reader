# mkdocs schema reader plugin 

This is a plugin that scans the entire repository for JSON Schema files, converts them to markdown and builds them into your documentation.

## Setup

Install the plugin using pip:

`pip install mkdocs-schema-reader`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - schema-reader
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Usage

Just activate the plugin and it will operate when normal mkdocs command are used like `mkdocs serve'
