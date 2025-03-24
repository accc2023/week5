# (C) Copyright Wieger Wesselink 2025. Distributed under the GPL-3.0-or-later
# Software License, (See accompanying file LICENSE or copy at
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Version 1
#
# Changelog:
#
# - The comparison of the segments between TODO markers has been made less strict with regards to whitespace.

import argparse
import re
from pathlib import Path

class Settings(object):
    no_filename_check = False


def extract_tags(text: str) -> dict[str, tuple[int, int]]:
    """
    Extracts all unique tags from the text along with their line numbers.

    Args:
        text (str): The input text containing the markers.

    Returns:
        dict[str, tuple[int, int]]: A dictionary where each key is a tag, and the value is a tuple
                                    with the line numbers of the begin and end markers.

    Raises:
        ValueError: If there are unmatched, duplicate, or overlapping tag pairs.
    """
    tags = {}
    tag_pattern = re.compile(r"//\s*(BEGIN|END)-TODO\((.*?)\)")

    for line_num, line in enumerate(text.splitlines(), start=1):
        match = tag_pattern.search(line)
        if match:
            marker_type, tag = match.groups()
            if marker_type == "BEGIN":
                if tag in tags:
                    raise ValueError(f"Duplicate BEGIN-TODO tag '{tag}' found at line {line_num}.")
                tags[tag] = (line_num, None)
            elif marker_type == "END":
                if tag not in tags:
                    raise ValueError(f"END-TODO tag '{tag}' at line {line_num} has no matching BEGIN-TODO.")
                if tags[tag][1] is not None:
                    raise ValueError(f"Duplicate END-TODO tag '{tag}' found at line {line_num}.")
                tags[tag] = (tags[tag][0], line_num)

    # Check for tags with missing END markers
    for tag, (begin_line, end_line) in tags.items():
        if end_line is None:
            raise ValueError(f"BEGIN-TODO tag '{tag}' at line {begin_line} has no matching END-TODO.")

    # Check for overlapping tag pairs
    sorted_tags = sorted(tags.items(), key=lambda x: x[1])
    for i in range(len(sorted_tags) - 1):
        current_tag, (current_begin, current_end) = sorted_tags[i]
        next_tag, (next_begin, next_end) = sorted_tags[i + 1]
        if current_end > next_begin:
            raise ValueError(f"Overlapping tags detected: '{current_tag}' (lines {current_begin}-{current_end}) and '{next_tag}' (lines {next_begin}-{next_end}).")

    return tags


def compare_tags(assignment_tags: dict[str, tuple[int, int]], submission_tags: dict[str, tuple[int, int]]) -> None:
    """
    Compares the tags from the assignemnt and the submission to check if they match.

    Args:
        assignment_tags (dict[str, tuple[int, int]]): The tags extracted from the assignment text.
        submission_tags (dict[str, tuple[int, int]]): The tags extracted from the submission text.

    Raises:
        ValueError: If the tags do not match, with specific details about the mismatch.
    """
    assignment_tag_order = list(assignment_tags.keys())
    submission_tag_order = list(submission_tags.keys())

    # Check for missing tags
    missing_tags = [tag for tag in assignment_tag_order if tag not in submission_tag_order]
    if missing_tags:
        raise ValueError(f"The following tags are missing in the submission: {', '.join(missing_tags)}")

    # Check for extra tags
    extra_tags = [tag for tag in submission_tag_order if tag not in assignment_tag_order]
    if extra_tags:
        raise ValueError(f"The following extra tags are present in the submission: {', '.join(extra_tags)}")

    # Check for order mismatch
    for i, (expected_tag, actual_tag) in enumerate(zip(assignment_tag_order, submission_tag_order)):
        if expected_tag != actual_tag:
            raise ValueError(
                f"Tag mismatch at position {i + 1}: expected '{expected_tag}' but found '{actual_tag}'."
            )


def extract_original_segments(text: str, tags: dict[str, tuple[int, int]]) -> list[str]:
    """
    Extracts segments of text outside the TODO markers.

    Args:
        text (str): The input text containing the markers.
        tags (dict[str, tuple[int, int]]): Extracted tags with their line numbers.

    Returns:
        list[str]: A list of text segments outside the TODO markers.
    """
    lines = text.splitlines()
    segments = []
    prev_end = 0

    sorted_tags = sorted(tags.values())

    for begin, end in sorted_tags:
        if prev_end < begin - 1:
            segments.append("\n".join(lines[prev_end:begin - 1]))
        prev_end = end

    if prev_end < len(lines):
        segments.append("\n".join(lines[prev_end:]))

    return segments


