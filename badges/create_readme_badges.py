# import anybadge

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


data["rating"] = get_pylint_rating(report_directory + "pylint_score.txt")


def main():  # pylint: disable=too-many-branches,too-many-statements
    pass


if __name__ == "__main__":
    main()
