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

.. _duodata:

DUO
---------------------------------------------------------------------------------
`Dataportaal DUO <http://data.duo.nl/>`_

.. _schoolvodata:

Vensters voor Verantwoording
---------------------------------------------------------------------------------
vo_branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. table::

    =================================== =================================== ========================================================================================================
    Field                               Type                                Description
    =================================== =================================== ========================================================================================================
    address                             Address                             Address of the branch.
    avg_education_hours_per_student     array of EducationHoursPerStudent   Array of EducationHoursPerStudent, representing how many hours of education were planned for a year, and how many are actually realised.
    avg_education_hours_per_student_url string                              URL to the *Onderwijstijd* page.
    board                               string                              The name of the board of this school.
    board_id                            integer                             Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                           integer                             Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    building_img_url                    string                              URL to a photo of the building of this branch.
    costs                               Costs                               Object representing the costs a parent can expect for this branch.
    costs_url                           string                              URL to the *Onderwijskosten* page.
    education_structures                array                               An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.
    email                               string                              Email address of this branch.
    logo_img_url                        string                              URL to a photo of the logo of the school of this branch.
    municipality                        string                              The name of the municipality this branch is located in.
    municipality_code                   integer                             Identifier (assigned by CBS [#cbs]_) to this municipality.
    name                                string                              Name of the branch of this school.
    parent_satisfaction                 array of ParentSatisfaction         Satisfaction polls of parents.
    parent_satisfaction_url             string                              URL to the *Tevredenheid ouders* page.
    phone                               string                              Unnormalised string representing the phone number of this branch.
    profile                             string                              Short description of the motto of this branch.
    province                            string                              The province [#provinces]_ this branch is situated in.
    schoolkompas_status_id              integer                             Identifier used at http://schoolkompas.nl. Use unknown.
    schoolvo_code                       string                              Identifier used at http://schoolvo.nl. Consists of the board_id, brin and branch_id, separated by dashes. A school page can be accessed at `http://schoolvo.nl/?p_schoolcode=`\ *<schoolvo_code>*.
    schoolvo_id                         integer                             Identifier used at schoolvo internally.
    schoolvo_status_id                  integer                             Use unknown.
    student_satisfaction                array of StudentSatisfaction        Satisfaction polls of students.
    student_satisfaction_url            string                              URL to the *Tevredenheid leerlingen* page.
    website                             string                              URL of the website of the school.
    =================================== =================================== ========================================================================================================

.. _owinspdata:

Onderwijsinspectie
---------------------------------------------------------------------------------
`Inspectierapporten archief <http://www.owinsp.nl/>`_

.. [#schoolbestuur] http://nl.wikipedia.org/wiki/Schoolbestuur
.. [#brin] http://nl.wikipedia.org/wiki/BRIN
.. [#edu_in_holland] http://en.wikipedia.org/wiki/Education_in_the_Netherlands#High_school
.. [#cbs] Dutch Bureau of Statistics: http://www.cbs.nl/en-GB/menu/home/default.htm
.. [#provinces] http://en.wikipedia.org/wiki/Dutch_provinces