def insert_submission_tags(assignment_text: str, submission_text: str, assignment_tags: dict[str, tuple[int, int]], submission_tags: dict[str, tuple[int, int]]) -> str:
    """
    Replaces the text between TODO markers in the assignment text with the text from the submitted text.

    Args:
        assignment_text (str): The original assignment text.
        submission_text (str): The submitted text.
        assignment_tags (dict[str, tuple[int, int]]): The tags from the original assignment with line numbers.
        submission_tags (dict[str, tuple[int, int]]): The tags from the submitted text with line numbers.

    Returns:
        str: The assignment text with the submitted answers inserted between the TODO markers.
    """
    assignment_lines = assignment_text.splitlines()
    submission_lines = submission_text.splitlines()
    result_lines = []
    prev_end = 0

    for tag in assignment_tags:
        if tag not in submission_tags:
            raise ValueError(f"Tag '{tag}' found in assignment but not in submission.")

        assignment_begin, assignment_end = assignment_tags[tag]
        submission_begin, submission_end = submission_tags[tag]

        # Add text before the TODO block
        result_lines.extend(assignment_lines[prev_end:assignment_begin])

        # Add the BEGIN-TODO marker
        result_lines.append(assignment_lines[assignment_begin])

        # Add the student's submission
        result_lines.extend(submission_lines[submission_begin + 1:submission_end - 1])

        # Add the END-TODO marker
        result_lines.append(assignment_lines[assignment_end - 1])

        prev_end = assignment_end

    # Add any remaining text after the last TODO block
    result_lines.extend(assignment_lines[prev_end:])

    return "\n".join(result_lines)


def compare_segments(assignment_segments: list[str], submission_segments: list[str]) -> None:
    """
    Compares segments of the original assignment with those in the submission.

    Args:
        assignment_segments (list[str]): List of text segments from the original assignment.
        submission_segments (list[str]): List of text segments from the submitted text.

    Raises:
        ValueError: If any segment from the original assignment has been modified in the submitted text,
                    ignoring whitespace differences.
    """
    for assignment_segment, submission_segment in zip(assignment_segments, submission_segments):
        if re.sub(r"\s+", "", assignment_segment) != re.sub(r"\s+", "", submission_segment):
            raise ValueError(f"The original text has been modified:\n{assignment_segment}\n-------------------\n{submission_segment}")


def check_filenames(assignment_file: str, submission_file: str) -> None:
    """
    Validates that the provided assignment and submission filenames follow the expected naming convention.

    The assignment file must end with '-assignment.dfy'. The corresponding submission file
    must have the same base name but end with '-submission.dfy'.

    Parameters:
        assignment_file (str): The filename of the assignment, expected to end with '-assignment.dfy'.
        submission_file (str): The filename of the submission, expected to match the assignment filename
                               but end with '-submission.dfy'.

    Raises:
        ValueError: If the assignment file does not end with '-assignment.dfy'.
        ValueError: If the submission file name does not match the expected format and
                    the no_filename_check flag is not set.

    Side Effects:
        Prints a warning if the submission file name is incorrect but the no_filename_check flag is set.

    Example:
        check_filenames('homework1-assignment.dfy', 'homework1-submission.dfy')  # Passes validation
        check_filenames('homework1.txt', 'homework1-submission.dfy')             # Raises ValueError
    """
    if not assignment_file.endswith("-assignment.dfy"):
        raise ValueError("The assignment file must end with '-assignment.dfy'.")

    expected_submission_file = re.sub(r"-assignment.dfy$", "-submission.dfy", assignment_file)
    if submission_file != expected_submission_file:
        if Settings.no_filename_check:
            print(f"WARNING: The submission file must be named '{expected_submission_file}'.")
        else:
            raise ValueError(f"The submission file must be named '{expected_submission_file}'.")


def check_submission(assignment_file: str, submission_file: str) -> str:
    """
    Validates a student's submission against the original assignment.

    Args:
        assignment_text (str): The original assignment text.
        submission_text (str): The submitted text.

    Returns:
        str: 'The submission is ACCEPTED.' if all checks pass,
             otherwise returns 'The submission is REJECTED.' followed by the error message.
    """
    try:
        check_filenames(assignment_file, submission_file)
    except ValueError as e:
        return f'The submission is REJECTED.\n{e}'

    assignment_text = Path(assignment_file).read_text()
    submission_text = Path(submission_file).read_text()

    try:
        assignment_tags = extract_tags(assignment_text)
        submission_tags = extract_tags(submission_text)
    except ValueError as e:
        return f'The submission is REJECTED.\n{e}'

    try:
        compare_tags(assignment_tags, submission_tags)
    except ValueError as e:
        return f'The submission is REJECTED.\n{e}'

    assignment_segments = extract_original_segments(assignment_text, assignment_tags)
    submission_segments = extract_original_segments(submission_text, submission_tags)

    try:
        compare_segments(assignment_segments, submission_segments)
    except ValueError as e:
        return f'The submission is REJECTED.\n{e}'

    return 'The submission is ACCEPTED.'


def main():
    cmdline_parser = argparse.ArgumentParser(description='Check a submission with TODO markers against the original assignment.')
    cmdline_parser.add_argument('assignment', metavar='FILENAME', type=str, help='a .dfy file containing the assignment.')
    cmdline_parser.add_argument('submission', metavar='FILENAME', type=str, help='a .dfy file containing the submitted answer.')
    cmdline_parser.add_argument('--no-filename-check', help=argparse.SUPPRESS, action='store_true')
    args = cmdline_parser.parse_args()

    if args.no_filename_check:
        Settings.no_filename_check = True

    print(f'Comparing the assignment `{args.assignment}` with the submission `{args.submission}`')

    if not Path(args.assignment).is_file():
        print(f'ERROR: Assignment file {args.assignment} does not exist.')
        return

    if not Path(args.submission).is_file():
        print(f'ERROR: Submission file {args.submission} does not exist.')
        return

    feedback = check_submission(args.assignment, args.submission)
    print(feedback)
    print('')


if __name__ == '__main__':
    main()
