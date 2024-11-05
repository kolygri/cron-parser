#!/usr/bin/env python3
import sys
from typing import List, Set


class CronField:
    def __init__(self, field_str: str, min_value: int, max_value: int) -> None:
        self.field_str = field_str
        self.min_value = min_value
        self.max_value = max_value
        self.values = self.parse_cron_field()

    def parse_cron_field(self) -> List[int]:
        if not self.field_str:
            raise ValueError("Field string is empty.")

        values: Set[int] = set()
        parts = self.field_str.split(",")

        for part in parts:
            # Handle step values
            if "/" in part:
                if part.count("/") > 1:
                    raise ValueError(f"Invalid field component: {part}")
                range_part, step_part = part.split("/")
                if not step_part.isdigit() or int(step_part) <= 0:
                    raise ValueError(f"Invalid step value: {step_part}")
                step = int(step_part)
            else:
                range_part = part
                step = 1

            # Handle ranges and wildcards
            if range_part == "*":
                start = self.min_value
                end = self.max_value
            elif "-" in range_part:
                if range_part.count("-") > 1:
                    raise ValueError(f"Invalid range: {range_part}")
                start_str, end_str = range_part.split("-")
                if not start_str.isdigit() or not end_str.isdigit():
                    raise ValueError(f"Invalid range: {range_part}")
                start, end = int(start_str), int(end_str)
                if start > end:
                    raise ValueError(f"Start of range {start} is greater than end {end}.")
            elif range_part.isdigit():
                start = end = int(range_part)
            else:
                raise ValueError(f"Invalid field component: {range_part}")

            # Validate the start and end
            if not (self.min_value <= start <= self.max_value):
                raise ValueError(f"Value out of range: {start}")
            if not (self.min_value <= end <= self.max_value):
                raise ValueError(f"Value out of range: {end}")

            # Add the calculated values
            values.update(range(start, end + 1, step))

        return sorted(values)


class CronExpression:
    def __init__(self, cron_expression: str) -> None:
        self.cron_expression = cron_expression
        self.minute_field: CronField
        self.hour_field: CronField
        self.dom_field: CronField
        self.month_field: CronField
        self.dow_field: CronField
        self.command: str
        self.parse_expression()

    def parse_expression(self) -> None:
        expression = self.cron_expression.strip()
        parts = expression.split()
        if len(parts) < 6:
            raise ValueError("Invalid cron expression. Expected 5 fields and a command.")
        self.minute_field = CronField(parts[0], 0, 59)
        self.hour_field = CronField(parts[1], 0, 23)
        self.dom_field = CronField(parts[2], 1, 31)
        self.month_field = CronField(parts[3], 1, 12)
        self.dow_field = CronField(parts[4], 1, 7)
        self.command = " ".join(parts[5:])


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: cron_parser 'cron_expression'")
        sys.exit(1)

    cron_expression_str: str = sys.argv[1]
    try:
        cron_expression = CronExpression(cron_expression_str)

        # Output the results
        print("{:<14}{}".format("minute", " ".join(map(str, cron_expression.minute_field.values))))
        print("{:<14}{}".format("hour", " ".join(map(str, cron_expression.hour_field.values))))
        print("{:<14}{}".format("day of month", " ".join(map(str, cron_expression.dom_field.values))))
        print("{:<14}{}".format("month", " ".join(map(str, cron_expression.month_field.values))))
        print("{:<14}{}".format("day of week", " ".join(map(str, cron_expression.dow_field.values))))
        print("{:<14}{}".format("command", cron_expression.command))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
