import sys
import xml.etree.ElementTree as etree

import anybadge

build_directory = "../build/"
report_directory = build_directory + "reports/"
badge_directory = build_directory + "badges/"


data = {}


def get_pylint_rating(filename=report_directory + "pylint_score.txt"):
    """
    Extracts 8.24 from 'Your code has been rated at 8.24/10
    (previous run: 8.24/10, +0.00)'.
    """

    with open(filename) as f:
        # non empty lines removed https://stackoverflow.com/a/4842070
        lines = [non_empty for non_empty in (line.strip() for line in f) if non_empty]

    return float(lines[-1].split("/10")[0].split(" ")[-1])


def parse_coverage(filename):
    """Parse the coverage report to return the percentage coverage.

    Returns:
        int or str: coverage percentage or 'unknown'
    """
    cov_tree = None
    cov_percent = "unknown"
    try:
        cov_tree = etree.parse(filename)
    except FileNotFoundError:
        print("WARNING code-coverage.xml file not found")

    if cov_tree:
        try:
            cov_root = cov_tree.getroot()
            branch_count = cov_root.get("branches-valid", "0")
            if branch_count != "0":
                branch_count = int(branch_count)
                branches_covered = int(cov_root.get("branches-covered", "0"))
                line_count = int(cov_root.get("lines-valid", "0"))
                lines_covered = int(cov_root.get("lines-covered", "0"))

                # This is how coverage.py's
                # terminal report calculates TOTAL coverage:
                numerator = lines_covered + branches_covered
                denominator = line_count + branch_count
                cov_percent = 100.0 * numerator / denominator
            else:
                cov_percent = 100.0 * float(cov_root.get("line-rate"))
        except AttributeError as err:
            print(
                "WARNING: Attribute not found. Make sure that the file "
                "code-coverage.xml has the correct 'line-rate' attribute: ",
                err,
            )
    return cov_percent


# Parse coverage report
coverage = parse_coverage(report_directory + "code-coverage.xml")
data["coverage"] = coverage

if len(sys.argv) > 1:
    data["rating"] = float(sys.argv[1])
else:
    data["rating"] = get_pylint_rating(report_directory + "pylint_score.txt")


def main():  # pylint: disable=too-many-branches,too-many-statements
    #################################################################
    # PYLINT
    # RATING ======================================================
    # Extract metric
    label = "pylint rating"
    metric = data["rating"]
    value = metric

    if metric == "unknown":
        value = "unknown"
        color = "#FF00FF"
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            default_color=color,
            value_prefix=" ",
        )
    elif 0 <= metric <= 10:
        # Define thresholds
        thresholds = {5: "red", 6: "orange", 8: "yellow", 10: "green"}
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            thresholds=thresholds,
            value_prefix=" ",
            value_suffix="/10 ",
        )
    else:
        # Undefined Metric
        color = "#FF00FF"
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            default_color=color,
            value_prefix=" ",
            value_suffix="% ",
        )

    # Write badge
    badge.write_badge(badge_directory + "rating.svg", overwrite=True)

    #################################################################
    # COVERAGE
    # PERCENTAGE ======================================================
    # Extract metric
    label = "coverage"
    metric = data["coverage"]
    value = metric

    if metric == "unknown":
        value = "unknown"
        color = "#FF00FF"
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            default_color=color,
            value_prefix=" ",
        )
    elif 0 <= metric <= 100:
        # Define thresholds
        thresholds = {50: "red", 60: "orange", 80: "yellow", 100: "green"}
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            thresholds=thresholds,
            value_format="%.2f",
            value_prefix=" ",
            value_suffix="% ",
        )
    else:
        # Undefined Metric
        color = "#FF00FF"
        # Create badge
        badge = anybadge.Badge(
            label=label,
            value=value,
            default_color=color,
            value_prefix=" ",
            value_suffix="% ",
        )

    # Write badge
    badge.write_badge(badge_directory + "coverage.svg", overwrite=True)


if __name__ == "__main__":
    main()
