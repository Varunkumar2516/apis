from jinja2 import Environment
from jinja2 import FileSystemLoader

env = Environment(
    loader=FileSystemLoader("app/templates")
)

def render_template(template_name, **kwargs):

    template = env.get_template(template_name)

    return template.render(**kwargs)