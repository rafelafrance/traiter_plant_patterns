#!/usr/bin/env python3
import argparse
import logging
import textwrap
from pathlib import Path

from pylib.traits.habit import habit_compilers as habit
from pylib.traits.link_part import link_part_compilers as link_part
from pylib.traits.part import part_compilers as part
from spacy.lang.en import English
from traiter.pylib import log


class Matchers:
    def __init__(self, name, matchers, dir_=None):
        self.name = name
        self.matchers = matchers if isinstance(matchers, list) else [matchers]
        self.dir = dir_ if dir_ else name


def main():
    log.started()

    all_matchers = [
        Matchers("habit", habit.COMPILERS),
        Matchers("part", part.COMPILERS),
        Matchers("link_part", link_part.LINK_PART, "link_part"),
        Matchers("link_part_once", link_part.LINK_PART_ONCE, "link_part"),
        Matchers("link_subpart", link_part.LINK_SUBPART, "link_part"),
    ]

    args = parse_args()

    for matchers in all_matchers:
        if args.trait and matchers.dir != args.trait:
            continue

        logging.info(f"Compiling {matchers.name}")

        patterns = []
        for matcher in matchers.matchers:
            for pattern in matcher.patterns:
                line = {
                    "label": matcher.label,
                    "pattern": pattern,
                }
                if matcher.id:
                    line["id"] = matcher.id
                patterns.append(line)

        nlp = English()
        ruler = nlp.add_pipe("entity_ruler")
        ruler.add_patterns(patterns)

        dir_ = args.traits_dir / matchers.dir

        path = dir_ / f"{matchers.name}_patterns.jsonl"
        ruler.to_disk(path)

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert pattern objects into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--traits-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Save the term JSONL files to this directory.""",
    )

    arg_parser.add_argument("--trait", help="Only compile patterns for this trait.")

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
