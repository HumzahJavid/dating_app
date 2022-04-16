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


def parse_junit_tree(element, test_summary=None):
    """Recursively parse and extract a summary of a JUnit xml element tree.

    Args:
        element (xml.etree.Element): XML Element
        test_summary (dict): Summary of the JUnit XML report

    Returns:
        dict: Summary of Junit results.

    Notes:
        For JUnit XML schema see:
            <https://github.com/windyroad/JUnit-Schema>
    """
    # Create default entries in the stats dictionary if required.
    if not test_summary:
        test_summary = dict(
            testsuites=dict(tests=0, failures=0),
            testsuite=dict(tests=0, failures=0, skipped=0, errors=0),
            testcase=dict(tests=0, failures=0, skipped=0, errors=0),
        )

    # Parse top level <testsuites> or <testsuite> tags.
    if element.tag in ["testsuites", "testsuite"]:

        for attr in test_summary[element.tag]:
            test_summary[element.tag][attr] += int(element.get(attr, 0))

        for child in element:
            parse_junit_tree(child, test_summary)

    # Parse <testcase> tag. This is a child of testsuite.
    if element.tag == "testcase":
        key = "testcase"

        # Incrememnt test case counter.
        test_summary[key]["tests"] += 1

        # Parse child <error>, <skipped>, <failure> tags.
        for child in element:
            parse_junit_tree(child, test_summary)

    # Parse <error>, <skipped>, and <failure> tags. Children of testcase.
    if element.tag in ["error", "skipped", "failure"]:
        key = element.tag
        if element.tag == "error":
            key = "errors"
        elif element.tag == "failure":
            key = "failures"
        test_summary["testcase"][key] += 1

    # Parse <system-out>, <system-err>, and <properties> tags.
    # Children of testsuite.
    if element.tag in ["system-out", "system-err", "properties"]:
        pass

    return test_summary


def count_junit_metrics(filename):
    """Collect metrics from a JUnit XML file.

    Used to parse unit tests and linting results.

    Args:
        filename (str): Filename path of JUnit file

    Returns:
        dict: Summary of Unit test or linting results

    """
    try:
        root_elem = etree.parse(filename).getroot()
        if root_elem.tag not in ["testsuites", "testsuite"]:
            raise ValueError("Invalid JUnit XML file.")
        stats = parse_junit_tree(root_elem)
        result = dict(errors=0, failures=0, tests=0, skipped=0)
        for key in result:
            if key in ["tests", "failures"]:
                result[key] = max(
                    stats["testsuites"][key],
                    stats["testsuite"][key],
                    stats["testcase"][key],
                )
            else:
                result[key] = max(stats["testsuite"][key], stats["testcase"][key])
        result["total"] = result["tests"]
        del result["tests"]
    except (FileNotFoundError, etree.ParseError, ValueError) as expt:
        print(
            "Exception parsing '%s', returning empty results..: %s",
            filename,
            expt,
        )
        result = dict(errors="unknown", failures="unknown", total="unknown", skipped=0)

    return result


# Parse pylint rating
if len(sys.argv) > 1:
    data["rating"] = float(sys.argv[1])
else:
    data["rating"] = get_pylint_rating(report_directory + "pylint_score.txt")

# Parse coverage report
data["coverage"] = parse_coverage(report_directory + "code-coverage.xml")

# Parse JUnit XML linting report
data["lint"] = count_junit_metrics(report_directory + "linting.xml")


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

    ###############################################################
    # LINT
    # ERRORS ======================================================
    # Extract metric
    label = "lint errors"
    metric = data["lint"]["errors"]
    value = metric

    # set colour
    if metric == "unknown":
        value = "unknown"
        color = "#FF00FF"
    elif metric == 0:
        color = "green"
    elif metric > 0:
        color = "yellow"
    else:
        # Undefined Metric
        color = "#FF00FF"

    # Create badge
    badge = anybadge.Badge(
        label=label,
        value=value,
        default_color=color,
        value_prefix=" ",
        value_suffix=" ",
    )

    # Write badge
    badge.write_badge(badge_directory + "lint_errors.svg", overwrite=True)

    # FAILURES ===================================================
    # Extract metric
    label = "lint failures"
    metric = data["lint"]["failures"]
    value = metric

    # set colour
    if metric == "unknown":
        value = "unknown"
        color = "#FF00FF"
    elif metric == 0:
        color = "green"
    elif metric > 0:
        color = "red"
    else:
        # Undefined Metric
        color = "#FF00FF"

    # Create badge
    badge = anybadge.Badge(
        label=label,
        value=value,
        default_color=color,
        value_prefix=" ",
        value_suffix=" ",
    )

    # Write badge
    badge.write_badge(badge_directory + "lint_failures.svg", overwrite=True)

    # TOTAL ========================================================
    # Extract metric
    label = "lint tests"
    metric = data["lint"]["total"]
    value = metric

    # set colour
    if metric == "unknown":
        value = "unknown"
        color = "#FF00FF"
    elif metric > 0:
        color = "lightgrey"
    else:
        # Undefined Metric
        color = "#FF00FF"

    # Create badge
    badge = anybadge.Badge(
        label=label,
        value=value,
        default_color=color,
        value_prefix=" ",
        value_suffix=" ",
    )

    # Write badge
    badge.write_badge(badge_directory + "lint_total.svg", overwrite=True)


if __name__ == "__main__":
    main()
