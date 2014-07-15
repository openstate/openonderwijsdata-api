Data
====
The data that is made available through the API originates from different sources: :ref:`duodata`, :ref:`schoolvodata` and the :ref:`owinspdata`. Each of these sources provides different types of data, from school assessments to financial figures. For each source the available fields are described, as well as the data they contain.

The data sources present their data aggregated on different *granularities*: financial data is usually aggregated to the level of the school *board*, whereas the number of students is available for specific locations (*branch*) of a school. In order to represent the data properly, the following entities are defined for different levels of education: *board*, *school*, *branch*. Currently there are two types of education are available, primary and secondary education (respectively in Dutch: *primair onderwijs* or *po* and *voortgezet onderwijs* or *vo*). Examples of the *vo* entities:

**vo_board** (in Dutch: *schoolbestuur*)
    A vo_board represents the school board in secondary education. The school board is responsible for decisions about education provided at their school(s), as well as the school in general [#schoolbestuur]_. For example, the board is responsible for the financial health of its schools. Boards can be responsible for multiple schools.

**vo_school** (in Dutch: *middelbare school*)
    A vo_school represents an institution where secondary education is provided to students. Data regarding the success rate at exams is aggregated at this level. A vo_school is identified by a BRIN, an identifier for schools and related institutions such as universities [#brin]_. A school can have multiple physical locations (*branches*), where for example different levels of education are offered.

**vo_branch** (in Dutch: *afdeling middelbare school*)
    A school can be located at different (geographical) locations. For example, large schools that offer different levels of education [#edu_in_holland]_ often do so at separate buildings. These different departments are represented by a *vo_branch*.

A similar categorisation for schools at the primary level is available.

Additionally, there's data available for the *appropriate education* collaborations (*passend onderwijs*):

**pao_collaboration** (in Dutch: *samenwerkingsverband passend onderwijs*)
    With appropriate education schools can provide education more tailored to students who need extra support. In 2014, responsibility for part of what used to be special education moved to the collaborations for appropriate education.
    
**po_lo_collaboration** (in Dutch: *samenwerkingsverband lichte ondersteuning, primair onderwijs*)
    Before 2014, schools were part of collaborations for *light support*.

Note that many fields in the :ref:`duodata` dataset overlap, as these data is available on all levels.

For some fields the original Dutch term is included, in order to allow the API user to look up the definition of that term at the source collection.

.. _duodata:

DUO
---
DUO publishes many different datasets, each of these datasets has a different "release cycle". Some are published annually, just before the start of the new schoolyear, others are updated on a monthly basis. To group related data we introduce the notion of a "reference year". DUO datasets that are published within the same calendar year are grouped together into a single (vo_board, vo_school or vo_branch) document. For example: DUO published the :ref:`duostdstruct` on October 1, 2012 and :ref:`duostdres` on October 2, 2012, in this case both documents are combined into a single vo_branch document with ``reference_year`` 2012. For the sake of completeness, the exact reference date of the original item is also preserved, for example in the ``student_residences_reference_date`` and ``students_by_structure_reference_date`` attributes.

.. note::

   Currently DUO updates general information (addresses, names, phone numbers, etc.) of educational institutions on a monthly basis. Unfortunately, historical information is not provided. This means that for some reference years the API contains information such as the financial indicators and dropouts of a school, but does not include the address or name. A plausible explanation is that because of mergers or bankruptcies the school no longer exists in recent files.

.. _duovoboard:

vo_board
^^^^^^^^
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
    financial_key_indicators_per_year_reference_date date                                Peiljaar                            Date the financial key indicator source file was published at http://data.duo.nl
    financial_key_indicators_per_year_url            string                                                                  URL to the financial key indicator source file at http://data.duo.nl
    meta                                             :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                                     string                                                                  The name of the municipality this board is located in.
    municipality_code                                integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                             string                                                                  Name of the board.
    phone                                            string                                                                  Phone number of the board.
    reference_year                                   date                                Peiljaar                            Year the boards source file was published
    website                                          string                                                                  URL of the webpage of the board.
    ================================================ =================================== =================================== =============================================================

.. _duovoschool:

vo_school
^^^^^^^^^
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
    dropouts_per_year_reference_date    date                                Peildatum                           Date the dropouts source file was published at http://data.duo.nl.
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
    reference_year                      integer                             Peiljaar                                    Year the schools source file was published.
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
^^^^^^^^^
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
    havo_exam_grades_per_course             array of :ref:`gradespercourse`     Cijfers per vak per jaar            Grades per course per year for the HAVO section of this school.
    havo_exam_grades_reference_date         date
    havo_exam_grades_reference_url          string                                                                  URL to the vmbo exam grades per course source file at http://data.duo.nl/
    meta                                    :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                            string                                                                  The name of the municipality this branch is located in.
    municipality_code                       integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                    string                                                                  Name of the school.
    nodal_area                              string                              Nodaal gebied                       Area defined for the planning of distribution of secondary schools. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
    nodal_area_code                         integer                                                                 Identifier of the nodal_area.
    phone                                   string                                                                  Phone number of the school.
    province                                string                                                                  The province [#provinces]_ this branch is situated in.
    reference_year                          integer                             Peiljaar                            Year the schools source file was published.
    rmc_region                              string                              Rmc-regio                           Area that is used for the coordination of school dropouts. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
    rmc_region_code                         integer                                                                 Identifier of the rmc_region.
    rpa_area                                string                              Rpa-gebied                          Area defined to cluster information on the labour market. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
    rpa_area_code                           integer                                                                 Identifier of the rpa_area.
    student_residences                      :ref:`duostdres`                                                        Array of :ref:`duostdres`, where each item contains the distribution of students from a given municipality over the years in this branch.
    student_residences_reference_date       date                                Peildatum                           Date the student residences source file was published at http://data.duo.nl
    student_residences_url                  string                                                                  URL of the student residences source file.
    students_by_structure                   :ref:`duostdstruct`                                                     Distribution of students by education structure and gender.
    students_by_structure_reference_date    date                                Peildatum                           Date the student per structure source file was published at http://data.duo.nl
    students_by_structure_url               string                                                                  URL of the student by structure source file.
    graduations                             array of :ref:`graduation`          Examenkandidaten en geslaagden      Array of :ref:`graduation` where each item represents a school year. For each year information on the number of passed, failed and candidates is available. A futher breakdown in department and gender is also available.
    graduations_reference_date              date                                Peildatum                           Date the graduations source file was published at http://data.duo.nl
    graduations_url                         string                                                                  URL to the dropouts source file at http://data.duo.nl/
    exam_grades                             array of :ref:`examgrades`          Eindcijfers                         School and central exam grades per education structure and sector.
    exam_grades_reference_date              date                                Peildatum                           Date the exam grades source file was published at http://data/duo.nl/
    exam_grades_url                         string                                                                  URL to the exam grades source file at http://data.duo.nl/
    vmbo_exam_grades_per_course             array of :ref:`gradespercourse`     Cijfers per vak per jaar            Grades per course per year for the VMBO section of this school.
    vmbo_exam_grades_reference_date         date
    vmbo_exam_grades_reference_url          string                                                                  URL to the vmbo exam grades per course source file at http://data.duo.nl/
    vwo_exam_grades_per_course              array of :ref:`gradespercourse`     Cijfers per vak per jaar            Grades per course per year for the VWO section of this school.
    vwo_exam_grades_reference_date          date
    vwo_exam_grades_reference_url           string                                                                  URL to the vmbo exam grades per course source file at http://data.duo.nl/
    website                                 string                                                                  Website of this school.
    wgr_area                                string                              Wgr-gebied                          Cluster of municipalities per collaborating region according to the "Wet gemeenschappelijke regelingen" [#wgr_law]_. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied.
    wgr_area_code                           integer                                                                 Identifier of the wgr_area.
    ======================================= =================================== =================================== ======================================================================

.. _duopoboard:

po_board
^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 05. Bevoegde gezagen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/po_adressen05.asp>`_

.. table::
    =================================================== =================================== =================================== =============================================================
    Field                                               Type                                Original term                       Description
    =================================================== =================================== =================================== =============================================================
    address                                             :ref:`duoaddress`                                                       Address of this board.
    administrative_office_id                            integer                             Administratiekantoor                Identifier (assigned by :ref:`duodata`) for the accountancy firm that manages this board finances.
    board_id                                            integer                             Bevoegd gezag nummer                Identifier (assigned by :ref:`duodata`) of the board of this branch.
    correspondence_address                              :ref:`duoaddress`                                                       Correspondence address of this board.
    denomination                                        string                              Denominatie                         In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    edu_types                                           array of :ref:`edutypes`                                                Array of :ref:`edutypes`, where each item shows how many pupils are in the education types po, spo, so or svo in this board's schools.
    edu_types_reference_date                            2013-06-22                          Peiljaar                            Date the source file was published at http://data.duo.nl
    edu_types_reference_url                             string                                                                  URL to the source file at http://data.duo.nl
    financial_key_indicators_per_year                   array of :ref:`finindicator`                                            Array of :ref:`finindicator`, where each item represents a set of key financial indicators for a given year.
    financial_key_indicators_per_year_reference_date    date                                Peiljaar                            Date the financial key indicator source file was published at http://data.duo.nl
    financial_key_indicators_per_year_url               string                                                                  URL to the financial key indicator source file at http://data.duo.nl
    meta                                                :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                                        string                              Gemeente                            The name of the municipality this board is located in.
    municipality_code                                   integer                             Gemeentenummer                      Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                                string                              Bevoegd gezag naam                  Name of the board.
    phone                                               string                              Telefoonnummer                      Phone number of the board.
    reference_year                                      date                                Peiljaar                            Year the boards source file was published
    website                                             string                                                                  URL of the webpage of the board.
    =================================================== =================================== =================================== =============================================================

.. _duoposchool:

po_school
^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 01. Hoofdvestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/hoofdvestigingen.asp>`_

.. table::
    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    address                             :ref:`duoaddress`                                                       Address of this school.
    board_id                            integer                             Bevoegd gezag nummer                Identifier (assigned by :ref:`duodata`) of the board of this school.
    brin                                string                                                                  "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    corop_area                          string                              COROP-gebied                        A COROP area in the Netherlands is a region consisting of several municipalities, and is primarily used by research institutions to present statistical data. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
    corop_area_code                     integer                                                                 Identifier of the corop_area.
    correspondence_address              :ref:`duoaddress`                                                       Correspondence address of this school.
    denomination                        string                                                                  In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_area                      string                              Onderwijsgebied                     Education areas are aggregations of nodal areas based on regional origins and destinations of students in secondary education. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
    education_area_code                 integer                                                                 Identifier of the education_area.
    meta                                :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                        string                                                                  The name of the municipality this branch is located in.
    municipality_code                   integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                string                                                                  Name of the school.
    nodal_area                          string                              Nodaal gebied                       Area defined for the planning of distribution of secondary schools. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
    nodal_area_code                     integer                                                                 Identifier of the nodal_area.
    phone                               string                                                                  Phone number of the school.
    province                            string                                                                  The province [#provinces]_ this branch is situated in.
    reference_year                      integer                             Peiljaar                            Year the schools source file was published.
    rmc_region                          string                              Rmc-regio                           Area that is used for the coordination of school dropouts. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
    rmc_region_code                     integer                                                                 Identifier of the rmc_region.
    rpa_area                            string                              Rpa-gebied                          Area defined to cluster information on the labour market. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
    rpa_area_code                       integer                                                                 Identifier of the rpa_area.
    website                             string                                                                  Website of this school.
    wgr_area                            string                              Wgr-gebied                          Cluster of municipalities per collaborating region according to the "Wet gemeenschappelijke regelingen" [#wgr_law]_. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied.
    wgr_area_code                       integer                                                                 Identifier of the wgr_area.
    =================================== =================================== =================================== ==========================================================================

.. _duopobranch:

po_branch
^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 03. Alle vestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/vest_bo.asp>`_

.. table::
    =================================================== =================================== =================================== ======================================================================
    Field                                               Type                                Original term                       Description
    =================================================== =================================== =================================== ======================================================================
    address                                             :ref:`duoaddress`                                                       Address of this branch.
    ages_per_branch_by_student_weight                   dict of :ref:`agesbystudentweight`                                      The number of children for each age on this branch by student weight (keys: *student_weight_0.0*, *student_weight_0.3* and *student_weight_1.2*).
    ages_per_branch_by_student_weight_reference_date    date                                                                    Date the ages per branch by student weight source file was published at http://data.duo.nl
    ages_per_branch_by_student_weight_reference_url     string                                                                  URL of the ages per branch by student weight source file.
    board_id                                            integer                                                                 Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                                           integer                                                                 Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                                string                                                                  "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    corop_area                                          string                              COROP-gebied                        A COROP area in the Netherlands is a region consisting of several municipalities, and is primarily used by research institutions to present statistical data. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
    corop_area_code                                     integer                                                                 Identifier of the corop_area.
    correspondence_address                              :ref:`duoaddress`                                                       Correspondence address of this branch.
    denomination                                        string                                                                  In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_area                                      string                              Onderwijsgebied                     Education areas are aggregations of nodal areas based on regional origins and destinations of students in secondary education. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
    education_area_code                                 integer                                                                 Identifier of the education_area.
    meta                                                :ref:`duometa`                                                          Metadata, such as date of scrape and whether this item passed validation.
    municipality                                        string                                                                  The name of the municipality this branch is located in.
    municipality_code                                   integer                                                                 Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                                string                                                                  Name of the school.
    nodal_area                                          string                              Nodaal gebied                       Area defined for the planning of distribution of secondary schools. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
    nodal_area_code                                     integer                                                                 Identifier of the nodal_area.
    phone                                               string                                                                  Phone number of the school.
    province                                            string                                                                  The province [#provinces]_ this branch is situated in.
    student_residences                                  array of :ref:`dustrespo`                                               The number of pupils in this branch living in certain zipcodes by ages.
    student_residences_reference_date                   date                                Peiljaar                            Date the source file was published at http://data.duo.nl
    student_residences_reference_url                    string                                                                  URL of the source file.
    reference_year                                      integer                             Peiljaar                            Year the schools source file was published.
    rmc_region                                          string                              Rmc-regio                           Area that is used for the coordination of school dropouts. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
    rmc_region_code                                     integer                                                                 Identifier of the rmc_region.
    rpa_area                                            string                              Rpa-gebied                          Area defined to cluster information on the labour market. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
    rpa_area_code                                       integer                                                                 Identifier of the rpa_area.
    website                                             string                                                                  Website of this school.
    students_by_origin                                  array of :ref:`students_by_origin`                                      Number of studentes born in countries other than The Netherlands by country. Only availabe in 2009 as collecting of this data has been stopped since 2010.
    students_by_origin_reference_date                   date                                 Peiljaar                           Date the source file was published at http://data.duo.nl
    students_by_origin_reference_url                    string                                                                  URL of the source file.
    student_weights_per_branch                          array of :ref:`studentweights`                                          The number of children per student weight (0.0, 0.3 or 1.2), school weight and impulse area data for each branch.
    student_weights_per_branch_reference_date           date                                                                    Date the source file was published at http://data.duo.nl
    student_weights_per_branch_reference_url            string                                                                  URL of the source file.
    wgr_area                                            string                              Wgr-gebied                          Cluster of municipalities per collaborating region according to the "Wet gemeenschappelijke regelingen" [#wgr_law]_. *Source:* http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied.
    wgr_area_code                                       integer                                                                 Identifier of the wgr_area.
    =================================================== =================================== =================================== ======================================================================

.. _duopaocollaboration:

paocollaboration
^^^^^^^^^^^^^^^^
**Source:** `Passend onderwijs - Adressen - 01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/passendow/Adressen/Adressen/passend_po_1.asp>`
.. table::
    ================================================ =================================== =================================== =============================================================
    Field                                            Type                                Original term                       Description
    ================================================ =================================== =================================== =============================================================
    collaboration_id                                 string                              Administratienummer                 Identification number of collaboration                 
    address                                          :ref:`duoaddress`                                                       Address of this collaboration.
    correspondence_address                           :ref:`duoaddress`                                                       Correspondence address of this collaboration.
    ================================================ =================================== =================================== =============================================================


.. _duoaddress:

Address
^^^^^^^
**Source:** `Primair onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/default.asp>`_

**Source:** `Voortgezet onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/default.asp>`_

**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    address_components                  array of :ref:`duoaddresscomponent` Array of :ref:`duoaddresscomponent`, where each item represents a classification of components of the address, such as municipality, postal code, etc.
    formatted_address                   string                              Normalised address as returned by the BAG42 geocoding API [#bag42geo]_.
    city                                string                              Name of the city or village this branch is located.
    street                              string                              Street name and number of the address of this branch.
    zip_code                            string                              Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    geo_location                        :ref:`duogeoloc`                    Latitude/longitude coordinates of this address.
    geo_viewport                        :ref:`duogeoviewport`               Latitude/longitude coordinates of the viewport for this address
    =================================== =================================== ==========================================================================

.. _duoaddresscomponent:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    long_name                           string                              Full name of this component. (*i.e. "Nederland"*)
    short_name                          string                              Abbreviated form (if applicable) of the long_name. (*i.e. "NL"*)
    types                               array                               Array containing classifications of this component.
    =================================== =================================== ==========================================================================

AgesByStudentWeight
^^^^^^^^^^^^^^^^^^^
This dict has three keys *student_weight_0.0*, *student_weight_0.3* and *student_weight_1.2*, the weights are based on the pupil's parents level of education [#weight]_.

**Source:** `Primair onderwijs - Leerlingen - 03. Leerlingen basisonderwijs naar leerlinggewicht en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen3.asp>`_

.. table::
    =================================== ================ ==========================================================================
    Field                               Type             Description
    =================================== ================ ==========================================================================
    age_3                               integer          Number of children at age 3 in the key's weight category at this branch.
    age_4                               integer          Number of children at age 4 in the key's weight category at this branch.
    age_5                               integer          Number of children at age 5 in the key's weight category at this branch.
    age_6                               integer          Number of children at age 6 in the key's weight category at this branch.
    age_7                               integer          Number of children at age 7 in the key's weight category at this branch.
    age_8                               integer          Number of children at age 8 in the key's weight category at this branch.
    age_9                               integer          Number of children at age 9 in the key's weight category at this branch.
    age_10                              integer          Number of children at age 10 in the key's weight category at this branch.
    age_11                              integer          Number of children at age 11 in the key's weight category at this branch.
    age_12                              integer          Number of children at age 12 in the key's weight category at this branch.
    age_13                              integer          Number of children at age 13 in the key's weight category at this branch.
    age_14                              integer          Number of children at age 14 in the key's weight category at this branch.
    =================================== ================ ==========================================================================

.. _dropout:

Dropout
^^^^^^^
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

.. _edutypes:

EduTypes
^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen7.asp>`_

.. table::
    =========== ========== ================ =============================
    Field       Type       Original term    Description
    =========== ========== ================ =============================
    po          integer    Bao              Primary education.
    so          integer    So               Special education.
    spo         integer    Sbao             Special primary education.
    vso         integer    Svo              Special secondary education.
    =========== ========== ================ =============================

.. _examgrades:

ExamGrades
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 07. Geslaagden, gezakten en gemiddelde examencijfers per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen7.asp>`_

.. table::
    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    sector                              string                              Afdeling                            E.g. "Cultuur en Maatschappij"
    education_structure                 string                              Onderwijstype VO                    E.g. "HAVO"
    candidates                          integer                                                                 The total number of exam candidates for this school year
    passed                              integer                                                                 The number of candidates that graduated
    failed                              integer                                                                 The number of candidates that did not graduate
    avg_grade_school_exam               float                               Gemiddeld cijfer schoolexamen
    avg_grade_central_exam              float                               Gemiddeld cijfer centraal examen
    avg_final_grade                     float                               Gemiddeld cijfer cijferlijst
    =================================== =================================== =================================== ==========================================================================

.. _agesbystudentweight:

.. _finindicator:

FinancialIndicator
^^^^^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Financiën - 15. Kengetallen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Financien/Jaarrekeninggegevens/Kengetallen.asp>`_

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

.. _gradespercourse:

GradesPerCourse
^^^^^^^^^^^^^^^
**Source:** `08. Examenkandidaten vmbo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp>`_

**Source:** `09. Examenkandidaten havo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp>`_

**Source:** `10. Examenkandidaten vwo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp>`_

.. table::
    ======================================================= ========================== ========================= ======================================================================
    Field                                                   Type                       Original term             Description
    ======================================================= ========================== ========================= ======================================================================
    amount_of_central_exams                                 integer                                              The amount of central exams [#centralexams]_ conducted for this branch
    amount_of_central_exams_counting_for_diploma            integer                                              The amount of central exams [#centralexams]_ conducted at this branch that count for a diploma
    amount_of_school_exams_with_grades                      integer                                              The amount of school exams [#schoolexams]_ conducted at this branch that are graded
    amount_of_school_exams_with_grades_counting_for_diploma integer                                              The amount of school exams [#schoolexams]_ conducted at this branch that are graded and count for a diploma
    amount_of_school_exams_with_rating                      integer                                              Not all school exams are graded, but are rated as "onvoldoende" (insufficient), "voldoende" (sufficient) and "goed" (good). This number denotes the amount of school exams that have rating, rather then a grade
    amount_of_school_exams_with_rating_counting_for_diploma integer                                              The amount of school exams that are rated rather than graded that count for a diploma
    average_grade_overall                                   float                                                The final average grade. This average is based on the grades on the final list of grades
    avg_grade_central_exams                                 float                                                The average grade for central exams.
    avg_grade_central_exams_counting_for_diploma            float                                                The average grade of central exams that count toward a diploma
    avg_grade_school_exams                                  float                                                The average grade for school exams
    avg_grade_school_exams_counting_for_diploma             float                                                The average grade of school exams that count toward a diploma
    course_abbreviation                                     string                                               Abbreviation used by DUO that denotes the course
    course_identifier                                       string                                               Identifier used by DUO for a course
    course_name                                             string                                               Verbose, human-readable name for the course
    education_structure                                     string                                               Level of education [#edu_in_holland]_
    ======================================================= ========================== ========================= ======================================================================


.. _graduation:

Graduation
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_

.. table::
    ==================== ===================================== =================================== ======================================================================
    Field                Type                                  Original term                       Description
    ==================== ===================================== =================================== ======================================================================
    year                 string                                Schooljaar                          The school year the graduations applay to
    candidates           integer                                                                   The total number of exam candidates for this school year
    passed               integer                                                                   The number of candidates that graduated
    failed               integer                                                                   The number of candidates that did not graduate
    per_department       array of :ref:`graduationdepartment`                                      Breakdown of the candidate and graduation results by deparment and gender
    ==================== ===================================== =================================== ======================================================================


.. _graduationdepartment:

GraduationPerDepartment
^^^^^^^^^^^^^^^^^^^^^^^
Belongs to :ref:`graduationdepartment`.

**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_

.. table::
    =================== =================================== =================================== ======================================================================
    Field               Type                                Original term                       Description
    =================== =================================== =================================== ======================================================================
    education_structure string                              ONDERWIJSTYPE VO
    inspectioncode      string
    department          string                              OPLEIDINGSNAAM
    candidates          Object                                                                  The distribution of genders of candidates participating in final exams
    - unknown           integer                                                                 The amount of candidates of which the gender is not known
    - male              integer                                                                 The amount of male participants
    - female            integer                                                                 The amount of female participants
    passed              Object                                                                  The distribution of genders of candidates that passed the final exams
    - unknown           integer
    - male              integer
    - female            integer
    failed              Object                                                                  The distribution of genders of candidates that failed the final exams
    - unknown           integer
    - male              integer
    - female            integer
    =================== =================================== =================================== ======================================================================

.. _duogeoloc:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    lat                                 float                               Latitude
    lon                                 float                               Longitude
    =================================== =================================== ==========================================================================

.. _duogeoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    northeast                           :ref:`duogeoloc`                    Coordinates of the north-east coordinate of the viewport.
    southwest                           :ref:`duogeoloc`                    Coordinates of the south-west coordinate of the viewport.
    =================================== =================================== ==========================================================================

.. _duometa:

Meta
^^^^
**Source:** `OpenOnderwijs scrapers <http://api.openonderwijsdata.nl/>`_

.. table::
    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    item_scraped_at                     datetime                            The date and time this branch was scraped from the source.
    scrape_started_at                   datetime                            The date and time the scrape session this item was downloaded in started.
    validated_at                        datetime                            The date and time this item was validated.
    validation_result                   string                              Indication whether the item passed validation.
    =================================== =================================== ======================================================================================================

.. _dustrespo:

StudentResidences
^^^^^^^^^^^^^^^^^
Number of pupils per age group (up to 25, as special education is included).

**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen11.asp>`_

.. table::
    ========= ========================== ================== ==========================================================================
    Field     Type                       Original term      Description
    ========= ========================== ================== ==========================================================================
    ages      array of :ref:`duostpores`
    zip_code  string                     Postcode           The zip code where these pupils live.
    ========= ========================== ================== ==========================================================================

.. _duostpores:

StudentResidence
^^^^^^^^^^^^^^^^

.. table::
    ========= ========================== ================== ==========================================================================
    Field     Type                       Original term      Description
    ========= ========================== ================== ==========================================================================
    age       integer                                       Age group
    students  integer                                       Amount of students
    ========= ========================== ================== ==========================================================================

.. _students_by_origin:

StudentsByOrigin
^^^^^^^^^^^^^^^^
Number of students born in countries other than The Netherlands, by country.

**Source:** `Primair onderwijs - Leerlingen - 09. Leerlingen basisonderwijs met een niet-Nederlandse achtergrond naar geboorteland <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen9.asp>`_

.. table::
    =================================== ================= ===================================
    Field                               Type              Description
    =================================== ================= ===================================
    country                             string            Country students originated from
    students                            integer           The amount of students originating form this country at this school
    =================================== ================= ===================================

.. _duostdres:

StudentResidence
^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 01. Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp>`_

.. table::
    =================================== ====================== ==========================================================================
    Field                               Type                   Description
    =================================== ====================== ==========================================================================
    department                          string                 Optional. Department of a vmbo track.
    education_name                      string                 Name of the education programme.
    education_structure                 string                 Level of education [#edu_in_holland]_.
    element_code                        integer                Unknown.
    lwoo                                boolean                Indicates whether this sector supports "Leerwegondersteunend onderwijs", for students who need additional guidance [#lwoo]_.
    vmbo_sector                         string                 Vmbo sector [#sectors]_.
    year_1                              mapping                Distribution of male and female students for year 1.
    year_2                              mapping                Distribution of male and female students for year 2.
    year_3                              mapping                Distribution of male and female students for year 3.
    year_4                              mapping                Distribution of male and female students for year 4.
    year_5                              mapping                Distribution of male and female students for year 5.
    year_6                              mapping                Distribution of male and female students for year 6.
    =================================== ====================== ==========================================================================

.. _studentweights:

StudentWeights
^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 01. Leerlingen basisonderwijs naar leerlinggewicht en per vestiging het schoolgewicht en impulsgebied <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen1.asp>`_

.. table::
    =================================== =================================== =================================== ==========================================================================
    Field                               Type                                Original term                       Description
    =================================== =================================== =================================== ==========================================================================
    impulse_area                        boolean                             Impulsgebied                        True if the branch is located in a so-called impulse area, which is an zipcode area with many families with low income or welfare. In if this is the case the branch gets extra money for each pupil.
    school_weight                       integer                             Schoolgewicht                       Based on the student weights and results in extra money for the branch.
    student_weight_0.0                  integer                                                                 Number of pupils who's parents don't fall into the weight 0.3 or 1.2 categories.
    student_weight_0.3                  integer                                                                 Number of pupils who's both parents didn't get education beyond lbo/vbo, 'praktijkonderwijs' or vmbo 'basis- of kaderberoepsgerichte leerweg' [#weight]_.
    student_weight_1.2                  integer                                                                 Number of pupils who's parents (one or both) didn't get education beyond 'basisonderwijs' or (v)so-zmlk [#weight]_.
    =================================== =================================== =================================== ==========================================================================

.. _schoolvodata:

Vensters voor Verantwoording
----------------------------
`Vensters voor Verantwoording <http://schoolvo.nl/>`_ provides VO schools with a platform where they can share data on their performance with the public. The data described here is currently **not** available to the public through the `OpenOnderwijs API <http://api.openonderwijsdata.nl/>`_.

vo_branch
^^^^^^^^^
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
^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    address_components                  array of :ref:`schoolvoaddrcomp`    Array of :ref:`schoolvoaddrcomp`, where each item represents a classification of components of the address, such as municipality, postal code, etc.
    formatted_address                   string                              Normalised address as returned by the BAG42 geocoding API [#bag42geo]_.
    city                                string                              Name of the city or village this branch is located.
    street                              string                              Street name and number of the address of this branch.
    zip_code                            string                              Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    geo_location                        :ref:`schoolvo_coordinates`         Latitude/longitude coordinates of this address.
    geo_viewport                        :ref:`schoolvoviewport`             Latitude/longitude coordinates of the viewport for this address
    =================================== =================================== ==========================================================================

.. _schoolvoaddrcomp:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    long_name                           string                              Full name of this component. (*i.e. "Nederland"*)
    short_name                          string                              Abbreviated form (if applicable) of the long_name. (*i.e. "NL"*)
    types                               array                               Array containing classifications of this component.
    =================================== =================================== ==========================================================================

.. _costs:

Costs
^^^^^

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
^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^

.. table::
    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    hours_planned                       integer                             Hours of education planned by the school council [#medezeggenschapsraad]_ for the past year.
    hours_realised                      integer                             Hours of education realised at the school [#medezeggenschapsraad]_ for the past year.
    structure                           string                              The structure these hours apply to (*vbmo-t, havo, vwo, ...*)
    =================================== =================================== ======================================================================================================

.. _schoolvo_coordinates:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    lat                                 float                               Latitude
    lon                                 float                               Longitude
    =================================== =================================== ==========================================================================

.. _schoolvoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    northeast                           :ref:`schoolvo_coordinates`         Coordinates of the north-east coordinate of the viewport.
    southwest                           :ref:`schoolvo_coordinates`         Coordinates of the south-west coordinate of the viewport.
    =================================== =================================== ==========================================================================

.. _indicator:

Indicator
^^^^^^^^^

.. table::
    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    grade                               float                               The average grade student/parents awarded this indicator.
    indicator                           string                              The indicator.
    =================================== =================================== ======================================================================================================

.. _schoolvometa:

Meta
^^^^

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
^^^^^^^^^^^^

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
------------------
The Inspectie voor het Onderwijs [#owinsp]_ is tasked with inspecting Dutch schools. Since 1997, they are required to publish reports on their findings when inspecting schools.

.. _owinspdatavobranch:

vo_branch
^^^^^^^^^
.. table::
    ======================================================= =================================== ========================================================================================================
    Field                                                   Type                                Description
    ======================================================= =================================== ========================================================================================================
    address                                                 :ref:`owinspaddress`                Address of this branch
    advice_structure_third_year                             array of :ref:`advice_struct_3`     An array of :ref:`advice_struct_3`, representing the distribution of the primary school advices students have in the third year of their education.
    board                                                   string                              The name of the board of this school.
    board_id                                                integer                             Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                                               integer                             Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                                    string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    composition_first_year                                  :ref:`first_year_comp`              Composition of the first year of this school, distinguishing between *combined* (students from different education structures partaking in the same courses) and *categorical* (percentage of students from the same education structures).
    current_ratings                                         array of :ref:`owinspcurrat`        Array of :ref:`owinspcurrat`, where each item represents the current rating of the Onderwijsinspectie [#owinsp]_.
    denomination                                            string                              In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    education_structures                                    array                               An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    exam_average_grades                                     array of :ref:`exam_avg_grades`     Array of :ref:`exam_avg_grades`, showing the average exam grade per course group.
    exam_participation_per_profile                          array of :ref:`exam_part_prof`      Array of :ref:`exam_part_prof`, containing the distribution of sectors (VMBO) and profiles (HAVO/VWO) in students participating in exams.
    first_years_performance                                 :ref:`first_year_perf`              Description of the performance of the school's "onderbouw" (first years).
    meta                                                    :ref:`owinspmeta`                   Metadata, such as date of scrape and whether this item passed validation.
    name                                                    string                              Name of this branch.
    performance_assessments                                 array of :ref:`perf_ass`            Array of :ref:`perf_ass`, indicating the "Opbrengstenoordeel", a rating given by the Inspectie to each school, based on the performance in the first years ("onderbouw"), final years ("bovenbouw"), grades of the central examinations and the three year average of the difference between "schoolexamens" and central examinations grades.
    rating_history                                          array of :ref:`owinsprathist`       Array of :ref:`owinsprathist`, where each item represents a rating the Onderwijsinspectie [#owinsp]_ awarded to this branch.
    reports                                                 array of :ref:`owinspreport`        Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.
    result_card_url                                         string                              URL to the result card ("opbrengstenkaart") of this branch.
    students_from_third_year_to_graduation_without_retaking array of :ref:`straight_grad`       Array of :ref:`straight_grad`, showing the percentage of students that go on to graduation from their third year without retaking a year, per education structure.
    students_in_third_year_without_retaking                 array of :ref:`3yearnoretakes`      Array of :ref:`3yearnoretakes`, showing the percentage of students that reach their third year without retaking a year.
    website                                                 string                              Website of this branch (optional).
    ======================================================= =================================== ========================================================================================================

.. _owinspdatapobranch:

po_branch
^^^^^^^^^
.. table::
    ======================================================= =================================== ========================================================================================================
    Field                                                   Type                                Description
    ======================================================= =================================== ========================================================================================================
    address                                                 :ref:`owinspaddress`                Address of this branch
    brin                                                    string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    current_ratings                                         :ref:`owinspcurrat`                 :ref:`owinspcurrat`, which represents the current rating of the Onderwijsinspectie [#owinsp]_.
    denomination                                            string                              In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.
    meta                                                    :ref:`owinspmeta`                   Metadata, such as date of scrape and whether this item passed validation.
    name                                                    string                              Name of this branch.
    rating_history                                          array of :ref:`owinsprathist`       Array of :ref:`owinsprathist`, where each item represents a rating the Onderwijsinspectie [#owinsp]_ awarded to this branch.
    reports                                                 array of :ref:`owinspreport`        Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.
    website                                                 string                              Website of this branch (optional).
    ======================================================= =================================== ========================================================================================================

.. _owinspaddress:

Address
^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    address_components                  array of :ref:`owinspaddrcomp`      Array of :ref:`owinspaddrcomp`, where each item represents a classification of components of the address, such as municipality, postal code, etc.
    formatted_address                   string                              Normalised address as returned by the BAG42 geocoding API [#bag42geo]_.
    city                                string                              Name of the city or village this branch is located.
    street                              string                              Street name and number of the address of this branch.
    zip_code                            string                              Zip code of the address of this branch. A Dutch zip code consists of four digits, a space and two letters (*1234 AB*) [#zipcodes]_. For normalisation purposes, the whitespace is removed.
    geo_location                        :ref:`owinsp_coordinates`           Latitude/longitude coordinates of this address.
    geo_viewport                        :ref:`owinspgeoviewport`            Latitude/longitude coordinates of the viewport for this address
    =================================== =================================== ==========================================================================

.. _owinspaddrcomp:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    long_name                           string                              Full name of this component. (*i.e. "Nederland"*)
    short_name                          string                              Abbreviated form (if applicable) of the long_name. (*i.e. "NL"*)
    types                               array                               Array containing classifications of this component.
    =================================== =================================== ==========================================================================

.. _exam_avg_grades:

AverageExamGrades
^^^^^^^^^^^^^^^^^
.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    grade                               float                               The average exam grade.
    compared_performance                integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
    education_structure                 string                              Level of education [#edu_in_holland]_
    name                                string                              The name of the course group this grade applies to.
    =================================== =================================== ==========================================================================

.. _owinspcurrat:

CurrentRating
^^^^^^^^^^^^^
.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*). **This value is optional**: as :ref:`owinspdatapobranch` do not have education structures, only :ref:`owinspdatavobranch` have this value.
    owinsp_id                           integer                             Identifier (assigned by :ref:`owinspdata`). Use unknown.
    owinsp_url                          string                              URL to the page of the branch where the rating for this education_structure was found.
    rating                              string                              Rating awarded by the Onderwijsinspectie [#owinsp]_.
    rating_excerpt                      string                              Excerpt of the rating report.
    rating_valid_since                  date                                Date this rating went into effect.
    =================================== =================================== ==========================================================================

.. _exam_part_prof:

ExamParticipationPerProfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::
    ========================================= =================================== ==========================================================================
    Field                                     Type                                Description
    ========================================= =================================== ==========================================================================
    sector                                    string                              The sector or profile, depending on the education structure.
    percentage                                float                               Percentage of students participating in an exam with this sector of profile.
    education_structure                       string                              The education structure [#edu_in_holland]_ this sector or profile belongs to.
    ========================================= =================================== ==========================================================================

.. _first_year_comp:

FirstYearComposition
^^^^^^^^^^^^^^^^^^^^
.. table::
    ========================================= =================================== ==========================================================================
    Field                                     Type                                Description
    ========================================= =================================== ==========================================================================
    percentage_student_combined_education     float                               Percentage of students in combined education (following multiple kinds of education)
    percentage_student_categorical_education  float                               Percentage of students in categorical education (following one kind of education)
    combined_education_structures             array of strings                    Array containing strings representing education structures that have students following *combined* education.
    categorical_education_structures          array of strings                    Array containing strings representing education structures that have students following *categorical* education.
    ========================================= =================================== ==========================================================================

.. _first_year_perf:

FirstYearPerformance
^^^^^^^^^^^^^^^^^^^^
.. table::
    ========================================= =================================== ==========================================================================
    Field                                     Type                                Description
    ========================================= =================================== ==========================================================================
    ratio                                     float                               Index describing the change of the first years performance. The starting date for this index is not known.
    compared_performance                      integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
    compared_performance_category             string                              String describing to which education structure (group) this school's first years are compared.
    ========================================= =================================== ==========================================================================

FirstYearsPerformance

.. _owinsp_coordinates:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    lat                                 float                               Latitude
    lon                                 float                               Longitude
    =================================== =================================== ==========================================================================

.. _owinspgeoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    northeast                           :ref:`owinsp_coordinates`           Coordinates of the north-east coordinate of the viewport.
    southwest                           :ref:`owinsp_coordinates`           Coordinates of the south-west coordinate of the viewport.
    =================================== =================================== ==========================================================================

.. _owinsprathist:

HistoricalRating
^^^^^^^^^^^^^^^^
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
^^^^

.. table::
    =================================== =================================== ======================================================================================================
    Field                               Type                                Description
    =================================== =================================== ======================================================================================================
    item_scraped_at                     datetime                            The date and time this branch was scraped from the source.
    scrape_started_at                   datetime                            The date and time the scrape session this item was downloaded in started.
    validated_at                        datetime                            The date and time this item was validated.
    validation_result                   string                              Indication whether the item passed validation.
    =================================== =================================== ======================================================================================================

.. _perf_ass:

PerformanceAssessments
^^^^^^^^^^^^^^^^^^^^^^

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    education_structure                 string                              The structure this assessment applies to (*vbmo-t, havo, vwo, ...*)
    performance_assessment              string                              String describing the assessment. Can have a value "voldoende" (adequate), "onvoldoende" (inadequate), "van 1 jaar gegevens" (data for only 1 year available) or "geen oordeel/onvoldoende gegevens" (no assessment/not enough data).
    =================================== =================================== ==========================================================================

.. _advice_struct_3:

PrimarySchoolAdvices
^^^^^^^^^^^^^^^^^^^^

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    primary_school_advices              Array of :ref:`advice_struct_comp`  Array of :ref:`advice_struct_comp`, containing the distribution of primary school advices of students in the third year of their education.
    education_structure                 string                              String that represents the level of education [#edu_in_holland]_ the primary school advice distribution applies to.
    =================================== =================================== ==========================================================================

.. _advice_struct_comp:

PrimarySchoolAdvice
^^^^^^^^^^^^^^^^^^^

.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    advice                              string                              String that represents the level of education [#edu_in_holland]_ the primary school recommended the student upon leaving primary education.
    percentage_of_students              float                               Percentage of students with this advice in the third year of their education.
    =================================== =================================== ==========================================================================

.. _owinspreport:

Report
^^^^^^
.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    date                                date                                Date the report was published by the Onderwijsinspectie [#owinsp]_.
    education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*)
    title                               string                              Title of the report.
    url                                 string                              URL to the full report in PDF.
    =================================== =================================== ==========================================================================

.. _straight_grad:

StraightToGraduation
^^^^^^^^^^^^^^^^^^^^
.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    education_structure                 string                              Level of education [#edu_in_holland]_
    percentage                          float                               Percentage of all students in this education structure that graduate without retaking any year between their third and their final year.
    compared_performance                integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
    =================================== =================================== ==========================================================================

.. _3yearnoretakes:

StraightToThirdYear
^^^^^^^^^^^^^^^^^^^
.. table::
    =================================== =================================== ==========================================================================
    Field                               Type                                Description
    =================================== =================================== ==========================================================================
    education_structure                 string                              Level of education [#edu_in_holland]_
    percentage                          float                               Percentage of all students in this education structure that reach their third year without retaking any year between their first and their third year.
    =================================== =================================== ==========================================================================

**Footnotes**

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
.. [#bag42geo] http://calendar42.com/bag42/
.. [#centralexams] http://nl.wikipedia.org/wiki/Centraal_examen
.. [#schoolexams] http://nl.wikipedia.org/wiki/Schoolexamen
.. [#weight] http://www.rijksoverheid.nl/onderwerpen/leerachterstand/vraag-en-antwoord/wat-is-de-gewichtenregeling-in-het-basisonderwijs.html
