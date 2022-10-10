from lazero.filesystem.io import readFile
import jinja2

template_configs = {
    "defaultFontname": "Arial",
    "defaultFontsize": 48,  # integer?
    "translationFontname": "Migu 1P",
    "translationFontsize": 48,
    "kanjiFontname": "Migu 1P",
    "kanjiFontsize": 46,
    "romajiFontname": "Migu 1P",
    "romajiFontsize": 38,
}
# template_configs = {'defaultFontname':'Anonymous Pro'}
template_path = "/root/Desktop/works/pyjom/tests/karaoke_effects/in2.ass.j2"
template = jinja2.Template(source=readFile(template_path))
template_configured = template.render(**template_configs)

print(template_configured)
