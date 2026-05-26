#!/usr/bin/env python3

import argparse
import csv
import html
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


MERCHANT_RULES = [
    (r"^DOORDASH", "DoorDash"),
    (r"^DD \*DOORDASH", "DoorDash"),
    (r"^WALMART", "Walmart"),
    (r"^Walmart\+ Member", "Walmart+"),
    (r"^IC\* COSTCO BY INSTACAR", "Costco via Instacart"),
    (r"^IC\* INSTACART\*SUBSCRIP", "Instacart+ membership"),
    (r"^IC\* INSTACART", "Instacart"),
    (r"^AMAZON\.COM", "Amazon"),
    (r"^Amazon\.com", "Amazon"),
    (r"^AMZN", "Amazon"),
    (r"^AIRBNB", "Airbnb"),
    (r"^MAVERIK", "Maverik"),
    (r"^BURN SARATOGA SPRINGS", "Burn Saratoga Springs"),
    (r"^BURN BOOT CAMP", "Burn Boot Camp"),
    (r"^UNFILTERED", "Unfiltered"),
    (r"^LULULEMON", "lululemon"),
    (r"^ANTHROPOLOGIE", "Anthropologie"),
    (r"^CHARLES TYRWHITT", "Charles Tyrwhitt"),
    (r"^SP VUORI", "Vuori"),
    (r"^SP EVEREVE", "Evereve"),
    (r"^LEHI CITY CORPORATION", "Example City A City"),
    (r"^BANFIELD", "Banfield"),
    (r"^WASATCH BROADBAND", "Wasatch Broadband"),
    (r"^NETFLIX", "Netflix"),
    (r"^HLU\*HULUPLUS", "Hulu"),
    (r"^PAYPAL \*DISNEY PLUS", "Disney+"),
    (r"^INTERACTION-DESIGN\.ORG", "Interaction Design Inc"),
    (r"^SILVER BEAR SWIM", "Silver Bear Swim"),
    (r"^SQ \*COMMUNAL", "Communal"),
    (r"^GRAND AMERICA FOOD", "Grand America Food & Bev"),
]


@dataclass
class Txn:
    txn_date: datetime
    post_date: datetime
    description: str
    category: str
    amount: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a Chase activity export and print a household-spend report."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        help="Path to a Chase CSV export. Defaults to the newest Chase*_Activity*.CSV in ~/Downloads.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="How many merchants and example transactions to show per category.",
    )
    parser.add_argument(
        "--raw-categories",
        action="store_true",
        help="Do not reclassify Walmart/Instacart into Groceries.",
    )
    return parser.parse_args()


def find_latest_csv() -> Path:
    downloads = Path.home() / "Downloads"
    candidates = sorted(
        downloads.glob("Chase*_Activity*.CSV"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise SystemExit("No Chase*_Activity*.CSV files found in ~/Downloads.")
    return candidates[0]


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%m/%d/%Y")


def load_transactions(csv_path: Path) -> list[Txn]:
    txns: list[Txn] = []
    with csv_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            txn_type = row["Type"].strip()
            if txn_type not in {"Sale", "Return"}:
                continue
            amount = -float(row["Amount"])
            if abs(amount) < 0.005:
                continue
            txns.append(
                Txn(
                    txn_date=parse_date(row["Transaction Date"]),
                    post_date=parse_date(row["Post Date"]),
                    description=html.unescape(row["Description"].strip()),
                    category=row["Category"].strip(),
                    amount=amount,
                )
            )
    if not txns:
        raise SystemExit(f"No Sale/Return transactions found in {csv_path}.")
    return txns


def adjusted_category(txn: Txn, raw_categories: bool) -> str:
    if raw_categories:
        return txn.category
    desc = txn.description.lower()
    if "walmart" in desc or "instacar" in desc:
        return "Groceries"
    if "walmart+ member" in desc:
        return "Groceries"
    return txn.category


def normalize_merchant(description: str) -> str:
    for pattern, label in MERCHANT_RULES:
        if re.search(pattern, description, re.IGNORECASE):
            return label
    compact = re.sub(r"\s+", " ", description).strip()
    return compact[:48]


def money(value: float) -> str:
    return f"${value:,.2f}"


def share(value: float, total: float) -> str:
    return f"{(value / total * 100):.1f}%"


def top_positive(txns: Iterable[Txn], limit: int) -> list[Txn]:
    return sorted((txn for txn in txns if txn.amount > 0), key=lambda txn: txn.amount, reverse=True)[
        :limit
    ]


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_path).expanduser() if args.csv_path else find_latest_csv()
    txns = load_transactions(csv_path)

    overall_total = sum(txn.amount for txn in txns)
    by_category: dict[str, list[Txn]] = defaultdict(list)
    for txn in txns:
        by_category[adjusted_category(txn, args.raw_categories)].append(txn)

    sorted_categories = sorted(
        by_category.items(),
        key=lambda item: sum(txn.amount for txn in item[1]),
        reverse=True,
    )

    food_total = sum(txn.amount for txn in txns if txn.category == "Food & Drink")
    doordash_total = sum(txn.amount for txn in txns if "doordash" in txn.description.lower())
    grocery_reclass_total = sum(
        txn.amount
        for txn in txns
        if ("walmart" in txn.description.lower() or "instacar" in txn.description.lower())
    )

    dates = sorted(txn.txn_date for txn in txns)

    print("# Chase Spend Report")
    print()
    print(f"- CSV: {csv_path}")
    print(
        f"- Period: {dates[0].strftime('%B %d, %Y')} through {dates[-1].strftime('%B %d, %Y')}"
    )
    print(f"- Total spend reviewed: {money(overall_total)}")
    if not args.raw_categories:
        print(
            f"- Reclassified to Groceries: {money(grocery_reclass_total)} from Walmart/Instacart-related transactions"
        )
    if food_total:
        print(
            f"- DoorDash inside Food & Drink: {money(doordash_total)} ({share(doordash_total, food_total)} of Food & Drink)"
        )

    print()
    print("## Category Summary")
    print()
    for category, category_txns in sorted_categories:
        category_total = sum(txn.amount for txn in category_txns)
        if category_total <= 0:
            continue
        print(f"- {category}: {money(category_total)} ({share(category_total, overall_total)})")

    print()
    print("## Category Details")
    print()
    for category, category_txns in sorted_categories:
        category_total = sum(txn.amount for txn in category_txns)
        if category_total <= 0:
            continue

        merchant_totals: dict[str, float] = defaultdict(float)
        for txn in category_txns:
            merchant_totals[normalize_merchant(txn.description)] += txn.amount

        top_merchants = sorted(
            ((merchant, total) for merchant, total in merchant_totals.items() if total > 0),
            key=lambda item: item[1],
            reverse=True,
        )[: args.top]

        examples = top_positive(category_txns, args.top)

        print(f"### {category}")
        print(f"- Total: {money(category_total)} ({share(category_total, overall_total)})")
        if top_merchants:
            merchant_line = ", ".join(f"{name} {money(total)}" for name, total in top_merchants)
            print(f"- Top merchants: {merchant_line}")
        if examples:
            example_line = "; ".join(
                f"{txn.txn_date.strftime('%b %d')}: {txn.description} {money(txn.amount)}"
                for txn in examples
            )
            print(f"- Example transactions: {example_line}")
        print()


if __name__ == "__main__":
    main()
