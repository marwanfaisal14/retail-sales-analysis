"""Check data rejection and financial reconciliation against the supplied extract."""
import csv
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from openpyxl import Workbook

from analyze import HEADERS, ROOT, analyze, read_records


class RetailAnalysisTests(unittest.TestCase):
    def test_complete_analysis_and_repeatability(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            first = analyze(ROOT / 'SampleSuperstore.csv.xlsx', ROOT / 'project.sql', output)
            second = analyze(ROOT / 'SampleSuperstore.csv.xlsx', ROOT / 'project.sql', output)
            self.assertEqual(first, second)
            self.assertEqual(second['sales_lines'], 9994)
            self.assertEqual(second['units_sold'], 37873)
            self.assertEqual(second['sales'], 2297200.86)
            self.assertEqual(second['profit'], 286397.02)
            self.assertEqual(second['profit_margin_pct'], 12.47)
            self.assertEqual(len(second['queries']), 10)
            self.assertEqual(second['queries'][4]['rows'], 10)
            self.assertEqual(second['queries'][5]['rows'], 10)
            self.assertEqual(json.loads((output / 'summary.json').read_text()), second)
            with (output / 'query-07.csv').open() as handle:
                segments = list(csv.DictReader(handle))
            self.assertEqual(sum(int(row['Sales_Lines']) for row in segments), 9994)
            self.assertEqual(sum(int(row['Units_Sold']) for row in segments), 37873)
            self.assertAlmostEqual(sum(float(row['Total_Profit']) for row in segments), 286397.02, places=2)
            with (output / 'query-10.csv').open() as handle:
                regions = list(csv.DictReader(handle))
            self.assertAlmostEqual(sum(float(row['Sales_Share_Pct']) for row in regions), 100, delta=0.02)
            self.assertEqual(regions[0]['Region'], 'West')
            db = sqlite3.connect(output / 'retail.sqlite')
            try:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM SampleSuperstore').fetchone()[0], 9994)
            finally:
                db.close()

    def invalid_workbook(self, field=None, value=None, headers=HEADERS):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'invalid.xlsx'
            book = Workbook()
            sheet = book.active
            sheet.title = 'SampleSuperstore'
            sheet.append(headers)
            row = ['Second Class', 'Consumer', 'United States', 'City', 'State', '12345',
                   'West', 'Furniture', 'Chairs', 100, 2, 0.2, 15]
            if field:
                row[HEADERS.index(field)] = value
            sheet.append(row)
            book.save(path)
            book.close()
            with self.assertRaises(ValueError):
                read_records(path)

    def test_rejects_missing_or_misordered_columns(self):
        self.invalid_workbook(headers=tuple(reversed(HEADERS)))

    def test_rejects_discount_outside_range(self):
        self.invalid_workbook('Discount', 1.2)

    def test_rejects_missing_numeric_value(self):
        self.invalid_workbook('Profit', None)

    def test_rejects_non_numeric_sales(self):
        self.invalid_workbook('Sales', '100 dollars')

    def test_rejects_fractional_quantity(self):
        self.invalid_workbook('Quantity', 1.5)


if __name__ == '__main__':
    unittest.main()
