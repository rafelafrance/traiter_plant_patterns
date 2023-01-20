import collections
import itertools
from datetime import datetime

import jinja2

COLOR_COUNT = 14
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])
BORDERS = itertools.cycle([f"bb{i}" for i in range(COLOR_COUNT)])

Formatted = collections.namedtuple("Formatted", "text traits")
Trait = collections.namedtuple("Trait", "label data")
SortableTrait = collections.namedtuple("SortableTrait", "label start trait title")


class CssClasses:
    def __int__(self):
        self.classes = {}

    def __getitem__(self, label):
        if label not in self.classes:
            self.classes[label] = next(BACKGROUNDS)
        return self.classes[label]


def write_template(args, root_dir, proj_dir, formatted):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            f"{root_dir}/{proj_dir}/pylib/writers/templates"
        ),
        autoescape=True,
    )

    template = env.get_template("html_writer.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=args.in_text.name,
        data=formatted,
    )

    with open(args.out_html, "w") as html_file:
        html_file.write(template)
        html_file.close()
