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

For some fields the original Dutch term is included, in order to allow the API user to look up the definition of that term at the source collection.

.. _duodata:

DUO
---------------------------------------------------------------------------------
.. _duovoboard:

vo_board
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
    financial_key_indicators_per_year_url            string                                                                  URL to the financial key indicator  source file at http://data.duo.nl
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
.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    =================================== =================================== =================================== ==========================================================================

.. _duovobranch:

vo_branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    =================================== =================================== =================================== ==========================================================================

.. _duoaddress:

Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    city                                string                                                                  Name of the city or village this branch is located.
    street                              string                                                                  Street name and number of the address of this branch.
    zip_code                            string                                                                  Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    =================================== =================================== =================================== ==========================================================================

.. _finindicator:

FinancialIndicator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    =================================== =================================== =================================== ==========================================================================

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
    other_costs                         string                              Indication whether parents should expect additional costs, other than the costs mentioned here. Value is usually "Ja" or "Nee".
    year                                string                              String representation of the years these costs apply to.
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
    =================================== =================================== ========================================================================================================



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
