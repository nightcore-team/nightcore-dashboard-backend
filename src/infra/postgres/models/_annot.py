from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Rules:
    chapters: list[Chapter]


@dataclass
class Chapter:
    number: int
    title: str
    rules: list[Rule]


@dataclass
class Rule:
    number: str
    text: str
    subrules: list[Rule]


class FAQPageAnnot(TypedDict):
    title: str
    description: str
    content: str
    image_url: str | None
