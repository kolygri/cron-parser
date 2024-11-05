# Cron Expression Parser

A command-line tool that parses a cron expression and expands each field to display the exact times at which it will run.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Output](#output)
- [Requirements](#requirements)
- [Features](#features)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

You can install the package using the provided wheel file:

```bash
pip install cron_parser-0.1.0-py3-none-any.whl
```

To uninstall the package:

```bash
pip uninstall cron_parser
```

## Usage

After installation, you can run the cron_parser script:

```bash
cron_parser "<cron_expression>"
```

Alternatively, if you are running from the source code or using Poetry:

```bash
poetry run cron_parser "<cron_expression>"
```

Note: You can skip `poetry run` if you're in a virtual environment or have installed the package globally.

## Example

Parse the cron expression `*/15 0 1,15 * 1-5 /usr/bin/find`:

```bash
cron_parser "*/15 0 1,15 * 1-5 /usr/bin/find"
```

## Output

```bash
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

## Requirements

- Python 3.11 or higher

## Features

- Supports standard cron format with five time fields (minute, hour, day of month, month, and day of week) followed by a command.
- Expands each field to show all possible execution times.
- Day of week values range from 1-7 (Monday=1, Sunday=7).
- Month values range from 1-12.

## Limitations

- Does not support special time strings like `@yearly`, `@monthly`, etc.
- Does not handle non-standard cron expressions or special characters like `?`, `L`, `W`, `#`.

## Future Enhancements

Planned features for future releases:

- Support for month and day-of-week names (e.g., Jan, Mon).
- Handling of special characters such as `?`, `L`, `W`, `#`.
- Support for special time strings like `@yearly`, `@monthly`.

## Contributing

Contributions are welcome! Please follow the steps below to contribute:

1. Ensure Poetry is installed:
    ```bash
    poetry --version
    ```
    If not installed, install Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/kolygri/cron_parser.git
    ```

3. Create a new branch:
    ```bash
    git checkout -b feature/your-feature
    ```

4. Navigate to the project directory:
    ```bash
    cd cron_parser
    ```

5. Create a virtual environment and install dependencies:
    ```bash
    poetry install
    ```

6. Activate the virtual environment:
    ```bash
    poetry shell
    ```

7. Make your changes and add tests:
    Ensure that any new functionality is covered by tests in the `tests/` directory.

8. Run tests:
    ```bash
    pytest
    ```
    Or, if not in the virtual environment:
    ```bash
    poetry run pytest
    ```

9. Check test coverage:
    ```bash
    poetry run coverage report
    ```

10. Format code:
    ```bash
    make format
    ```

11. Run linters:
    ```bash
    make lint
    ```

12. Build the package:
    ```bash
    poetry build
    ```

13. Commit your changes:
    ```bash
    git add .
    git commit -m "feat: Description of your feature"
    ```

14. Push your changes and create a pull request:
    ```bash
    git push origin feature/your-feature
    ```

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact Konstantin Grigorov at [k.l.grigorov@gmail.com](mailto:k.l.grigorov@gmail.com).
