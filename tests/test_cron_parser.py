import unittest

from cron_tool.cron_parser import CronExpression, CronField


class TestCronParser(unittest.TestCase):
    def test_minute_field(self):
        self.assertEqual(CronField("*/15", 0, 59).values, [0, 15, 30, 45])
        self.assertEqual(CronField("10-20", 0, 59).values, list(range(10, 21)))
        self.assertEqual(CronField("0-30/10", 0, 59).values, [0, 10, 20, 30])
        self.assertEqual(CronField("5", 0, 59).values, [5])
        self.assertEqual(CronField("*", 0, 59).values, list(range(0, 60)))
        self.assertEqual(CronField("1,2,3", 0, 59).values, [1, 2, 3])

        # Edge cases
        self.assertEqual(CronField("0", 0, 59).values, [0])  # Lower bound
        self.assertEqual(CronField("59", 0, 59).values, [59])  # Upper bound

        # Testing full range
        self.assertEqual(CronField("0-59", 0, 59).values, list(range(0, 60)))

        # Testing multiple values at the boundaries
        self.assertEqual(CronField("0,59", 0, 59).values, [0, 59])

        # Testing mixed list of ranges and steps
        self.assertEqual(CronField("0-30/15,40-50/5", 0, 59).values, [0, 15, 30, 40, 45, 50])

        # Edge case for step that exceeds range
        self.assertEqual(CronField("0-59/60", 0, 59).values, [0])  # Only 0 within range

        # Edge case: large steps within a small range
        self.assertEqual(CronField("0-5/6", 0, 59).values, [0])  # No other number fits

        # Ensure no duplicate values (e.g., overlapping ranges)
        self.assertEqual(CronField("10-20,15-25", 0, 59).values, list(range(10, 26)))

    def test_minute_failure_inputs(self):
        # Invalid inputs
        with self.assertRaises(ValueError):
            CronField("60", 0, 59)  # Out of upper bound
        with self.assertRaises(ValueError):
            CronField("-1", 0, 59)  # Out of lower bound
        with self.assertRaises(ValueError):
            CronField("invalid", 0, 59)  # Invalid format
        with self.assertRaises(ValueError):
            CronField("*/-5", 0, 59)  # Invalid negative step
        with self.assertRaises(ValueError):
            CronField("0-10/0", 0, 59)  # Zero step
        with self.assertRaises(ValueError):
            CronField("0-10/", 0, 59)  # Missing step value
        with self.assertRaises(ValueError):
            CronField("/5", 0, 59)  # Missing range_part
        with self.assertRaises(ValueError):
            CronField("*/", 0, 59)  # Missing step value

    def test_hour_field(self):
        self.assertEqual(CronField("0", 0, 23).values, [0])
        self.assertEqual(CronField("*/6", 0, 23).values, [0, 6, 12, 18])
        self.assertEqual(CronField("1-5", 0, 23).values, [1, 2, 3, 4, 5])

        # Complex expressions
        self.assertEqual(CronField("0,12-14/2,18", 0, 23).values, [0, 12, 14, 18])

        # Upper boundary inclusion
        self.assertEqual(CronField("20-23", 0, 23).values, [20, 21, 22, 23])

        # Large step value with wildcard
        self.assertEqual(CronField("*/25", 0, 23).values, [0])

    def test_obscure_hour_ranges(self):
        # Overlapping ranges and lists
        self.assertEqual(CronField("1,3-5", 0, 23).values, [1, 3, 4, 5])

        # Duplicates in list
        self.assertEqual(CronField("2,2,2", 0, 23).values, [2])

        # Full range
        self.assertEqual(CronField("0-23", 0, 23).values, list(range(0, 24)))

    def test_hour_failure_inputs(self):
        # Range exceeding boundaries
        with self.assertRaises(ValueError):
            CronField("22-25", 0, 23)
        # Negative numbers
        with self.assertRaises(ValueError):
            CronField("-1", 0, 23)
        # Non-integer values
        with self.assertRaises(ValueError):
            CronField("two", 0, 23)
        # Empty string
        with self.assertRaises(ValueError):
            CronField("", 0, 23)
        # Invalid step zero
        with self.assertRaises(ValueError):
            CronField("*/0", 0, 23)
        # Zero step value in range
        with self.assertRaises(ValueError):
            CronField("1-5/0", 0, 23)
        # Step value larger than range
        self.assertEqual(CronField("0-5/10", 0, 23).values, [0])
        # Invalid characters
        with self.assertRaises(ValueError):
            CronField("*/$%", 0, 23)
        # Range with start greater than end
        with self.assertRaises(ValueError):
            CronField("5-1", 0, 23)
        # Missing step value
        with self.assertRaises(ValueError):
            CronField("*/", 0, 23)
        # Missing range value
        with self.assertRaises(ValueError):
            CronField("/5", 0, 23)

    def test_day_of_month_field(self):
        self.assertEqual(CronField("1,15", 1, 31).values, [1, 15])
        self.assertEqual(CronField("*", 1, 31).values, list(range(1, 32)))

    def test_month_field(self):
        self.assertEqual(CronField("*", 1, 12).values, list(range(1, 13)))
        self.assertEqual(CronField("1-5", 1, 12).values, [1, 2, 3, 4, 5])

    def test_day_of_week_field(self):
        self.assertEqual(CronField("1-5", 1, 7).values, [1, 2, 3, 4, 5])
        self.assertEqual(CronField("*", 1, 7).values, list(range(1, 8)))

    def test_cron_expression(self):
        cron_expr = CronExpression("*/15 0 1,15 * 1-5 /usr/bin/find")
        self.assertEqual(cron_expr.minute_field.values, [0, 15, 30, 45])
        self.assertEqual(cron_expr.hour_field.values, [0])
        self.assertEqual(cron_expr.dom_field.values, [1, 15])
        self.assertEqual(cron_expr.month_field.values, list(range(1, 13)))
        self.assertEqual(cron_expr.dow_field.values, [1, 2, 3, 4, 5])
        self.assertEqual(cron_expr.command, "/usr/bin/find")

    def test_cron_expression_failure(self):
        with self.assertRaises(ValueError):
            CronExpression("invalid expression")
        with self.assertRaises(ValueError):
            CronExpression("*/15 0 1,15 *")  # Missing command


if __name__ == "__main__":
    unittest.main()
