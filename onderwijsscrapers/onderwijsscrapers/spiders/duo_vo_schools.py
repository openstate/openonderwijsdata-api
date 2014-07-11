class DuoVoSchoolsSpider(BaseSpider):
    name = 'duo_vo_schools'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vo/adressen/Adressen/hoofdvestigingen.asp',
            #         self.parse_schools),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vschoolverlaten/vsv_voortgezet.asp',
            #         self.parse_dropouts),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen11.asp',
            #         self.parse_students_prognosis),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_6.asp',
                    self.parse_vo_lo_collaboration),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_8.asp',
                    self.parse_pao_collaboration),
        ]

    def parse_schools(row):
        """
        Parse: "01. Adressen hoofdvestigingen"
        """

        # Fields that do not need additonal processing
        school_fields = {
            'BRIN NUMMER': 'brin',
            'PROVINCIE': 'province',
            'INSTELLINGSNAAM': 'name',
            'GEMEENTENAAM': 'municipality',
            'DENOMINATIE': 'denomination',
            'INTERNETADRES': 'website',
            'TELEFOONNUMMER': 'phone',
            'ONDERWIJSGEBIED NAAM': 'education_area',
            'NODAAL GEBIED NAAM': 'nodal_area',
            'RPA-GEBIED NAAM': 'rpa_area',
            'WGR-GEBIED NAAM': 'wgr_area',
            'COROPGEBIED NAAM': 'corop_area',
            'RMC-REGIO NAAM': 'rmc_region'
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = row[key].strip()
                    row[key] = value or None

                school = DuoVoSchool()
                school['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'city': row['PLAATSNAAM'],
                    'zip_code': row['POSTCODE'].replace(' ', '')
                }

                school['correspondence_address'] = {
                    'street': '%s %s' % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                                         row['HUISNUMMER-TOEVOEGING '
                                             'CORRESPONDENTIEADRES']),
                    'city': row['PLAATSNAAM CORRESPONDENTIEADRES'],
                    'zip_code': row['POSTCODE CORRESPONDENTIEADRES']
                }

                school['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])
                school['education_structures'] = row['ONDERWIJSSTRUCTUUR']
                if school['education_structures']:
                    school['education_structures'] = school['education_structures'].split('/')

                if row['COROPGEBIED CODE']:
                    school['corop_area_code'] = int(row['COROPGEBIED CODE'])

                school['nodal_area_code'] = int_or_none(row['NODAAL GEBIED CODE'])

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'])

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'])

                school['education_area_code'] = int_or_none(row['ONDERWIJSGEBIED CODE'])

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'])

                for field, field_norm in school_fields.iteritems():
                    school[field_norm] = row[field]

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']

                yield school

    def parse_dropouts(row):
        """
        Parse: "02. Vsv in het voortgezet onderwijs per vo instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            dropouts_per_school = {}
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace and remove
                # thousands separator ('.')
                for key in row.keys():
                    row[key] = row[key].strip().replace('.', '')

                brin = row['BRIN NUMMER']

                if brin not in dropouts_per_school:
                    dropouts_per_school[brin] = []

                dropouts = {
                    'year': int(row['JAAR']),
                    'education_structure': row['ONDERWIJSSTRUCTUUR EN LEERJAAR'],
                    'total_students': int(row['AANTAL DEELNEMERS']),
                    'total_dropouts': int(row['AANTAL VSV ERS']),
                    'dropouts_with_vmbo_diploma': int(row['AANTAL VSV ERS MET VMBO DIPLOMA']),
                    'dropouts_with_mbo1_dimploma': int(row['AANTAL VSV ERS MET MBO1 DIPLOMA']),
                    'dropouts_without_diploma': int(row['AANTAL VSV ERS ZONDER DIPLOMA'])
                }

                if row['PROFIEL'] == 'NVT':
                    dropouts['sector'] = None
                else:
                    dropouts['sector'] = row['PROFIEL']

                dropouts_per_school[brin].append(dropouts)

            for brin, dropouts in dropouts_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    dropouts_per_year_url=csv_url,
                    dropouts_per_year=dropouts,
                    dropouts_per_year_reference_date=reference_date,
                    reference_year=reference_year,
                )

                yield school

    def parse_students_prognosis(row):
        """
        Parse: "11. Prognose aantal leerlingen"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            students_prognosis_per_school = {}
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace and remove
                # thousands separator ('.')
                for key in row.keys():
                    row[key] = row[key].strip().replace('.', '')

                brin = row['BRIN NUMMER']

                if brin not in students_prognosis_per_school:
                    students_prognosis_per_school[brin] = []

                # ignoring actual data for now, only adding prognosis
                students_prognosis = []
                for k, v in row.iteritems():
                    row_words = k.split()
                    # k is of the form 'PROGNOSE LWOO PRO 2024'
                    if row_words[0] == 'PROGNOSE' or row_words[0]=='POGNOSE': # don't ask
                        if row_words[-1].isdigit():
                            students_prognosis.append({
                                'year' : int(row_words[-1]),
                                'structure' : '_'.join(row_words[1:-1]).lower(),
                                'students' : int(v),
                            })

                students_prognosis_per_school[brin].append(students_prognosis)

            for brin, students_prognosis in students_prognosis_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    students_prognosis_url=csv_url,
                    students_prognosis=students_prognosis,
                    students_prognosis_reference_date=reference_date,
                    reference_year=reference_year,
                )

                yield school

    def parse_vo_lo_collaboration(row):
        """
        Passend onderwijs > Adressen
        Parse "06. Adressen instellingen per samenwerkingsverband lichte ondersteuning, voortgezet onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            vo_lo_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                cid = row['ADMINISTRATIENUMMER'].strip()
                if '-' in cid:
                    int_parts = map(int_or_none, cid.split('-'))
                    if any([i == None for i in int_parts]):
                        cid = '-'.join(map(str, int_parts))
                collaboration = cid

                if brin not in vo_lo_collaboration_per_school:
                    vo_lo_collaboration_per_school[brin] = []

                vo_lo_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in vo_lo_collaboration_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    vo_lo_collaboration_reference_url=csv_url,
                    vo_lo_collaboration_reference_date=reference_date,
                    vo_lo_collaboration=per_school
                )
                yield school

    def parse_pao_collaboration(row):
        """
        Passend onderwijs > Adressen
        Parse "08. Adressen instellingen per samenwerkingsverband passend onderwijs, voortgezet onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            pao_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                collaboration = row['ADMINISTRATIENUMMER']

                if brin not in pao_collaboration_per_school:
                    pao_collaboration_per_school[brin] = []

                pao_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in pao_collaboration_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    pao_collaboration_reference_url=csv_url,
                    pao_collaboration_reference_date=reference_date,
                    pao_collaboration=per_school
                )
                yield school
