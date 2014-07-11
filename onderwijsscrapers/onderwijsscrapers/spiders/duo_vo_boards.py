class DuoVoBoardsSpider(DuoSpider):
    name = 'duo_vo_boards'

    # requests = {
    #     'vo/adressen/Adressen/besturen.asp':
    #         self.parse_boards,
    #     'vo/Financien/Financien/Kengetallen.asp':
    #         self.parse_financial_key_indicators,
    #     'vo/leerlingen/Leerlingen/vo_leerlingen4.asp':
    #         self.parse_vavo_students,
    # }

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/adressen/Adressen/besturen.asp',
                    self.parse_boards),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/Financien/Financien/Kengetallen.asp',
                    self.parse_financial_key_indicators),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen4.asp',
                    self.parse_vavo_students),
        ]

    def parse_boards(row):
        """
        Parse "03. Adressen bevoegde gezagen"
        """
        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board = DuoVoBoard()
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

                board['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].replace(' ', '') or None

                board['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'] or None

                board['municipality'] = row['GEMEENTENAAM'] or None

                board['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])

                board['phone'] = row['TELEFOONNUMMER'] or None

                board['website'] = row['INTERNETADRES'] or None

                board['denomination'] = row['DENOMINATIE'] or None

                board['administrative_office_id'] = int_or_none(row['ADMINISTRATIEKANTOORNUMMER'])

                board['reference_year'] = reference_year
                board['ignore_id_fields'] = ['reference_year']
                yield board

    def parse_financial_key_indicators(row):
        """
        Parse "15. Kengetallen"
        """

        indicators_mapping = {
            'LIQUIDITEIT (CURRENT RATIO)': 'liquidity_current_ratio',
            'RENTABILITEIT': 'profitability',
            'SOLVABILITEIT 1': 'solvency_1',
            'SOLVABILITEIT 2': 'solvency_2',
            'ALGEMENE RESERVE / TOTALE BATEN': 'general_reserve_div_total_income',
            'BELEGGINGEN (T.O.V. EV)': 'investments_relative_to_equity',
            'CONTRACTACTIVITEITEN / RIJKSBIJDRAGE': 'contract_activities_div_gov_funding',
            'CONTRACTACTIVITEITEN / TOTALE BATEN': 'contractactivities_div_total_profits',
            'EIGEN VERMOGEN / TOTALE BATEN': 'equity_div_total_profits',
            'INVESTERING HUISVESTING / TOTALE BATEN': 'housing_investment_div_total_profits',
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
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in indicators_per_board:
                    indicators_per_board[board_id] = []

                indicators = {}
                indicators['year'] = int(row['JAAR'])
                indicators['group'] = row['GROEPERING']

                for ind, ind_norm in indicators_mapping.iteritems():
                    indicators[ind_norm] = float(row[ind].replace('.', '')
                                                         .replace(',', '.'))

                indicators_per_board[board_id].append(indicators)

            for board_id, indicators in indicators_per_board.iteritems():
                board = DuoVoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    financial_key_indicators_per_year_url=csv_url,
                    financial_key_indicators_per_year_reference_date=reference_date,
                    financial_key_indicators_per_year=indicators
                )

                yield board

    def parse_vavo_students(row):
        """
        Primair onderwijs > Leerlingen
        Parse "04 Leerlingen per bestuur en denominatie (vavo apart)"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            vavo_students_per_school = {}

            for row in parse_csv_file(csv_url):

                board_id = int(row['BEVOEGD GEZAG NUMMER'].strip())

                vavo_students = {
                    'non_vavo' : int(row['AANTAL LEERLINGEN'] or 0),
                    'vavo' : int(row['AANTAL VO LEERLINGEN UITBESTEED AAN VAVO'] or 0),
                }

                if board_id not in vavo_students_per_school:
                    vavo_students_per_school[board_id] = []
                vavo_students_per_school[board_id].append(vavo_students)

            for board_id, per_school in vavo_students_per_school.iteritems():
                school = DuoVoBranch(
                    board_id=board_id,
                    reference_year=reference_year,
                    vavo_students_reference_url=csv_url,
                    vavo_students_reference_date=reference_date,
                    vavo_students=per_school,
                )
                yield school