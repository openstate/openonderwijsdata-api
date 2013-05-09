import csv
from glob import glob
import json
import re

MONITOR_DIR = 'toezichtkaarten'

REGEXES = {
    # comma followed by optional whitespace
    'space_opt_comma': re.compile(r',\s?')
}

PRIMARY_SCHOOL_ADVICES_STRUCTURES = {
    'VMBO-B': {
        'blpop': 'VMBO-B',
        'blphond': 'VMBO-BK',
        'blpond': 'VMBO-K+'
    },
    'VMBO-K': {
        'klpbov': 'VMBO-B',
        'klphbov': 'VMBO-BK',
        'klpop': 'VMBO-K',
        'klphond': 'VMBO-K(G)T',
        'klpond': 'VMBO-(G)T+'},
    'VMBO-(G)T': {
        'gtpbov': 'VMBO-K-',
        'gtphbov': 'VMBO-K(G)T',
        'gtpop': 'VMBO-(G)T',
        'gtphond': 'VMBO-(G)T/HAVO',
        'gtpond': 'HAVO+'
    },
    'HAVO': {
        'hapbov': 'VMBO-(G)T-',
        'haphbov': 'VMBO-(G)T/HAVO',
        'hapbov': 'HAVO',
        'haphond': 'HAVO/VWO',
        'hapond': 'VWO'
    },
    'VWO': {
        'vwpbov': 'HAVO-',
        'vwphbov': 'HAVO/VWO',
        'vwpop': 'VWO'
    }
}

REACHED_THIRD_YEAR = {
    'VMBO-B': 'bl1e3e',
    'VMBO-K': 'kl1e3e',
    'VMBO-(G)T': 'gt1e3e',
    'HAVO': 'ha1e3e',
    'VWO': 'vw1e3e'
}

STRAIGHT_TO_GRADUATION = {
    'VMBO-B': {'percentage': 'BaOnv', 'indicator': 'BAonvbol'},
    'VMBO-K': {'percentage': 'KaOnv', 'indicator': 'KAonvbol'},
    'VMBO-(G)T': {'percentage': 'GtOnv', 'indicator': 'GTonvbol'},
    'HAVO': {'percentage': 'HaOnv', 'indicator': 'HAonvbol'},
    'VWO': {'percentage': 'VwOnv', 'indicator': 'VWonvbol'}
}

GRADES = {
    'VMBO-B': {
        'BAtotcec': {'name': 'Alle vakken', 'indicator': 'BAtotbol'},
        'BAnedcec': {'name': 'Nederlands', 'indicator': 'BAnedbol'},
        'BAmvtcec': {'name': 'Engels, Frans, Duits', 'indicator': 'BAmvtbol'},
        'BAzaacec': {'name': 'Aardrijkskunde, Geschiedenis', 'indicator': 'BAzaabol'},
        'BAecocec': {'name': 'Economische vakken', 'indicator': 'BAecobol'},
        'BAexacec': {'name': 'Wiskunde, Natuurkunde, Scheikunde', 'indicator': 'BAexbol'}
    },
    'VMBO-K': {
        'KAtotcec': {'name': 'Alle vakken', 'indicator': 'KAtotbol'},
        'KAnedcec': {'name': 'Nederlands', 'indicator': 'KAnedbol'},
        'KAmvtcec': {'name': 'Engels, Frans, Duits', 'indicator': 'KAmvtbol'},
        'KAzaacec': {'name': 'Aardrijkskunde, Geschiedenis', 'indicator': 'KAzaabol'},
        'KAecocec': {'name': 'Economische vakken', 'indicator': 'KAecobol'},
        'KAexacec': {'name': 'Wiskunde, Natuurkunde, Scheikunde', 'indicator': 'KAexbol'}
    },
    'VMBO-(G)T': {
        'GTtotcec': {'name': 'Alle vakken', 'indicator': 'GTtotbol'},
        'GTnedcec': {'name': 'Nederlands', 'indicator': 'GTnedbol'},
        'GTmvtcec': {'name': 'Engels, Frans, Duits', 'indicator': 'GTmvtbol'},
        'GTzaacec': {'name': 'Aardrijkskunde, Geschiedenis', 'indicator': 'GTzaabol'},
        'GTecocec': {'name': 'Economische vakken', 'indicator': 'GTecobol'},
        'GTexacec': {'name': 'Wiskunde, Natuurkunde, Scheikunde', 'indicator': 'GTexbol'}
    },
    'HAVO': {
        'HAtotcec': {'name': 'Alle vakken', 'indicator': 'HAtotbol'},
        'HAnedcec': {'name': 'Nederlands', 'indicator': 'HAnedbol'},
        'HAmvtcec': {'name': 'Engels, Frans, Duits', 'indicator': 'HAmvtbol'},
        'HAzaacec': {'name': 'Aardrijkskunde, Geschiedenis', 'indicator': 'HAzaabol'},
        'HAecocec': {'name': 'Economische vakken', 'indicator': 'HAecobol'},
        'HAexacec': {'name': 'Wiskunde, Natuurkunde, Scheikunde', 'indicator': 'HAexbol'}
    },
    'VWO': {
        'VWtotcec': {'name': 'Alle vakken', 'indicator': 'VWtotbol'},
        'VWnedcec': {'name': 'Nederlands', 'indicator': 'VWnedbol'},
        'VWmvtcec': {'name': 'Engels, Frans, Duits', 'indicator': 'VWmvtbol'},
        'VWzaacec': {'name': 'Aardrijkskunde, Geschiedenis', 'indicator': 'VWzaabol'},
        'VWecocec': {'name': 'Economische vakken', 'indicator': 'VWecobol'},
        'VWexacec': {'name': 'Wiskunde, Natuurkunde, Scheikunde', 'indicator': 'VWexbol'},
        'VWklacec': {'name': 'Latijn, Grieks', 'indicator': 'VWklabol'}
    },
}


