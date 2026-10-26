"""Load the supplied workbook and run the project's ten SQLite analyses."""
import argparse
import csv
import json
import math
from pathlib import Path
import sqlite3
import tempfile

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
HEADERS = (
    'Ship Mode', 'Segment', 'Country', 'City', 'State', 'Postal Code',
    'Region', 'Category', 'Sub-Category', 'Sales', 'Quantity', 'Discount', 'Profit',
)
NUMERIC = {'Sales', 'Quantity', 'Discount', 'Profit'}


def read_records(path):
    book = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = book['SampleSuperstore']
        rows = iter(sheet.values)
        headers = next(rows, ())
        if tuple(headers) != HEADERS:
            raise ValueError('Workbook columns do not match the supplied extract')
        records = []
        for number, row in enumerate(rows, start=2):
            if all(value is None for value in row):
                continue
            values = dict(zip(headers, row))
            if any(value is None for value in row):
                raise ValueError(f'Row {number}: missing value')
            for field in NUMERIC:
                value = values[field]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    raise ValueError(f'Row {number}: invalid numeric {field}')
            if values['Sales'] < 0 or not 0 <= values['Discount'] <= 1:
                raise ValueError(f'Row {number}: sales or discount outside accepted range')
            if values['Quantity'] <= 0 or int(values['Quantity']) != values['Quantity']:
                raise ValueError(f'Row {number}: quantity must be a positive integer')
            records.append(tuple(row))
        if not records:
            raise ValueError('Workbook contains no sales lines')
        return records
    finally:
        book.close()


def analyze(workbook, sql_path, output):
    records = read_records(workbook)
    output.mkdir(parents=True, exist_ok=True)
    # Stage a complete run before replacing generated outputs.
    with tempfile.TemporaryDirectory(dir=output) as staging:
        staging = Path(staging)
        db = sqlite3.connect(staging / 'retail.sqlite')
        try:
            columns = ', '.join(
                '"' + h.replace(' ', '_').replace('-', '_') + '" ' +
                ('INTEGER' if h == 'Quantity' else 'REAL' if h in NUMERIC else 'TEXT')
                for h in HEADERS
            )
            db.execute(f'CREATE TABLE SampleSuperstore ({columns})')
            db.executemany('INSERT INTO SampleSuperstore VALUES (' + ','.join('?' for _ in HEADERS) + ')', records)
            db.commit()
            if db.execute('PRAGMA integrity_check').fetchone() != ('ok',):
                raise ValueError('SQLite integrity check failed')
            results = []
            statement = ''
            # sqlite3.complete_statement preserves comments and quoted semicolons.
            for line in sql_path.read_text().splitlines(keepends=True):
                statement += line
                if not sqlite3.complete_statement(statement):
                    continue
                cursor = db.execute(statement)
                if cursor.description is None:
                    raise ValueError('Expected a result-producing analysis query')
                rows = cursor.fetchall()
                if not rows:
                    raise ValueError('Analysis query returned no results')
                name = f'query-{len(results) + 1:02d}.csv'
                with (staging / name).open('w', newline='') as handle:
                    writer = csv.writer(handle)
                    writer.writerow([col[0] for col in cursor.description])
                    writer.writerows(rows)
                results.append({'file': name, 'rows': len(rows)})
                statement = ''
            if any(line.strip() and not line.lstrip().startswith('--') for line in statement.splitlines()):
                raise ValueError('SQL ends with an incomplete statement')
            if len(results) != 10:
                raise ValueError(f'Expected ten analysis queries, got {len(results)}')
            sales, profit, quantity = db.execute('SELECT ROUND(SUM(Sales), 2), ROUND(SUM(Profit), 2), SUM(Quantity) FROM SampleSuperstore').fetchone()
            summary = {'sales_lines': len(records), 'units_sold': quantity, 'sales': sales,
                       'profit': profit, 'profit_margin_pct': round(100 * profit / sales, 2) if sales else None,
                       'queries': results, 'grain': 'sales line; distinct orders and customers unavailable'}
            (staging / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        finally:
            db.close()
        for file in staging.iterdir():
            file.replace(output / file.name)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workbook', type=Path, default=ROOT / 'SampleSuperstore.csv.xlsx')
    parser.add_argument('--output', type=Path, default=ROOT / 'outputs')
    args = parser.parse_args()
    summary = analyze(args.workbook, ROOT / 'project.sql', args.output)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
