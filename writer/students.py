#!/usr/bin/python3
import csv

from writer.base import get_student_name

template = """
    <!-- http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{} -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{}">
        <rdf:type rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#Student"/>
        <academicYearEnrolled rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</academicYearEnrolled>
    </owl:NamedIndividual>
    


"""


def main(infile: str, outfile: str):
    with open(infile, 'r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)

        all_indivs = []
        for row in data:
            student_name = get_student_name(row['student_id'])
            individual = template.format(
                student_name,
                student_name,
                row['academic_year_enrolled']
            )
            all_indivs.append(individual)

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_indivs))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Write SKE course Ontology Student individuals')
    parser.add_argument('infile', type=str, help='the csv file to read from')
    parser.add_argument('outfile', type=str, help='the output file')
    args = parser.parse_args()
    main(args.infile, args.outfile)
