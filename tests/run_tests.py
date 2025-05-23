# run_tests.py
import argparse
import unittest
from pathlib import Path
import sys
from pathlib import Path

# Add project root (parent of tests/) to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


parser = argparse.ArgumentParser(description="Run tests by type and target.")
parser.add_argument("--type", choices=["unit", "integration", "all"], default="all")
parser.add_argument("--target", help="Target test file keyword (e.g., podbean, spotify)")

args = parser.parse_args()

base_dirs = {
    "unit": "tests/unit",
    "integration": "tests/integration"
}

def discover_tests(path):
    return unittest.TestLoader().discover(start_dir=path)

def discover_specific_file(test_type, keyword):
    path = Path(base_dirs[test_type])
    suites = []
    filename = f"test_{keyword}.py"

    path = Path(base_dirs[test_type])

    print(path)
    for file in path.glob(f"test_*{keyword}*.py"):
        module_path = file.with_suffix('').as_posix().replace('/', '.')

        print(f"🔍 Found test file: {file} → importing {module_path}")
        try:
            suite = unittest.TestLoader().loadTestsFromName(module_path)
            print(f"✅ Loaded {module_path} with {suite.countTestCases()} test(s)")
            suites.append(suite)
        except Exception as e:
            print(f"❌ Failed to load {module_path}: {e}")

    if suites:
        return unittest.TestSuite(suites)
    else:
        print("⚠️ No test files matched the keyword.")
        return None


suites = []

if args.type == "all" and not args.target:
    suites.append(discover_tests(base_dirs["unit"]))
    suites.append(discover_tests(base_dirs["integration"]))
elif args.type != "all" and not args.target:
    suites.append(discover_tests(base_dirs[args.type]))
elif args.type != "all" and args.target:
    suite = discover_specific_file(args.type, args.target)
    if suite:
        suites.append(suite)
else:
    print("Invalid combination of arguments.")
    sys.exit(1)

runner = unittest.TextTestRunner(verbosity=2)
for suite in suites:
    runner.run(suite)

