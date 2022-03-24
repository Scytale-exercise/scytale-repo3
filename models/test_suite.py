import inspect
import inquirer
import time
from cli.utils import get_loader, get_success_message, get_failure_message


def test_a():
    print("Doing some stuff...")


class TestSuite:

    def __init__(self, integration_instance):
        self.integration = integration_instance
        self.methods = inspect.getmembers(integration_instance, predicate=inspect.ismethod)

        self.tests = {}

        for method in self.methods:
            method_name = method[1].__doc__
            if method_name:
                self.tests[method_name] = method[1]

        self.choices = self.tests.keys()

    def run_test(self, test_name):
        """Run Test"""
        if test_name in self.tests:
            success = True
            spinner = get_loader(f"Running test: {test_name}" + "\n")
            spinner.start()
            time.sleep(2)
            spinner.stop()

            try:
                self.tests[test_name]()
            except Exception:
                success = False
                raise
            finally:
                if success:
                    print(get_success_message(f"{test_name} ran successfully"))
                else:
                    print(get_failure_message(f"{test_name} run failed"))

        else:
            print("Invalid test name")

    def select_test(self):
        questions = [
            inquirer.List('test_name',
                          message=f"Which {self.integration.display_name} test would you like to run?",
                          choices=self.choices,
                          carousel=True
                          ),
        ]
        answers = inquirer.prompt(questions)
        self.run_test(answers['test_name'])