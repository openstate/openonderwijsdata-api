from onderwijsscrapers.items import DuoPoBranch
from duo import DuoSpider, int_or_none, find_available_csvs, parse_csv_file, extract_csv_files, parse_csv_file
from scrapy.conf import settings

class DuoPoBranchesSpider(DuoSpider):
    name = 'duo_po_branches'

    def __init__(self):
        self.requests = {
            'po/adressen/Adressen/vest_bo.asp':
                self.parse_po_branches,
            'po/Leerlingen/Leerlingen/po_leerlingen1.asp':
                self.parse_po_student_weight,
            'po/Leerlingen/Leerlingen/po_leerlingen3.asp':
                self.parse_po_student_age,
            'po/Leerlingen/Leerlingen/po_leerlingen9.asp':
                self.parse_po_born_outside_nl,
            'po/Leerlingen/Leerlingen/po_leerlingen11.asp':
                self.parse_po_pupil_zipcode_by_age,
            'po/Leerlingen/Leerlingen/leerjaar.asp':
                self.parse_po_student_year,
            'po/Leerlingen/Leerlingen/po_leerlingen5.asp':
                self.parse_spo_students_by_birthyear,
            'po/Leerlingen/Leerlingen/po_leerlingen6.asp':
                self.parse_spo_students_by_edu_type,
            'po/Leerlingen/Leerlingen/Schooladvies.asp':
                self.parse_po_students_by_advice,
        }

    def parse_po_branches(self, response):
        """
        Primair onderwijs > Adressen
        Parse "03. Alle vestigingen basisonderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                school = DuoPoBranch()

                # Correct this field name which has a trailing space.
                if row.has_key('VESTIGINGSNAAM '):
                    row['VESTIGINGSNAAM'] = row['VESTIGINGSNAAM ']

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

                if row['NODAAL GEBIED CODE'].strip():
                    school['nodal_area_code'] = int(row['NODAAL GEBIED CODE']
                                                    .strip())
                else:
                    school['nodal_area_code'] = None

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

    def parse_po_student_weight(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "01. Leerlingen basisonderwijs naar leerlinggewicht en per
                   vestiging het schoolgewicht en impulsgebied"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            weights_per_school = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEWICHT0.00'):
                    row['GEWICHT 0'] = row['GEWICHT0.00']
                if row.has_key('GEWICHT0.30'):
                    row['GEWICHT 0.3'] = row['GEWICHT0.30']
                if row.has_key('GEWICHT1.20'):
                    row['GEWICHT 1.2'] = row['GEWICHT1.20']

                brin = row['BRIN NUMMER'].strip()
                # Bypasses error coming from the 2011 dataset which contains and
                # empty row.
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                weights = {}
            
                weights['student_weight_0.0'] = int_or_none(row['GEWICHT 0'].strip())        

                weights['student_weight_0.3'] = int_or_none(row['GEWICHT 0.3'].strip())

                weights['student_weight_1.2'] = int_or_none(row['GEWICHT 1.2'].strip())

                weights['school_weight'] = int_or_none(row['SCHOOLGEWICHT'].strip())

                # The 2008 dataset doesn't contain the IMPULSGEBIED field.
                if row.has_key('IMPULSGEBIED'):
                    if row['IMPULSGEBIED'].strip():
                        weights['impulse_area'] = bool(int(row['IMPULSGEBIED'].strip()))
                    else:
                        weights['impulse_area'] = None

                if school_id not in weights_per_school:
                    weights_per_school[school_id] = []

                weights_per_school[school_id].append(weights)

            for school_id, w_per_school in weights_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    weights_per_school_reference_url=csv_url,
                    weights_per_school_reference_date=reference_date,
                    weights_per_school=w_per_school
                )
                yield school

    def parse_po_student_age(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "02. Leerlingen basisonderwijs naar leeftijd"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            ages_per_branch_by_student_weight = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEMEENTE NUMMER'):
                    row['GEMEENTENUMMER'] = row['GEMEENTE NUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # The 2012 dataset had fields like 'LEEFTIJD 4 JAAR' instead of
                # '4 JAAR'. This fixes the problem.
                for key in row.keys():
                    key_norm = key.replace('LEEFTIJD ', '')
                    row[key_norm] = row[key]

                # Remove leading/trailing spaces from field names.
                for key in row.keys():
                    row[key.strip()] = row[key]

                ages = {}
                possible_ages = '3 4 5 6 7 8 9 10 11 12 13 14'.split()
                for age in possible_ages:
                    if row.has_key('%s JAAR' % age):
                        if row['%s JAAR' % age].strip():
                            ages['age_%s' % age] = int(row['%s JAAR' % age])
                        else:
                            ages['age_%s' % age] = 0
                    # The 2011 dataset uses other field names.
                    elif row.has_key('LEEFTIJD.%s' % age):
                        if row['LEEFTIJD.%s' % age].strip():
                            ages['age_%s' % age] = int(row['LEEFTIJD.%s' % age])
                        else:
                            ages['age_%s' % age] = 0

                if school_id not in ages_per_branch_by_student_weight:
                    ages_per_branch_by_student_weight[school_id] = {}

                if row['GEWICHT'].strip():
                    weight = 'student_weight_%.1f' % float(row['GEWICHT'].strip().replace(',', '.'))
                else:
                    weight = None

                ages_per_branch_by_student_weight[school_id][weight] = ages

            for school_id, a_per_school in ages_per_branch_by_student_weight.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    ages_per_branch_by_student_weight_reference_url=csv_url,
                    ages_per_branch_by_student_weight_reference_date=reference_date,
                    ages_per_branch_by_student_weight=a_per_school
                )
                yield school

    def parse_po_born_outside_nl(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "09. Leerlingen basisonderwijs met een niet-Nederlandse achtergrond naar geboorteland"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            students_by_origin = {}

            for row in parse_csv_file(csv_url):
                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # Remove leading/trailing spaces from field names and values.
                for key in row.keys():
                    row[key.strip()] = row[key].strip()

                origins = []
                for origin, country in settings['ORIGINS'].iteritems():
                    orig = {'country': country}
                    if row[origin].strip():
                        orig['students'] = int(row[origin].strip())
                    else:
                        orig['students'] = 0

                    origins.append(orig)

                if school_id not in students_by_origin:
                    students_by_origin[school_id] = origins

            for school_id, origs in students_by_origin.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_origin_reference_url=csv_url,
                    students_by_origin_reference_date=reference_date,
                    students_by_origin=origs
                )
                yield school

    def parse_po_pupil_zipcode_by_age(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd"
        """

        # For some reason, DUO decided to create a seperate file for each
        # municipality, zip them and only provide xls files.
        for zip_url, reference_date in find_available_zips(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)

            for csv_file in extract_csv_files(zip_url):
                school_ids = {}
                student_residences = {}

                for row in csv_file :
                    # Remove leading/trailing spaces from field names and values.
                    for key in row.keys():
                        row[key.strip()] = row[key].strip()

                    brin = row['BRIN_NUMMER'].strip()
                    branch_id = int(row['VESTIGINGSNUMMER'])
                    school_id = '%s-%s' % (brin, branch_id)

                    school_ids[school_id] = {
                        'brin': brin,
                        'branch_id': branch_id
                    }

                    if school_id not in student_residences:
                        student_residences[school_id] = []

                    student_residence = {
                        'zip_code': row['POSTCODE_LEERLING'].strip(),
                        'ages': []
                    }

                    for age in range(3, 26):
                        if row.has_key('LEEFTIJD_%i_JAAR' % age):
                            student_residence['ages'].append({
                                'age': age,
                                # Find out why Sicco casts to a float before he
                                # cast to an int..
                                'students': int(float(row['LEEFTIJD_%i_JAAR' % age].strip()))
                            })

                    student_residences[school_id].append(student_residence)

                    for school_id, residence in student_residences.iteritems():
                        school = DuoPoBranch(
                            brin=school_ids[school_id]['brin'],
                            branch_id=school_ids[school_id]['branch_id'],
                            reference_year=reference_year,
                            student_residences_reference_url=zip_url,
                            student_residences_reference_date=reference_date,
                            student_residences=residence
                        )

                    yield school

    def parse_po_student_year(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            years_per_branch = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names. (?)
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEMEENTE NUMMER'):
                    row['GEMEENTENUMMER'] = row['GEMEENTE NUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                brin = row['BRIN NUMMER'].strip()
                branch_id = 0 if not row['VESTIGINGSNUMMER'] else int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # Remove leading/trailing spaces from field names.
                for key in row.keys():
                    row[key.strip()] = row[key]

                years = {}
                possible_years = '1 2 3 4 5 6 7 8'.split()
                for year in possible_years:
                    if row['LEERJAAR %s' % year].strip():
                        years['year_%s' % year] = int(row['LEERJAAR %s' % year])
                    else:
                        years['year_%s' % year] = 0
                # Is there a total student number from somewhere?
                # if row['TOTAAL'].strip():
                #         years['students'] = int(row['TOTAAL'])

                if school_id not in years_per_branch:
                    years_per_branch[school_id] = {}

                years_per_branch[school_id] = years

            for school_id, y_per_branch in years_per_branch.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_year_reference_url=csv_url,
                    students_by_year_reference_date=reference_date,
                    students_by_year=y_per_branch
                )
                yield school

    def parse_spo_students_by_birthyear(self, response):
        """
        Passend onderwijs > Leerlingen
        Parse: "05. Leerlingen speciaal (basis)onderwijs naar geboortejaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names. (?)
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']


                branch = DuoPoBranch()
                branch['brin'] = row['BRIN NUMMER'].strip()
                branch['branch_id'] = 0 if not row['VESTIGINGSNUMMER'] else int(row['VESTIGINGSNUMMER'])
                branch['reference_year']=reference_year

                # Should this be in root, or spo_students_by_birthyear?
                branch['spo_law'] = row['AANDUIDING WET']
                branch['spo_edu_type'] = row['SOORT PRIMAIR ONDERWIJS'] # possibly multiple with slash
                branch['spo_cluster'] = row['CLUSTER'] # i hope they don't use slashes                

                # ignoring total
                students_by_birthyear = []
                for k, v in row.iteritems():
                    row_words = k.split('.')
                    # k is of the form 'aantal.2005' or just the year (yes, really)
                    if row_words[-1].isdigit() and v.isdigit() and int(v)>0 :
                        students_by_birthyear.append({
                            'birthyear' : int(row_words[-1]),
                            'students' : int(v),
                        })
                        

                branch['spo_students_by_birthyear'] = students_by_birthyear
                branch['spo_students_by_birthyear_reference_url'] = csv_url
                branch['spo_students_by_birthyear_reference_date'] = reference_date

                yield branch
    
    def parse_spo_students_by_edu_type(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "06. Leerlingen speciaal (basis)onderwijs naar onderwijssoort"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            spo_students_by_edu_type_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                if row.has_key('INDICATIE SPECIAAL (BASIS)ONDERWIJS'): # really now
                    row['INDICATIE SPECIAL BASIS ONDERWIJS'] = row['INDICATIE SPECIAAL (BASIS)ONDERWIJS']

                brin = row['BRIN NUMMER'].strip()
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }


                spo_students_by_edu_type = {
                    'spo_indication' : row['INDICATIE SPECIAL BASIS ONDERWIJS'],
                    'spo' : int(row['SBAO'] or 0),
                    'so' : int(row['SO'] or 0),
                    'vso' : int(row['VSO'] or 0),
                    }

                if school_id not in spo_students_by_edu_type_per_school:
                    spo_students_by_edu_type_per_school[school_id] = []

                spo_students_by_edu_type_per_school[school_id].append(spo_students_by_edu_type)

            for school_id, per_school in spo_students_by_edu_type_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    spo_students_by_edu_type_reference_url=csv_url,
                    spo_students_by_edu_type_reference_date=reference_date,
                    spo_students_by_edu_type=per_school
                )
                yield school

    def parse_po_students_by_advice(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "12. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar schooladvies"

        TODO: compare to owinsp PRIMARY_SCHOOL_ADVICES_STRUCTURES
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            students_by_advice_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                brin = row['BRIN NUMMER'].strip()
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }


                spo_students_by_advice = {
                    # TODO intOrNone
                    'vso' : int(row['VSO'] or 0),
                    'pro' : int(row['PrO'] or 0),
                    'vmbo_bl' : int(row['VMBO BL'] or 0),
                    'vmbo_bl_kl' : int(row['VMBO BL-KL'] or 0),
                    'vmbo_kl' : int(row['VMBO KL'] or 0),
                    'vmbo_kl_gt' : int(row['VMBO KL-GT'] or 0),
                    'vmbo_gt' : int(row['VMBO GT'] or 0),
                    'vmbo_gt_havo' : int(row['VMBO GT-HAVO'] or 0),
                    'havo' : int(row['HAVO'] or 0),
                    'havo_vwo' : int(row['HAVO-VWO'] or 0),
                    'vwo' : int(row['VWO'] or 0),
                    'unknown' : int(row['ONBEKEND'] or 0),
                    }

                if school_id not in students_by_advice_per_school:
                    students_by_advice_per_school[school_id] = []

                students_by_advice_per_school[school_id].append(spo_students_by_advice)

            for school_id, per_school in students_by_advice_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    spo_students_by_advice_reference_url=csv_url,
                    spo_students_by_advice_reference_date=reference_date,
                    spo_students_by_advice=per_school
                )
                yield school

