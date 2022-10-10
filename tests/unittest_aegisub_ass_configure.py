    from lazero.filesystem.io import readFile
    template_path = ""
    template = jinja2.Template(source=readFile(template_path))
    template_configured = template.render(**template_configs)
