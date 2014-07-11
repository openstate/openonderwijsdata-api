class DuoPaoCollaborationsSpider(BaseSpider):
    name = 'duo_pao_collaborations'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_1.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_3.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_1.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_7.asp',
                    self.parse_collaborations),
        ]

    def parse_collaborations(row):
        """
        Passend onderwijs > Adressen
        Parse: "01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs"
        Parse: "03. Adressen samenwerkingsverbanden passend onderwijs, primair onderwijs"
        Parse: "05. Adressen samenwerkingsverbanden lichte ondersteuning, voortgezet onderwijs"
        Parse: "07. Adressen samenwerkingsverbanden passend onderwijs, voortgezet onderwijs"
        """
        # Fields that do not need additonal processing
        collaboration_fields = {
            'SAMENWERKINGSVERBAND': 'collaboration'
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):

                collaboration = DuoPaoCollaboration()
                
                cid = row['ADMINISTRATIENUMMER'].strip()
                if '-' in cid:
                    int_parts = map(int_or_none, cid.split('-'))
                    if any([i == None for i in int_parts]):
                        cid = '-'.join(map(str, int_parts))
                collaboration['collaboration_id'] = cid

                collaboration['address'] = {
                    'street': row['ADRES'].strip() or None,
                    'city': row['PLAATSNAAM'].strip() or None,
                    'zip_code': row['POSTCODE'].replace(' ', '') or None
                }

                collaboration['correspondence_address'] = {
                    'street': row['CORRESPONDENTIEADRES'],
                    'city': row['PLAATS CORRESPONDENTIEADRES'],
                    'zip_code': row['POSTCODE CORRESPONDENTIEADRES'].replace(' ', '')
                }

                for field, field_norm in collaboration_fields.iteritems():
                    collaboration[field_norm] = row[field]

                collaboration['reference_year'] = reference_year
                collaboration['ignore_id_fields'] = ['reference_year']

                yield collaboration
