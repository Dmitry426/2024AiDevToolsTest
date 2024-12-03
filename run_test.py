import argparse
import subprocess
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(
        description=(
            "Fast api hw test ."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--repo_name",
        default="",
        help="git repository of a student  ",
        required=False,
    )
    parser.add_argument(
        "--group",
        default="",
        help="Student group base, middle or pro ",
        required=True,
    )

    return parser.parse_args()

def run_tests_and_capture_json():
    args = get_args()
    path = Path(__file__).resolve().parent / 'hw_tester' / 'tests'
    if args.group == "base":
        path = path / 'test_base_api.py'
    if args.group == "middle":
        path = path / 'test_middle_api.py'
    if args.group == "pro":
        path = path / 'test_pro_api.py'

    result = subprocess.run(
        ['pytest', '-v',str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.stderr:
        print(result.stderr)
        raise Exception('test_not_done')
    
    print(result.stdout)

if __name__ == '__main__':
    run_tests_and_capture_json()
