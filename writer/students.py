#!/usr/bin/python3
import csv

template = ''


def main(infile: str, outfile: str):
    with open(infile, 'r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)

        all_indivs = []
        for row in data:
            pass

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_indivs))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Write SKE course Ontology Student individuals')
    parser.add_argument('infile', type=str, help='the csv file to read from')
    parser.add_argument('outfile', type=str, help='the output file')
    args = parser.parse_args()
    main(args.infile, args.outfile)
