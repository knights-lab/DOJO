#!/usr/bin/env python
import click
import csv

from dojo.taxonomy import NCBITree


@click.command()
@click.option('-i', '--input', type=click.File('r'))
@click.option('-o', '--output', type=click.File('w'), default='-')
def add_green_genes_tax_to_gb_accession(input, output):
    # Load the taxonomy
    nt = NCBITree()

    # Skip header
    next(input)

    output_csv = csv.writer(output, delimiter="\t")
    # Write header
    output_csv.writerow(["gb_accession", "taxid", "green_genes_taxonomy"])
    csv_input = csv.reader(input, delimiter="\t")
    for row in csv_input:
        out_row = row + [0]
        taxid = int(row[1])
        out_row[2] = nt.green_genes_lineage(taxid, depth=8, depth_force=True)
        output_csv.writerow(out_row)


if __name__ == '__main__':
    add_green_genes_tax_to_gb_accession()
