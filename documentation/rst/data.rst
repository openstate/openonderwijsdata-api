Data
=================================================================================
The data that is made available through the API originates from different sources: :ref:`duodata`, :ref:`schoolvodata` and the :ref:`owinspdata`. Each of these sources provides different types of data, from school assessments to financial figures. For each source the available fields are described, as well as the data they contain.

The data sources present their data aggregated on different *granularities*: financial data is usually aggregated to the level of the school *board*, whereas the number of students is available for specific locations (*branch*) of a school. In order to represent the data properly, three entities are defined: *vo_board*, *vo_school* and *vo_branch*.

**vo_board** (in Dutch: *schoolbestuur*)
    A vo_board represents the school board in secondary education. The school board is responsible for decisions about education provided at their school(s), as well as the school in general [#schoolbestuur]_. For example, the board is responsible for the financial health of its schools. Boards can be responsible for multiple schools.

**vo_school** (in Dutch: *middelbare school*)
    A vo_school represents an institution where secondary education is provided to students. Data regarding the success rate at exams is aggregated at this level. A vo_school is identified by a BRIN, an identifier for schools and related institutions such as universities [#brin]_. A school can have multiple physical locations (*branches*), where for example different levels of education are offered.

**vo_branch** (in Dutch: *afdeling middelbare school*)
    A school can be located at different (geographical) locations. For example, large schools that offer different levels of education [#edu_in_holland]_ often do so at separate buildings. These different departments are represented by a *vo_branch*.

Note that many fields in the :ref:`duodata` overlap, as these data is available on both levels.

For some fields the original Dutch term is included, in order to allow the API user to look up the definition of that term at the source collection.

.. _duodata:

DUO
---------------------------------------------------------------------------------
.. _duovoboard:

vo_board
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 03. Adressen hoofdbesturen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/besturen.asp>`_

.. table::

    ================================================ =================================== =================================== =============================================================
    Field                                            Type                                Original term                       Description
    ================================================ =================================== =================================== =============================================================
    address                                          :ref:`duoaddress`                                                       Address of this board.
    administrative_office_id                         integer                             Administratiekantoor                Identifier (assigned by :ref:`duodata`) for the accountancy firm that manages this board finances.
    board_id                                         integer                                                                 Identifier (assigned by :ref:`duodata`) of the board of this branch.
    correspondence_address                           :ref:`duoaddress`                                                       Correspondence address of this board.
    denomination                                     string                                                                  In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    financial_key_indicators_per_year                array of :ref:`finindicator`                                            Array of :ref:`finindicator`, where each item represents a set of key financial indicators for a given year.
    financial_key_indicators_per_year_reference_date date                                                                    Date the financial key indicator source file was published at http://data.duo.nl
    financial_key_indicators_per_year_url            string                                                                  URL to the financial key indicator source file at http://data.duo.nl
    meta                                             :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                                     string                                                                  The name of the municipality this board is located in.
    municipality_code                                integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                             string                                                                  Name of the board.
    phone                                            string                                                                  Phone number of the board.
    reference_year                                   date                                                                    Year the boards source file was published
    website                                          string                                                                  URL of the webpage of the board.
    ================================================ =================================== =================================== =============================================================

.. _duovoschool:

vo_school
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 01. Adressen hoofdvestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/hoofdvestigingen.asp>`_

.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    address                             :ref:`duoaddress`                                                       Address of this school.
    board_id                            integer                                                                 Identifier (assigned by :ref:`duodata`) of the board of this school.
    brin                                string                                                                  "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    corop_area                          string                              COROP-gebied                        A COROP area in the Netherlands is a region consisting of several municipalities, and is primarily used by research institutions to present statistical data. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
    corop_area_code                     integer                                                                 Identifier of the corop_area.
    correspondence_address              :ref:`duoaddress`                                                       Correspondence address of this school.
    denomination                        string                                                                  In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    dropouts_per_year                   array of :ref:`dropout`                                                 Array of :ref:`dropout`, where each item represents the dropouts for a specific year, per school year.
    dropouts_per_year_reference_date    date                                                                    Date the dropouts source file was published at http://data.duo.nl.
    dropouts_per_year_url               string                                                                  URL to the dropouts source file at http://data.duo.nl.
    education_area                      string                              Onderwijsgebied                     Education areas are aggregations of nodal areas based on regional origins and destinations of students in secondary education. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
    education_area_code                 integer                                                                 Identifier of the education_area.
    education_structures                array                                                                   An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    meta                                :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                        string                                                                  The name of the municipality this branch is located in.
    municipality_code                   integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                string                                                                  Name of the school.
    nodal_area                          string                              Nodaal gebied                       Area defined for the planning of distribution of secondary schools. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
    nodal_area_code                     integer                                                                 Identifier of the nodal_area.
    phone                               string                                                                  Phone number of the school.
    province                            string                                                                  The province [#provinces]_ this branch is situated in.
    reference_year                      integer                                                                 Year the schools source file was published.
    rmc_region                          string                              Rmc-regio                           Area that is used for the coordination of school dropouts. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
    rmc_region_code                     integer                                                                 Identifier of the rmc_region.
    rpa_area                            string                              Rpa-gebied                          Area defined to cluster information on the labour market. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
    rpa_area_code                       integer                                                                 Identifier of the rpa_area.
    website                             string                                                                  Website of this school.
    wgr_area                            string                              Wgr-gebied                          Cluster of municipalities per collaborating region according to the "Wet gemeenschappelijke regelingen" [#wgr_law]_. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied.
    wgr_area_code                       integer                                                                 Identifier of the wgr_area.
    =================================== =================================== =================================== ==========================================================================

.. _duovobranch:

vo_branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 02. Adressen alle vestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/vestigingen.asp>`_

.. table::

    ======================================= =================================== =================================== ======================================================================
    Field                                   Type                                Original term                       Description
    ======================================= =================================== =================================== ======================================================================
    address                                 :ref:`duoaddress`                                                       Address of this branch.
    board_id                                integer                                                                 Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                               integer                                                                 Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                    string                                                                  "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    corop_area                              string                              COROP-gebied                        A COROP area in the Netherlands is a region consisting of several municipalities, and is primarily used by research institutions to present statistical data. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
    corop_area_code                         integer                                                                 Identifier of the corop_area.
    correspondence_address                  :ref:`duoaddress`                                                       Correspondence address of this branch.
    denomination                            string                                                                  In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_area                          string                              Onderwijsgebied                     Education areas are aggregations of nodal areas based on regional origins and destinations of students in secondary education. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
    education_area_code                     integer                                                                 Identifier of the education_area.
    education_structures                    array                                                                   An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    meta                                    :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                            string                                                                  The name of the municipality this branch is located in.
    municipality_code                       integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                    string                                                                  Name of the school.
    nodal_area                              string                              Nodaal gebied                       Area defined for the planning of distribution of secondary schools. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
    nodal_area_code                         integer                                                                 Identifier of the nodal_area.
    phone                                   string                                                                  Phone number of the school.
    province                                string                                                                  The province [#provinces]_ this branch is situated in.
    reference_year                          integer                                                                 Year the schools source file was published.
    rmc_region                              string                              Rmc-regio                           Area that is used for the coordination of school dropouts. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
    rmc_region_code                         integer                                                                 Identifier of the rmc_region.
    rpa_area                                string                              Rpa-gebied                          Area defined to cluster information on the labour market. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
    rpa_area_code                           integer                                                                 Identifier of the rpa_area.
    student_residences                      array of :ref:`duostdres`                                               Array of :ref:`duostdres`, where each item contains the distribution of students from a given municipality over the years in this branch.
    student_residences_reference_date       date                                                                    Date the student residences source file was published at http://data.duo.nl
    student_residences_url                  string                                                                  URL of the student residences source file.
    students_by_structure                   array of :ref:`duostdstruct`                                            Distribution of students by education structure and gender.
    students_by_structure_reference_date    date                                                                    Date the student per structure source file was published at http://data.
    students_by_structure_url               string                                                                  URL of the student by structure source file.
    website                                 string                                                                  Website of this school.
    wgr_area                                string                              Wgr-gebied                          Cluster of municipalities per collaborating region according to the "Wet gemeenschappelijke regelingen" [#wgr_law]_. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied.
    wgr_area_code                           integer                                                                 Identifier of the wgr_area.
    ======================================= =================================== =================================== ======================================================================

.. _duoaddress:

Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/default.asp>`_

.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    city                                string                                                                  Name of the city or village this branch is located.
    street                              string                                                                  Street name and number of the address of this branch.
    zip_code                            string                                                                  Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    =================================== =================================== =================================== ==========================================================================

.. _dropout:

Dropout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortijdig schoolverlaten - Voortijdig schoolverlaten - 02. Vsv in het voortgezet onderwijs per vo instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vschoolverlaten/vsvers/vsv_voortgezet.asp>`_

.. table::

    ======================================= =================================== =================================== ======================================================================
    Field                                   Type                                Original term                       Description
    ======================================= =================================== =================================== ======================================================================
    dropouts_with_mbo1_diploma              integer                             Aantal VSV-ers met MBO 1 diploma    Number of dropouts having a MBO 1 diploma (apprenticeship level) [#mbo1]_.
    dropouts_with_vmbo_diploma              integer                             Aantal VSV-ers met VMBO diploma     Number of dropouts having a VMBO diploma [#vmbo]_.
    dropouts_without_diploma                integer                             Aantal VSV-ers zonder diploma       Number of dropouts having no diploma.
    education_structure                     string                                                                  Level of education [#edu_in_holland]_.
    sector                                  string                              profiel/sector                      Package of courses a student takes in secondary education [#sectors]_ [#profiles]_.
    total_dropouts                          integer                                                                 Total dropouts for the given year at this school.
    total_students                          integer                                                                 Total students for the given year at this school.
    year                                    integer                                                                 The year the dropout numbers apply to.
    ======================================= =================================== =================================== ======================================================================

.. _finindicator:

FinancialIndicator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Financiën - 15. Kengetallen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/Financien/Financien/Kengetallen.asp>`_

.. table::

    ======================================= =============================== ======================================== =====================================================================
    Field                                   Type                            Original term                            Description
    ======================================= =============================== ======================================== =====================================================================
    capitalization_ratio                    float                           Kapitalisatiefactor
    contract_activities_div_gov_funding     float                           Contractactiviteiten/rijksbijdragen
    contractactivities_div_total_profits    float                           Contractactiviteiten/totale baten
    equity_div_total_profits                float                           Eigen vermogen/totale baten
    facilities_div_total_profits            float                           Voorzieningen/totale baten
    general_reserve_div_total_income        float                           Algemene reserve/totale baten
    gov_funding_div_total_profits           float                           Rijksbijdragen/totale baten
    group                                   string                          Groepering
    housing_expenses_div_total_expenses     float                           Huisvestingslasten/totale lasten
    housing_investment_div_total_profits    float                           Investering huisvesting/totale baten
    investments_div_total_profits           float                           Investeringen/totale baten
    investments_relative_to_equity          float                           Beleggingen t.o.v. eigen vermogen
    liquidity_current_ratio                 float                           Liquiditeit (current ratio)
    liquidity_quick_ratio                   float                           Liquiditeit (quick ratio)
    operating_capital_div_total_profits     float                           Werkkapitaal/totale baten
    operating_capital                       float                           Werkkapitaal
    other_gov_funding_div_total_profits     float                           Overige overheidsbijdragen/totale baten
    profitability                           float                           Rentabiliteit
    solvency_1                              float                           Solvabiliteit 1
    solvency_2                              float                           Solvabiliteit 2
    staff_costs_div_gov_funding             float                           Personeel/rijksbijdragen
    staff_expenses_div_total_expenses       float                           Personele lasten/totale lasten
    year                                    integer
    ======================================= =============================== ======================================== =====================================================================

.. _duometa:

Meta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    item_scraped_at                     datetime                            The date and time this branch was scraped from the source.
    scrape_started_at                   datetime                            The date and time the scrape session this item was downloaded in started.
    validated_at                        datetime                            The date and time this item was validated.
    validation_result                   string                              Indication whether the item passed validation.
    =================================== =================================== ======================================================================================================

.. _duostdres:

StudentResidence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 02. Leerlingen per vestiging naar postcode leerling en leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen2.asp>`_

.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    city                                string                                                                  The name of the city, town or village the students originate from.
    municipality                        string                                                                  The name of the municipality this branch is located in.
    municipality_code                   integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    year_1                              integer                                                                 The amount of students from this location in year 1.
    year_2                              integer                                                                 The amount of students from this location in year 2.
    year_3                              integer                                                                 The amount of students from this location in year 3.
    year_4                              integer                                                                 The amount of students from this location in year 4.
    year_5                              integer                                                                 The amount of students from this location in year 5.
    year_6                              integer                                                                 The amount of students from this location in year 6.
    zip_code                            string                                                                  Zip code (area) of the location the students originate from. Note that this value does not have to be a complete zipcode [#zipcodes]_, but can be somewhat anonimised (in order to preserve privacy of students) by being shortened to two digits. Also, students do not necessarily have a permanent residence.
    =================================== =================================== =================================== ==========================================================================

.. _duostdstruct:

StudentPerStructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 01. Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp>`_

.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    department                          string                                                                  Optional. Department of a vmbo track.
    education_name                      string                                                                  Name of the education programme.
    education_structure                 string                                                                  Level of education [#edu_in_holland]_.
    element_code                        integer                                                                 Unknown.
    lwoo                                boolean                                                                 Indicates whether this sector supports "Leerwegondersteunend onderwijs", for students who need additional guidance [#lwoo]_.
    vmbo_sector                         string                                                                  Vmbo sector [#sectors]_.
    year_1                              mapping                                                                 Distribution of male and female students for year 1.
    year_2                              mapping                                                                 Distribution of male and female students for year 2.
    year_3                              mapping                                                                 Distribution of male and female students for year 3.
    year_4                              mapping                                                                 Distribution of male and female students for year 4.
    year_5                              mapping                                                                 Distribution of male and female students for year 5.
    year_6                              mapping                                                                 Distribution of male and female students for year 6.
    =================================== =================================== =================================== ==========================================================================


.. _schoolvodata:

Vensters voor Verantwoording
---------------------------------------------------------------------------------
vo_branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ========================================================================================================
    Field                               Type                                Description
    =================================== =================================== ========================================================================================================
    address                             :ref:`schoolvoaddress`              Address of the branch.
    avg_education_hours_per_student     array of :ref:`eduhours`            Array of :ref:`eduhours`, representing how many hours of education were planned for a year, and how many are actually realised.
    avg_education_hours_per_student_url string                              URL to the *Onderwijstijd* page.
    board                               string                              The name of the board of this school.
    board_id                            integer                             Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                           integer                             Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    building_img_url                    string                              URL to a photo of the building of this branch.
    costs                               :ref:`costs`                        Object representing the costs a parent can expect for this branch.
    costs_url                           string                              URL to the *Onderwijskosten* page.
    denomination                        string                              In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_structures                array                               An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    email                               string                              Email address of this branch.
    logo_img_url                        string                              URL to a photo of the logo of the school of this branch.
    meta                                :ref:`schoolvometa`                 Metadata, such as date of scrape and whether this item passed validation.
    municipality                        string                              The name of the municipality this branch is located in.
    municipality_code                   integer                             Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                string                              Name of the branch of this school.
    parent_satisfaction                 array of :ref:`satisfaction`        Satisfaction polls of parents.
    parent_satisfaction_url             string                              URL to the *Tevredenheid ouders* page.
    phone                               string                              Unnormalised string representing the phone number of this branch.
    profile                             string                              Short description of the motto of this branch.
    province                            string                              The province [#provinces]_ this branch is situated in.
    schoolkompas_status_id              integer                             Identifier used at http://schoolkompas.nl. Use unknown.
    schoolvo_code                       string                              Identifier used at http://schoolvo.nl. Consists of the board_id, brin and branch_id, separated by dashes. A school page can be accessed at `http://schoolvo.nl/?p_schoolcode=`\ *<schoolvo_code>*.
    schoolvo_id                         integer                             Identifier used at schoolvo internally.
    schoolvo_status_id                  integer                             Use unknown.
    student_satisfaction                array of :ref:`satisfaction`        Satisfaction polls of students.
    student_satisfaction_url            string                              URL to the *Tevredenheid leerlingen* page.
    website                             string                              URL of the website of the school.
    =================================== =================================== ========================================================================================================


.. _schoolvoaddress:

Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    city                                string                              Name of the city or village this branch is located.
    street                              string                              Street name and number of the address of this branch.
    zip_code                            string                              Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    geo_location                        :ref:`schoolvo_coordinates`         The latitude and longitude of this branch.
    =================================== =================================== ======================================================================================================

.. _schoolvo_coordinates:

Coordinates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    lat                                 float                               Latitude of the address of this branch.
    lon                                 float                               Longitude of the address of this branch.
    =================================== =================================== ======================================================================================================

.. _costs:

Costs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    documents                           array                               Array containing URLs (string) to documents the school published regarding the costs for parents.
    explanation                         string                              Optional explanation provided by the school.
    per_year                            Array of :ref:`costsperyear`        Many schools provide a detailed overview of the costs per year, which are described in this array.
    signed_code_of_conduct              boolean                             *True* if the school signed the code of conduct of the VO-raad [#voraad]_ regarding school costs [#coc]_.
    =================================== =================================== ======================================================================================================

.. _costsperyear:

CostsPerYear
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    amount_euro                         float                               Costs in € (euro) for this year.
    explanation                         string                              Optional explanation of the details of the costs (*for a labcoat, for travel, ...*)
    link                                string                              Optional URL to a document detailing costs.
    other_costs                         boolean                             Indication whether parents should expect additional costs, other than the costs mentioned here.
    year                                string                              String representation of the years these costs apply to.
    =================================== =================================== ======================================================================================================

.. _eduhours:

EduHoursPerStudent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    hours_planned                       integer                             Hours of education planned by the school council [#medezeggenschapsraad]_ for the past year.
    hours_realised                      integer                             Hours of education realised at the school [#medezeggenschapsraad]_ for the past year.
    year                                string                              The school year the hours apply to. There are various ways in which these years are represented at `Vensters voor Verantwoording <http://schoolvo.nl>`_, but the most common is *Leerjaar <n>*.
    per_structure                       array of :ref:`eduhoursstructure`   Array of :ref:`eduhoursstructure`, representing the planning and realisation of education hours per education structure.
    =================================== =================================== ======================================================================================================

.. _eduhoursstructure:

EduHoursPerStructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    hours_planned                       integer                             Hours of education planned by the school council [#medezeggenschapsraad]_ for the past year.
    hours_realised                      integer                             Hours of education realised at the school [#medezeggenschapsraad]_ for the past year.
    structure                           string                              The structure these hours apply to (*vbmo-t, havo, vwo, ...*)
    =================================== =================================== ======================================================================================================

.. _indicator:

Indicator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    grade                               float                               The average grade student/parents awarded this indicator.
    indicator                           string                              The indicator.
    =================================== =================================== ======================================================================================================

.. _schoolvometa:

Meta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    item_scraped_at                     datetime                            The date and time this branch was scraped from the source.
    scrape_started_at                   datetime                            The date and time the scrape session this item was downloaded in started.
    validated_at                        datetime                            The date and time this item was validated.
    validation_result                   string                              Indication whether the item passed validation.
    =================================== =================================== ======================================================================================================

.. _satisfaction:

Satisfaction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    average_grade                       float                               The average satisfaction grade of this structure (*0.0 <= average_grade <= 10.0*).
    education_structure                 string                              String representing the education structure [#edu_in_holland]_ this satisfaction surveys were collected for.
    indicators                          array of :ref:`indicator`           Array of :ref:`indicator`, which indicate satisfaction scores for specific indicators [#tevr_stud]_ [#tevr_par]_.
    national_grade                      float                               The average grade for all these structures in the Netherlands (*0.0 <= average_grade <= 10.0*).
    source                              string                              Optional string describing the origin of the survey data.
    =================================== =================================== ======================================================================================================

.. _owinspdata:

Onderwijsinspectie
---------------------------------------------------------------------------------
.. _owinspdatavobranch:

vo_branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ========================================================================================================
    Field                               Type                                Description
    =================================== =================================== ========================================================================================================
    address                             :ref:`owinspaddress`                Address of this branch
    board                               string                              The name of the board of this school.
    board_id                            integer                             Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                           integer                             Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    current_ratings                     array of :ref:`owinspcurrat`        Array of :ref:`owinspcurrat`, where each item represents the current rating of the Onderwijsinspectie [#owinsp]_.
    denomination                        string                              In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_structures                array                               An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    meta                                :ref:`owinspmeta`                   Metadata, such as date of scrape and whether this item passed validation.
    name                                string                              Name of this branch.
    rating_history                      array of :ref:`owinsprathist`       Array of :ref:`owinsprathist`, where each item represents a rating the Onderwijsinspectie [#owinsp]_ awarded to this branch.
    reports                             array of :ref:`owinspreport`        Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.
    result_card_url                     string                              URL to the result card ("opbrengstenkaart") of this branch.
    website                             string                              Website of this branch (optional).
    =================================== =================================== ========================================================================================================

.. _owinspaddress:

Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    city                                string                              Name of the city or village this branch is located.
    street                              string                              Street name and number of the address of this branch.
    zip_code                            string                              Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    =================================== =================================== ==========================================================================

.. _owinspcurrat:

CurrentRating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*)
    owinsp_id                           integer                             Identifier (assigned by :ref:`owinspdata`). Use unknown.
    owinsp_url                          string                              URL to the page of the branch where the rating for this education_structure was found.
    rating                              string                              Rating awarded by the Onderwijsinspectie [#owinsp]_.
    rating_excerpt                      string                              Excerpt of the rating report.
    rating_valid_since                  date                                Date this rating went into effect.
    =================================== =================================== ==========================================================================

.. _owinsprathist:

HistoricalRating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    date                                date                                Date this rating was awarded.
    education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*)
    rating                              string                              Rating awarded by the Onderwijsinspectie [#owinsp]_.
    =================================== =================================== ==========================================================================

.. _owinspmeta:

Meta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. table::

    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    item_scraped_at                     datetime                            The date and time this branch was scraped from the source.
    scrape_started_at                   datetime                            The date and time the scrape session this item was downloaded in started.
    validated_at                        datetime                            The date and time this item was validated.
    validation_result                   string                              Indication whether the item passed validation.
    =================================== =================================== ======================================================================================================

.. _owinspreport:

Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    date                                date                                Date the report was published by the Onderwijsinspectie [#owinsp]_.
    education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*)
    title                               string                              Title of the report.
    url                                 string                              URL to the full report in PDF.
    =================================== =================================== ==========================================================================

.. [#schoolbestuur] http://nl.wikipedia.org/wiki/Schoolbestuur
.. [#brin] http://nl.wikipedia.org/wiki/BRIN
.. [#edu_in_holland] http://en.wikipedia.org/wiki/Education_in_the_Netherlands#High_school
.. [#denomination] http://en.wikipedia.org/wiki/Education_in_the_Netherlands#General_overview
.. [#cbs] Dutch Bureau of Statistics: http://www.cbs.nl/en-GB/menu/home/default.htm
.. [#provinces] http://en.wikipedia.org/wiki/Dutch_provinces
.. [#zipcodes] http://en.wikipedia.org/wiki/Postal_code#Netherlands
.. [#medezeggenschapsraad] http://nl.wikipedia.org/wiki/Medezeggenschapsraad
.. [#voraad] http://www.vo-raad.nl/
.. [#coc] http://www.vo-raad.nl/dossiers/leermiddelen/gedragscode-schoolkosten
.. [#tevr_stud] http://wiki.schoolvo.nl/mediawiki/index.php/Tevredenheid_leerlingen
.. [#tevr_par] http://wiki.schoolvo.nl/mediawiki/index.php/Tevredenheid_ouders
.. [#wgr_law] http://wetten.overheid.nl/BWBR0003740
.. [#mbo1] http://nl.wikipedia.org/wiki/Middelbaar_beroepsonderwijs#Niveau
.. [#vmbo] http://en.wikipedia.org/wiki/Voorbereidend_middelbaar_beroepsonderwijs
.. [#sectors] http://nl.wikipedia.org/wiki/Vmbo#Sectoren
.. [#profiles] http://nl.wikipedia.org/wiki/Profielen_Tweede_Fase#Profielen
.. [#lwoo] http://nl.wikipedia.org/wiki/Lwoo
.. [#owinsp] http://nl.wikipedia.org/wiki/Inspectie_van_het_Onderwijs_(Nederland)
