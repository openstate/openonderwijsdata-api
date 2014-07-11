class DuoPoSchoolsSpider(BaseSpider):
    name = 'duo_po_schools'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/adressen/Adressen/hoofdvestigingen.asp',
            #         self.parse_po_schools),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen4.asp',
            #         self.parse_spo_students_per_cluster),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/passendow/Adressen/Adressen/passend_po_2.asp',
            #         self.parse_po_lo_collaboration),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_4.asp',
                    self.parse_pao_collaboration),
        ]

    def parse_po_schools(row):
        """
        Primair onderwijs > Adressen
        Parse: "01. Hoofdvestigingen basisonderwijs"
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

                school = DuoPoSchool()
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

                school['municipality_code'] = int(row['GEMEENTENUMMER'])

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

    def parse_spo_students_per_cluster(row):
        """
        Primair onderwijs > Leerlingen
        Parse "04. Leerlingen speciaal onderwijs naar cluster"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            spo_students_per_cluster_per_school = {}


            for row in parse_csv_file(csv_url):
                spo_students_per_cluster_per_school[row['BRIN NUMMER']] = {
                    'cluster_1': int(row['CLUSTER 1']),
                    'cluster_2': int(row['CLUSTER 2']),
                    'cluster_3': int(row['CLUSTER 3']),
                    'cluster_4': int(row['CLUSTER 4']),
                }

            for brin, spo_students_per_cluster in spo_students_per_cluster_per_school.iteritems():
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    spo_students_per_cluster_reference_url=csv_url,
                    spo_students_per_cluster_reference_date=reference_date,
                    spo_students_per_cluster=spo_students_per_cluster
                )
                yield school

    def parse_po_lo_collaboration(row):
        """
        Passend onderwijs > Adressen
        Parse "02. Adressen instellingen per samenwerkingsverband lichte ondersteuning, primair onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            po_lo_collaboration_per_school = {}

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

                if brin not in po_lo_collaboration_per_school:
                    po_lo_collaboration_per_school[brin] = []

                po_lo_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in po_lo_collaboration_per_school.iteritems():
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    po_lo_collaboration_reference_url=csv_url,
                    po_lo_collaboration_reference_date=reference_date,
                    po_lo_collaboration=per_school
                )
                yield school

    def parse_pao_collaboration(row):
        """
        Passend onderwijs > Adressen
        Parse "04. Adressen instellingen per samenwerkingsverband passend onderwijs, primair onderwijs"
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
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    pao_collaboration_reference_url=csv_url,
                    pao_collaboration_reference_date=reference_date,
                    pao_collaboration=per_school
                )
                yield school
