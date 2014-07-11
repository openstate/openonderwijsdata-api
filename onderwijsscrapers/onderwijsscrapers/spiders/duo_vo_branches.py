class DuoVoBranchesSpider(BaseSpider):
    name = 'duo_vo_branches'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/adressen/Adressen/vestigingen.asp',
                    self.parse_branches),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen2.asp',
                    self.parse_student_residences),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp',
                     self.parse_students_per_branch),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp',
                    self.student_graduations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen7.asp',
                    self.student_exam_grades),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp',
                    self.vmbo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp',
                    self.havo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp',
                    self.vwo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen3.asp',
                    self.parse_vavo_students),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen5.asp',
                    self.parse_students_by_finegrained_structure),
        ]

    def parse_branches(row):
        """
        Parse "02. Adressen alle vestigingen"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                school = DuoVoBranch()

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']
                school['name'] = row['VESTIGINGSNAAM'].strip()
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'].strip(),
                                         row['HUISNUMMER-TOEVOEGING'].strip()),
                    'city': row['PLAATSNAAM'].strip(),
                    'zip_code': row['POSTCODE'].strip().replace(' ', '')
                }

                school['website'] = row['INTERNETADRES'].strip() or None

                school['denomination'] = row['DENOMINATIE'].strip() or None

                if row['ONDERWIJSSTRUCTUUR'].strip():
                    school['education_structures'] = row['ONDERWIJSSTRUCTUUR']\
                        .strip().split('/')
                else:
                    school['education_structures'] = None

                school['province'] = row['PROVINCIE'].strip() or None

                school['board_id'] = int_or_none(row['BEVOEGD GEZAG NUMMER'].strip())

                if row['BRIN NUMMER'].strip():
                    school['brin'] = row['BRIN NUMMER'].strip()

                if row['VESTIGINGSNUMMER'].strip():
                    school['branch_id'] = int(row['VESTIGINGSNUMMER']
                                              .strip()
                                              .replace(row['BRIN NUMMER'], ''))

                school['municipality'] = row['GEMEENTENAAM'].strip() or None

                school['municipality_code'] = int_or_none(row['GEMEENTENUMMER'].strip())

                school['phone'] = row['TELEFOONNUMMER'].strip() or None

                school['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'].strip(),
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'].strip())
                else:
                    school['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].strip().replace(' ', '')
                else:
                    school['correspondence_address']['zip_code'] = None

                school['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'].strip() or None

                school['nodal_area'] = row['NODAAL GEBIED NAAM'].strip() or None

                school['nodal_area_code'] = int_or_none(row['NODAAL GEBIED CODE']
                                                    .strip())

                school['rpa_area'] = row['RPA-GEBIED NAAM'].strip() or None

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'].strip())

                school['wgr_area'] = row['WGR-GEBIED NAAM'].strip() or None

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'].strip())

                school['corop_area'] = row['COROPGEBIED NAAM'].strip() or None

                school['corop_area_code'] = int_or_none(row['COROPGEBIED CODE'].strip())

                school['education_area'] = row['ONDERWIJSGEBIED NAAM'].strip() or None

                if row['ONDERWIJSGEBIED CODE'].strip():
                    school['education_area_code'] = int(row['ONDERWIJSGEBIED '
                                                            'CODE'].strip())
                else:
                    school['education_area_code'] = None

                school['rmc_region'] = row['RMC-REGIO NAAM'].strip() or None

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'].strip())

                yield school

    def parse_students_per_branch(row):
        """
        Parse "01. Leerlingen per vestiging naar onderwijstype, lwoo
        indicatie, sector, afdeling, opleiding"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            student_educations = {}
            school_ids = {}

            for row in parse_csv_file(csv_url):
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                                       row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER']
                                     .strip().replace(row['BRIN NUMMER'], ''))
                }

                if school_id not in student_educations:
                    student_educations[school_id] = []

                education_type = {}

                department = row['AFDELING'].strip()
                if department:
                    education_type['department'] = department
                    if education_type['department'].lower() == 'n.v.t.':
                        education_type['department'] = None
                else:
                    education_type['department'] = None

                if row['ELEMENTCODE'].strip():
                    education_type['elementcode'] = int(row['ELEMENTCODE']
                                                        .strip())
                else:
                    education_type['elementcode'] = None

                lwoo = row['LWOO INDICATIE'].strip().lower()
                if lwoo:
                    if lwoo == 'j':
                        education_type['lwoo'] = True
                    elif lwoo == 'n':
                        education_type['lwoo'] = False
                    else:
                        education_type['lwoo'] = None
                else:
                    education_type['lwoo'] = None

                vmbo_sector = row['VMBO SECTOR'].strip()
                if vmbo_sector:
                    if vmbo_sector.lower() == 'n.v.t.':
                        education_type['vmbo_sector'] = None
                    else:
                        education_type['vmbo_sector'] = vmbo_sector
                else:
                    education_type['vmbo_sector'] = None

                naam = row['OPLEIDINGSNAAM'].strip()
                education_type['education_name'] = naam or None

                otype = row['ONDERWIJSTYPE VO EN LEER- OF VERBLIJFSJAAR'].strip()
                education_type['education_structure'] = otype or None

                for available_year in range(1, 7):
                    male = int(row['LEER- OF VERBLIJFSJAAR %s - MAN'
                               % available_year])
                    female = int(row['LEER- OF VERBLIJFSJAAR %s - VROUW'
                                 % available_year])

                    education_type['year_%s' % available_year] = {
                        'male': male,
                        'female': female,
                        'total': male + female
                    }

                student_educations[school_id].append(education_type)

            for school_id, s_by_structure in student_educations.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_structure_url=csv_url,
                    students_by_structure_reference_date=reference_date,
                    students_by_structure=s_by_structure
                )

                yield school

    def parse_student_residences(row):
        """
        Parse "02. Leerlingen per vestiging naar postcode leerling en
        leerjaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            student_residences = {}
            school_ids = {}
            for row in parse_csv_file(csv_url):
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                                       row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER'].strip()
                                     .replace(row['BRIN NUMMER'], ''))
                }

                if school_id not in student_residences:
                    student_residences[school_id] = []

                student_residences[school_id].append({
                    'zip_code': row['POSTCODE LEERLING'].strip(),
                    'city': row['PLAATSNAAM LEERLING'].strip().capitalize(),
                    'municipality': row['GEMEENTENAAM LEERLING'].strip(),
                    'municipality_id': int(row['GEMEENTENUMMER LEERLING'].strip()),
                    'year_1': int(row['LEER- OF VERBLIJFSJAAR 1']),
                    'year_2': int(row['LEER- OF VERBLIJFSJAAR 2']),
                    'year_3': int(row['LEER- OF VERBLIJFSJAAR 3']),
                    'year_4': int(row['LEER- OF VERBLIJFSJAAR 4']),
                    'year_5': int(row['LEER- OF VERBLIJFSJAAR 5']),
                    'year_6': int(row['LEER- OF VERBLIJFSJAAR 6'])
                })

            for school_id, residence in student_residences.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    student_residences_url=csv_url,
                    student_residences_reference_date=reference_date,
                    student_residences=residence
                )

                yield school

    def student_graduations(row):
        """
        Parse "06. Examenkandidaten en geslaagden"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            graduations_school_year = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    row[key.replace('\n', '')] = row[key].strip()
                    del row[key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'].replace(brin, ''))
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                if school_id not in graduations_school_year:
                    graduations_school_year[school_id] = {}

                # The years present in the CVS file (keys) and the
                # normalized form we will use (values)
                years = {
                    'SCHOOLJAAR 2007-2008': '2007-2008',
                    'SCHOOLJAAR 2008-2009': '2008-2009',
                    'SCHOOLJAAR 2009-2010': '2009-2010',
                    'SCHOOLJAAR 2010-2011': '2010-2011',
                    'SCHOOLJAAR 2011-2012': '2011-2012',
                }

                # Available breakdowns and their normalized form
                breakdown = {
                    'MAN': 'male',
                    'VROUW': 'female',
                    'ONBEKEND': 'unknown'
                }

                for year, y_normal in years.iteritems():
                    if y_normal not in graduations_school_year[school_id]:
                        # Graduation info of a single school year
                        graduations_school_year[school_id][y_normal] = {
                            'year': y_normal,
                            'failed': 0,
                            'passed': 0,
                            'candidates': 0,
                            'per_department': []
                        }

                    # Total number of candidates (not always present for
                    # every year)
                    try:
                        candidates = row['EXAMENKANDIDATEN %s TOTAAL' % year]
                        if candidates:
                            candidates = int(candidates)
                        else:
                            continue
                    except KeyError:
                        candidates = 0
                    graduations_school_year[school_id][y_normal]['candidates'] += candidates

                    # Total number of successful graduations
                    try:
                        passed = int(row['GESLAAGDEN %s TOTAAL' % year])
                    except KeyError:
                        passed = 0
                    graduations_school_year[school_id][y_normal]['passed'] += passed

                    graduations_school_year[school_id][y_normal]['failed'] += (candidates - passed)

                    # Graduations for a singel department, by gender
                    department = {
                        'education_structure': row['ONDERWIJSTYPE VO'],
                        'department': row['OPLEIDINGSNAAM'],
                        'inspectioncode': row['INSPECTIECODE'],
                        'passed': {},
                        'failed': {},
                        'candidates': {},
                    }

                    for gender, gender_normal in breakdown.iteritems():
                        try:
                            candidates = row['EXAMENKANDIDATEN %s %s' % (year,
                                             gender)]
                        except KeyError:
                            continue

                        # Skip gender if no value
                        if not candidates:
                            continue

                        candidates = int(candidates)
                        department['candidates'][gender_normal] = candidates

                        try:
                            passed = int(row['GESLAAGDEN %s %s' % (year, gender)])
                        except KeyError:
                            continue
                        department['passed'][gender_normal] = passed

                        failed = candidates - passed
                        department['failed'][gender_normal] = failed

                    graduations_school_year[school_id][y_normal]['per_department'].append(department)

            for school_id, graduations in graduations_school_year.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    graduations_reference_url=csv_url,
                    graduations_reference_date=reference_date,
                    graduations=[graduations[year] for year in graduations]
                )

                yield school

    def student_exam_grades(row):
        """
        Parse "07. Geslaagden, gezakten en gemiddelde examencijfers per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            grades_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'].replace(brin, ''))
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO']
                }

                if 'LEERWEG VMBO' in row:
                    grades['education_structure'] += '-%s' % row['LEERWEG VMBO']

                if 'VMBO SECTOR' in row:
                    grades['vmbo_sector'] = row['VMBO SECTOR']

                if 'AFDELING' in row:
                    grades['sector'] = row['AFDELING']

                if 'EXAMENKANDIDATEN' in row:
                    grades['candidates'] = int(row['EXAMENKANDIDATEN'])

                if 'GESLAAGDEN' in row:
                    grades['passed'] = int(row['GESLAAGDEN'])

                if 'GEZAKTEN' in row:
                    grades['failed'] = int(row['GEZAKTEN'])

                if 'GEMIDDELD CIJFER SCHOOLEXAMEN' in row:
                    grades['avg_grade_school_exam'] = float(row[
                        'GEMIDDELD CIJFER SCHOOLEXAMEN'].replace(',', '.'))

                if 'GEMIDDELD CIJFER CENTRAAL EXAMEN' in row:
                    grades['avg_grade_central_exam'] = float(row[
                        'GEMIDDELD CIJFER CENTRAAL EXAMEN'].replace(',', '.'))

                if 'GEMIDDELD CIJFER CIJFERLIJST' in row:
                    grades['avg_final_grade'] = float(row[
                        'GEMIDDELD CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in grades_per_school:
                    grades_per_school[school_id] = []

                grades_per_school[school_id].append(grades)

            for school_id, grades in grades_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    exam_grades_reference_url=csv_url,
                    exam_grades_reference_date=reference_date,
                    exam_grades=grades
                )

                yield school

    def vmbo_exam_grades_per_course(row):
        """
        Parse "08. Examenkandidaten vmbo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': '%s-%s' % (row['ONDERWIJSTYPE VO'],
                                                      row['LEERWEG']),
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']

                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vmbo_exam_grades_reference_url=csv_url,
                    vmbo_exam_grades_reference_date=reference_date,
                    vmbo_exam_grades_per_course=grades
                )

                yield school

    def havo_exam_grades_per_course(row):
        """
        Parse "09. Examenkandidaten havo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO'],
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']

                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    havo_exam_grades_reference_url=csv_url,
                    havo_exam_grades_reference_date=reference_date,
                    havo_exam_grades_per_course=grades
                )

                yield school

    def vwo_exam_grades_per_course(row):
        """
        Parse "10. Examenkandidaten vwo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO'],
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']
                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vwo_exam_grades_reference_url=csv_url,
                    vwo_exam_grades_reference_date=reference_date,
                    vwo_exam_grades_per_course=grades
                )
                yield school

    def parse_vavo_students(row):
        """
        Voortgezet onderwijs > Leerlingen
        Parse "Leerlingen per vestiging en bevoegd gezag (vavo apart)"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            vavo_students_per_school = {}

            for row in parse_csv_file(csv_url):

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'].strip()[-2:] or 0)
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                vavo_students = {
                    'non_vavo' : int(row['AANTAL LEERLINGEN'] or 0),
                    'vavo' : int(row['AANTAL VO LEERLINGEN UITBESTEED AAN VAVO'] or 0),
                }

                if school_id not in vavo_students_per_school:
                    vavo_students_per_school[school_id] = []
                vavo_students_per_school[school_id].append(vavo_students)

            for school_id, per_school in vavo_students_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vavo_students_reference_url=csv_url,
                    vavo_students_reference_date=reference_date,
                    vavo_students=per_school
                )
                yield school

    def parse_students_by_finegrained_structure(row):
        """
        Voortgezet onderwijs > Leerlingen
        Parse "05. Leerlingen per samenwerkingsverband en onderwijstype"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            counts_per_school = {}

            for row in parse_csv_file(csv_url):

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'].strip()[-2:] or 0)
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                if school_id not in counts_per_school:
                    counts_per_school[school_id] = []

                # Don't make special fiends, just use all of 'em
                fields = [
                    'Brugjaar 1-2',
                    'Engelse Stroom',
                    'HAVO lj 4-5',
                    'HAVO uitbest. aan VAVO',
                    'HAVO/VWO lj 3',
                    'Int. Baccelaureaat',
                    'Praktijkonderwijs alle vj',
                    'VMBO BL lj 3-4',
                    'VMBO GL lj 3-4',
                    'VMBO KL lj 3-4',
                    'VMBO TL lj 3-4',
                    'VMBO uitbest. aan VAVO',
                    'VMBO-MBO2 lj 3-6',
                    'VWO lj 4-6',
                    'VWO uitbest. aan VAVO',
                ]
                for field, count in row.items():
                    if field.strip() in fields and count:
                        counts = {'type': field.strip(), 'count': int(count)}
                        counts_per_school[school_id].append(counts)

            for school_id, per_school in counts_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_finegrained_structure_reference_url=csv_url,
                    students_by_finegrained_structure_reference_date=reference_date,
                    students_by_finegrained_structure=per_school
                )
                yield school

