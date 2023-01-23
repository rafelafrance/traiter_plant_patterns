import collections
import html
import itertools
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

import jinja2

from . import writer_utils as w_utils


COLOR_COUNT = 14
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])
BORDERS = itertools.cycle([f"bb{i}" for i in range(COLOR_COUNT)])

SKIPS = {"start", "end", "trait", "part", "subpart"}

FormattedTrait = collections.namedtuple("FormattedTrait", "text traits raw")
TraitRow = collections.namedtuple("TraitRow", "label data")
SortableTrait = collections.namedtuple("SortableTrait", "label start trait title")


@dataclass(kw_only=True)
class HtmlWriterRow:
    formatted_text: str
    formatted_traits: list[TraitRow] = field(default_factory=list)


class CssClasses:
    def __init__(self):
        self.classes = {}

    def __getitem__(self, label):
        if label not in self.classes:
            self.classes[label] = next(BACKGROUNDS)
        return self.classes[label]


class HtmlWriter:
    def __init__(self, template_dir, out_path):
        self.template_dir = template_dir
        self.out_path = out_path
        self.css_classes = CssClasses()
        self.formatted = []

    def write(self, rows, in_file_name=""):
        raise NotImplementedError()

    def format_text(self, row):
        """Wrap traits in the text with <spans> that can be formatted with CSS."""
        frags = []
        prev = 0

        for trait in row.traits:
            start = trait["start"]
            end = trait["end"]

            if prev < start:
                frags.append(html.escape(row.text[prev:start]))

            label = w_utils.get_label(trait)
            cls = self.css_classes[label]

            title = ", ".join(
                f"{k}:&nbsp;{v}"
                for k, v in trait.items()
                if k not in w_utils.TITLE_SKIPS
            )

            frags.append(f'<span class="{cls}" title="{title}">')
            frags.append(html.escape(row.text[start:end]))
            frags.append("</span>")
            prev = end

        if len(row.text) > prev:
            frags.append(html.escape(row.text[prev:]))

        text = "".join(frags)
        return text

    def format_traits(self, row):
        """Group traits for display in their own table."""
        traits = []

        sortable = []
        for trait in row.traits:
            label = w_utils.get_label(trait)
            title = row.text[trait["start"] : trait["end"]]
            if trait["trait"] not in w_utils.DO_NOT_SHOW:
                sortable.append(SortableTrait(label, trait["start"], trait, title))

        sortable = sorted(sortable)

        for label, grouped in itertools.groupby(sortable, key=lambda x: x.label):
            cls = self.css_classes[label]
            label = f'<span class="{cls}">{label}</span>'
            trait_list = []
            for trait in grouped:
                fields = ", ".join(
                    f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                    for k, v in trait.trait.items()
                    if k not in w_utils.TRAIT_SKIPS
                )
                if fields:
                    trait_list.append(fields)

            if trait_list:
                traits.append(TraitRow(label, "<br/>".join(trait_list)))

        return traits

    def write_template(self, in_file_name=""):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True,
        )

        template = env.get_template("html_writer.html").render(
            now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
            file_name=in_file_name,
            rows=self.formatted,
        )

        with open(self.out_path, "w") as html_file:
            html_file.write(template)
