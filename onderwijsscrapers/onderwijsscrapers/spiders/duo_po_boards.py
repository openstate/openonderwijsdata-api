class DuoPoBoardsSpider(BaseSpider):
    name = 'duo_po_boards'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/adressen/Adressen/po_adressen05.asp',
                    self.parse_po_boards),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/Financien/Jaarrekeninggegevens/'
                    'Kengetallen.asp', self.parse_po_financial_key_indicators),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/Leerlingen/Leerlingen/po_leerlingen7.asp',
                    self.parse_po_education_type)
        ]

    def parse_po_boards(row):
        """
        Primair onderwijs > Adressen
        Parse "05. Bevoegde gezagen basisonderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board = DuoPoBoard()
                board['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                board['name'] = row['BEVOEGD GEZAG NAAM']
                board['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'zip_code': row['POSTCODE'].replace(' ', ''),
                    'city': row['PLAATSNAAM']
                }

                board['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES']:
                    board['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'])
                else:
                    board['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES']:
                    board['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].replace(' ', '')
                else:
                    board['correspondence_address']['zip_code'] = None

                board['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'] or None

                board['municipality'] = row['GEMEENTENAAM'] or None

                board['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])

                board['phone'] = row['TELEFOONNUMMER'] or None

                board['website'] = row['INTERNETADRES'] or None

                board['denomination'] = row['DENOMINATIE'] or None

                board['administrative_office_id'] = \
                        int_or_none(row['ADMINISTRATIEKANTOORNUMMER'])

                board['reference_year'] = reference_year
                board['ignore_id_fields'] = ['reference_year']
                yield board

    def parse_po_financial_key_indicators(row):
        """
        Primair onderwijs > Financien > Jaarrekeninggegevens
        Parse "15. Kengetallen"
        """

        indicators_mapping = {
            'LIQUIDITEIT (CURRENT RATIO)': 'liquidity_current_ratio',
            'RENTABILITEIT': 'profitability',
            'SOLVABILITEIT 1': 'solvency_1',
            'SOLVABILITEIT 2': 'solvency_2',
            'ALGEMENE RESERVE / TOTALE BATEN': 'general_reserve_div_total_income',
            'BELEGGINGEN (T.O.V. EV)': 'investments_relative_to_equity',
            #'CONTRACTACTIVITEITEN / RIJKSBIJDRAGE': 'contract_activities_div_gov_funding',
            #'CONTRACTACTIVITEITEN / TOTALE BATEN': 'contractactivities_div_total_profits',
            'EIGEN VERMOGEN / TOTALE BATEN': 'equity_div_total_profits',
            #'INVESTERING HUISVESTING / TOTALE BATEN': 'housing_investment_div_total_profits',
            'INVESTERINGEN (INVENT.+APP.) / TOTALE BATEN': 'investments_div_total_profits',
            'KAPITALISATIEFACTOR': 'capitalization_ratio',
            'LIQUIDITEIT (QUICK RATIO)': 'liquidity_quick_ratio',
            'OV. OVERHEIDSBIJDRAGEN / TOT. BATEN': 'other_gov_funding_div_total_profits',
            'PERSONEEL / RIJKSBIJDRAGEN': 'staff_costs_div_gov_funding',
            'PERSONELE LASTEN / TOTALE LASTEN': 'staff_expenses_div_total_expenses',
            'RIJKSBIJDRAGEN / TOTALE BATEN': 'gov_funding_div_total_profits',
            'VOORZIENINGEN /TOTALE BATEN': 'facilities_div_total_profits',
            #'WEERSTANDSVERMOGEN (-/- MVA)': '',
            #'WEERSTANDSVERMOGEN VO TOTALE BN.': '',
            'WERKKAPITAAL / TOTALE BATEN': 'operating_capital_div_total_profits',
            'HUISVESTINGSLASTEN / TOTALE LASTEN': 'housing_expenses_div_total_expenses',
            'WERKKAPITAAL': 'operating_capital',
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            indicators_per_board = {}
            for row in parse_csv_file(csv_url):
                # Strip leading and trailing whitespace from field names and values.
                for key in row.keys():
                    row[key.strip()] = row[key].strip()

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in indicators_per_board:
                    indicators_per_board[board_id] = []

                indicators = {}
                indicators['year'] = int(row['JAAR'])
                indicators['group'] = row['GROEPERING']

                for ind, ind_norm in indicators_mapping.iteritems():
                    # Some fields have no value, just an empty string ''.
                    # Set those to 0.
                    if row[ind] == '':
                        row[ind] = '0'
                    indicators[ind_norm] = float(row[ind].replace('.', '')
                                                         .replace(',', '.'))

                indicators_per_board[board_id].append(indicators)

            for board_id, indicators in indicators_per_board.iteritems():
                board = DuoPoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    financial_key_indicators_per_year_url=csv_url,
                    financial_key_indicators_per_year_reference_date=reference_date,
                    financial_key_indicators_per_year=indicators
                )
                yield board

    def parse_po_education_type(row):
        """
        Primair onderwijs > Leerlingen
        Parse "07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort"
        """

        possible_edu_types = ['BAO', 'SBAO', 'SO', 'VSO']

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            students_per_edu_type = {}
            for row in parse_csv_file(csv_url):
                # Strip leading and trailing whitespace from field names and values.
                for key in row.keys():
                    if row[key]:
                        row[key.strip()] = row[key].strip()
                    else:
                        row[key.strip()] = '0'

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in students_per_edu_type:
                    students_per_edu_type[board_id] = []

                for edu_type in possible_edu_types:
                    if edu_type in row:
                        if row[edu_type] == '':
                            continue

                        if row[edu_type] == 0:
                            continue

                        students_per_edu_type[board_id].append({
                            'denomination': row['DENOMINATIE'],
                            'edu_type': edu_type,
                            'students': int(row[edu_type].replace('.', ''))
                        })

            for board_id, e_types in students_per_edu_type.iteritems():
                board = DuoPoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    students_per_edu_type_reference_url=csv_url,
                    students_per_edu_type_reference_date=reference_date,
                    students_per_edu_type=e_types
                )
                yield board
