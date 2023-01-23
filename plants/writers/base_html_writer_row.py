import collections
from dataclasses import dataclass
from dataclasses import field


FormattedTrait = collections.namedtuple("FormattedTrait", "text traits raw")
TraitRow = collections.namedtuple("TraitRow", "label data")


@dataclass(kw_only=True)
class BaseRow:
    formatted_text: str
    formatted_traits: list[TraitRow] = field(default_factory=list)
