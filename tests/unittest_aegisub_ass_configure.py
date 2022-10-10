from lazero.filesystem.io import readFile
import jinja2
template_configs = {'defaultFontName':...}
# template_configs = {'defaultFontName':...}
template_path = "/root/Desktop/works/pyjom/tests/karaoke_effects/in2.ass.j2"
template = jinja2.Template(source=readFile(template_path))
template_configured = template.render(**template_configs)

print(template_configured)