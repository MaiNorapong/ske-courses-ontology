#!/usr/bin/python3
import csv

from writer.base import get_subject_name

template = """
    <!-- http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{} -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{}">
        <rdf:type rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#Subject"/>
{}
{}
        <semesterAllowed rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</semesterAllowed>
        <yearAllowed rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</yearAllowed>
        <rdfs:comment xml:lang="en">{}</rdfs:comment>
        <rdfs:comment xml:lang="th">{}</rdfs:comment>
        <rdfs:label xml:lang="en">{}</rdfs:label>
        <rdfs:label xml:lang="th">{}</rdfs:label>
    </owl:NamedIndividual>
    

"""

prereq = '        <hasPrerequisite rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{}"/>'
none_prereq = '        <hasPrerequisite rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#None"/>'
must_register_with = '        <mustRegisterWith rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#{}"/>'
none_must = '        <mustRegisterWith rdf:resource="http://www.semanticweb.org/user/ontologies/2020/SKE-courses#None"/>'


def main(infile: str, outfile: str):
    with open(infile, 'r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)

        all_indivs = []
        for row in data:
            indv_name = get_subject_name(row['id'])
            pres = [p.strip() for p in row['prerequisites'].split(',') if p]
            if pres:
                prereqs = '\n'.join(prereq.format(get_subject_name(sub)) for sub in pres)
            else:
                prereqs = none_prereq
            coregs = [p.strip() for p in row['coregister'].split(',') if p]
            if coregs:
                musts = '\n'.join(must_register_with.format(get_subject_name(sub)) for sub in coregs)
            else:
                musts = none_must
            sem_allow = row['semester']
            year_allow = row['year_start']
            en_desc = row['description_en']
            th_desc = row['description_th']
            en_label = row['name_en']
            th_label = row['name_th']
            individual = template.format(indv_name, indv_name, prereqs, musts, sem_allow, year_allow, en_desc, th_desc, en_label, th_label)
            all_indivs.append(individual)

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_indivs))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Write SKE course Ontology Subject individuals')
    parser.add_argument('infile', type=str, help='the csv file to read from')
    parser.add_argument('outfile', type=str, help='the output file')
    args = parser.parse_args()
    main(args.infile, args.outfile)
