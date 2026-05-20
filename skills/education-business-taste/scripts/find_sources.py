#!/usr/bin/env python3
"""Print or run recurring searches for education-business source refreshes."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceCluster:
    topic: str
    name: str
    urls: tuple[str, ...]
    web_queries: tuple[str, ...]
    youtube_queries: tuple[str, ...] = ()


CLUSTERS: tuple[SourceCluster, ...] = (
    SourceCluster(
        topic="offer",
        name="Hormozi / Acquisition.com / Skool",
        urls=(
            "https://www.acquisition.com/",
            "https://shop.acquisition.com/",
            "https://www.skool.com/@hormozi",
            "https://www.hormozigames.com/",
        ),
        web_queries=(
            "Alex Hormozi 100M Offers education business",
            "Alex Hormozi Skool community business",
            "Leila Hormozi education business operations",
        ),
        youtube_queries=(
            "Alex Hormozi education business offer course community",
            "Alex Hormozi Skool community business",
        ),
    ),
    SourceCluster(
        topic="cohort",
        name="Maven / Wes Kao / Gagan Biyani / altMBA",
        urls=(
            "https://www.weskao.com/about/",
            "https://maven.com/maven/course-accelerator",
            "https://maven.com/wes-kao",
            "https://www.gaganbiyani.com/",
            "https://about.udemy.com/company/",
            "https://www.sethgodin.com/",
        ),
        web_queries=(
            "Wes Kao cohort based course curriculum design",
            "Wes Kao course market fit",
            "Gagan Biyani Maven cohort based courses",
            "Seth Godin altMBA online workshop",
        ),
        youtube_queries=(
            "Wes Kao cohort based courses",
            "Gagan Biyani Maven Udemy education",
            "Seth Godin altMBA cohort",
        ),
    ),
    SourceCluster(
        topic="upskilling",
        name="Reforge / Section / CXL",
        urls=(
            "https://www.reforge.com/",
            "https://www.reforge.com/blog/reforge-raises-series-b",
            "https://www.sectionai.com/about",
            "https://profgmedia.com/classes",
            "https://cxl.com/",
        ),
        web_queries=(
            "Brian Balfour Reforge program design",
            "Reforge membership expert network education",
            "Scott Galloway Section business education",
            "Peep Laja CXL institute marketing education",
        ),
        youtube_queries=(
            "Brian Balfour Reforge education",
            "Scott Galloway Section business education",
            "Peep Laja CXL education",
        ),
    ),
    SourceCluster(
        topic="bootcamp",
        name="Coding Bootcamps and Career-Change Education",
        urls=(
            "https://www.codesmith.io/about",
            "https://www.willsentance.com/",
            "https://flatironschool.com/about-us/",
            "https://www.appacademy.io/",
            "https://www.hackreactor.com/about/",
            "https://www.cirr.org/",
        ),
        web_queries=(
            "Will Sentance Codesmith pedagogy outcomes",
            "Flatiron School Adam Enbar Avi Flombaum outcomes",
            "Kush Patel App Academy deferred tuition job guarantee",
            "coding bootcamp outcomes reporting methodology CIRR",
            "2U Trilogy boot camps microcredentials 2024",
        ),
        youtube_queries=(
            "Will Sentance Codesmith pedagogy",
            "coding bootcamp founder outcomes reporting",
            "App Academy deferred tuition founder",
        ),
    ),
    SourceCluster(
        topic="caution",
        name="BloomTech / Lambda and Outcomes-Claim Risk",
        urls=(
            "https://www.consumerfinance.gov/enforcement/actions/bloomtech-inc-and-austen-allred/",
            "https://www.cirr.org/",
        ),
        web_queries=(
            "CFPB BloomTech Austen Allred income share agreements",
            "Lambda School outcomes reporting ISA",
            "coding bootcamp job placement claims enforcement",
        ),
        youtube_queries=(
            "Austen Allred Lambda School ISA outcomes",
            "BloomTech Lambda School CFPB",
        ),
    ),
    SourceCluster(
        topic="learning",
        name="Learning Science and Instructional Design",
        urls=(
            "https://usablelearning.com/about/",
            "https://designbetterlearning.com/about/",
            "https://www.makeitstick.com/",
            "https://www.coursera.org/learn/learning-how-to-learn",
        ),
        web_queries=(
            "Julie Dirksen Design for How People Learn course design",
            "Make It Stick retrieval practice spaced repetition interleaving",
            "Barbara Oakley Learning How to Learn course design",
        ),
        youtube_queries=(
            "Julie Dirksen learning design behavior change",
            "Make It Stick retrieval practice",
            "Barbara Oakley Learning How to Learn",
        ),
    ),
)


def selected_clusters(topic: str) -> Iterable[SourceCluster]:
    if topic == "all":
        return CLUSTERS
    return tuple(cluster for cluster in CLUSTERS if cluster.topic == topic)


def markdown(clusters: Iterable[SourceCluster]) -> str:
    sections: list[str] = []
    for cluster in clusters:
        lines = [f"## {cluster.name}", "", f"Topic: `{cluster.topic}`", "", "URLs:"]
        lines.extend(f"- {url}" for url in cluster.urls)
        lines.extend(("", "Web searches:"))
        lines.extend(f"- {query}" for query in cluster.web_queries)
        if cluster.youtube_queries:
            lines.extend(("", "YouTube searches:"))
            lines.extend(
                "- yt-dlp --flat-playlist --print '%(upload_date)s|%(channel)s|%(webpage_url)s|%(title)s' "
                + json.dumps(f"ytsearch10:{query}")
                for query in cluster.youtube_queries
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def run_youtube(clusters: Iterable[SourceCluster], limit: int) -> int:
    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed or not on PATH.")
        return 1

    exit_code = 0
    for cluster in clusters:
        for query in cluster.youtube_queries:
            print(f"\n## {cluster.name}: {query}")
            command = [
                "yt-dlp",
                "--flat-playlist",
                "--playlist-end",
                str(limit),
                "--print",
                "%(upload_date)s|%(channel)s|%(webpage_url)s|%(title)s",
                f"ytsearch{limit}:{query}",
            ]
            result = subprocess.run(command, check=False, text=True)
            if result.returncode != 0:
                exit_code = result.returncode
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--topic",
        choices=("all", "offer", "cohort", "upskilling", "bootcamp", "caution", "learning"),
        default="all",
    )
    parser.add_argument("--json", action="store_true", help="Print source clusters as JSON.")
    parser.add_argument("--run-youtube", action="store_true", help="Run yt-dlp searches.")
    parser.add_argument("--limit", type=int, default=10, help="YouTube result limit per query.")
    args = parser.parse_args()

    clusters = tuple(selected_clusters(args.topic))
    if args.run_youtube:
        return run_youtube(clusters, args.limit)

    if args.json:
        print(json.dumps([cluster.__dict__ for cluster in clusters], indent=2))
    else:
        print(markdown(clusters))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