def get_school_composition(school):
    """
    Returns the composition of education_structures in the first year. A
    student can follow categorical education (only follow courses in a single
    education structure) or combined (Dutch on HAVO level, French on VMBO level)
    """
    composition = {}
    categorical_perc = school['perccat1'].strip()
    combined_perc = school['percsam1'].strip()
    categorical_structs = school['klcomb1a'].strip()
    combined_categories = school['klcomb1g'].strip()

    if categorical_perc:
        categorical_perc = int(categorical_perc) / 100.0
        composition['percentage_student_categorical_education'] = categorical_perc

    if combined_perc:
        combined_perc = int(combined_perc) / 100.0
        composition['percentage_student_combined_education'] = combined_perc

    if categorical_structs:
        if categorical_perc > 0:
            categorical_structs = re.split(REGEXES['space_opt_comma'],
                                           categorical_structs)
        else:
            categorical_structs = []
        composition['categorical_education_structures'] = categorical_structs

    if combined_categories:
        if combined_perc > 0:
            combined_categories = re.split(REGEXES['space_opt_comma'],
                                           combined_categories)
        else:
            combined_categories = []
        composition['combined_education_structures'] = combined_categories

    return composition


def get_first_years_performance(school):
    """
    Returns performance indicator for this school, as well as an indicator
    (1-5; 3 is average, 1 is worse, 5 is better) that compares the school to
    the national average.
    """
    performance = {}
    ratio = school['renondb'].strip()
    # bolletje
    compared_performance = school['renonbol'].strip()

    if ratio:
        ratio = float(ratio.replace(',', '.'))
        performance['ratio'] = ratio

    if compared_performance:
        performance['compared_performance'] = int(compared_performance)
        performance['compared_performance_category'] = school['renoncat'].strip()

    return performance


def get_advice_structure(school):
    """
    Returns the distribution of primary school advices for all the education
    structures the school provides.
    """
    structures = []

    for struct, advices in PRIMARY_SCHOOL_ADVICES_STRUCTURES.iteritems():
        structure = {'education_structure': struct, 'primary_school_advices': []}
        for advice, adv_name in advices.iteritems():
            dist = school[advice].strip()
            if dist:
                structure['primary_school_advices'].append({
                    'advice': adv_name,
                    'percentage_of_students': int(dist) / 100.0
                })
        if structure['primary_school_advices']:
            structures.append(structure)

    return structures


def get_students_without_retaking(school):
    """
    Returns the percentage of students that reach their third year, without
    retaking a year, per education structure.
    """
    structures = []
    for struct, key in REACHED_THIRD_YEAR.iteritems():
        percentage = school[key].strip()
        if percentage:
            percentage = int(percentage) / 100.0
            structures.append({
                'education_structure': struct,
                'percentage': percentage
            })

    if structures:
        return structures


def get_straight_to_graduation(school):
    """
    Returns the percentage of students that graduate without retaking a year
    between the third year and graduation, as well as an indicator (1-5; 3 is
    average, 1 is worse, 5 is better) that compares these numbers to the
    national average.
    """
    graduations = []

    for structure, fields in STRAIGHT_TO_GRADUATION.iteritems():
        perc = school[fields['percentage']].strip()
        if perc:
            perc = float(perc.replace(',', '.')) / 100.0
            indicator = int(school[fields['indicator']].strip())
            graduations.append({
                'education_structure': structure,
                'percentage': perc,
                'compared_graduation': indicator
            })

    if graduations:
        return graduations


def get_grades(school):
    """
    Returns average grades per school and per course(group), as well as an
    indicator (1-5; 3 is average, 1 is worse, 5 is better) that compares these
    to the national average.
    """
    grades = []

    return grades


def process(item):
    """
    Processes a school by calling different functions that format different
    subsets of the required data.
    """
    schools = {}
    reader = csv.DictReader(item, delimiter=';')

    for row in reader:
        branch_id = row['brin'] + '-' + row['vestnr']
        if branch_id not in schools:
            school = {}
            # school['composition_first_year'] = get_school_composition(row)
            # school['first_years_performance'] = get_first_years_performance(row)
            # school['advice_structure_third_year'] = get_advice_structure(row)

            # retaking = get_students_without_retaking(row)
            # if retaking:
            #     school['percentage_students_third_year_without_retaking'] = \
            #         retaking

            # straight_to_graduation = get_straight_to_graduation(row)
            # if straight_to_graduation:
            #     school['percentage_student_3_year_to_graduation'] = \
            #         straight_to_graduation

            school['grades'] = get_grades(row)
        else:
            # If this happens, we have multiple entries in a single file for
            # the same brin + branch combination; that is bad
            pass

        print json.dumps(school, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    for item in glob('%s/*.csv' % MONITOR_DIR):
        with open(item, 'r') as csvfile:
            process(csvfile)
