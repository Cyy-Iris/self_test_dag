# Automodeling Data Pipeline Contribution guidelines

## Code Style

In general, code formatting is done using `black` this helps in making the code standard and limit also the size of diff when reviewing code changes. For everything else such as how to document modules, packages, functions we try to follow google guidelines:
https://google.github.io/styleguide/pyguide.html.

## Code Testing

The code is tested with the `Pytest` library. For each defined functions, unit test should be defined in `tests/unit`. For testing several tasks chained together we can also define tests in `tests/integration`. Finally for testing a whole dag end to end tests can be defined in `tests/e2e`.

## Code Documentation

We try to respect the guidelines in https://google.github.io/styleguide/pyguide.html. Furthermore documentation of the modules, packages, and functions are used to generate the documentation website with sphinx.

