
Data
====
The data that is made available through the API now originates only from :ref:`duodata`. For each source the available fields are described, as well as the data they contain.

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

.. _`COROP-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
.. _`Onderwijsgebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
.. _`Nodaal gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
.. _`Rmc-regio`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
.. _`Rpa-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
.. _`Wgr-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied
.. _`Indicatie Special Basis Onderwijs`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Indicatie%20speciaal%20onderwijs
.. _`Cluster`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Cluster


.. _duo-DuoPoBoard:

DuoPoBoard
^^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 05. Bevoegde gezagen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/po_adressen05.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoPoBoard.csv

.. _duo-DuoPoBranch:

DuoPoBranch
^^^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 03. Alle vestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/vest_bo.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoPoBranch.csv

.. _duo-DuoPoSchool:

DuoPoSchool
^^^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 01. Hoofdvestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/hoofdvestigingen.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoPoSchool.csv

.. _duo-DuoVoBoard:

DuoVoBoard
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 03. Adressen hoofdbesturen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/besturen.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoVoBoard.csv

.. _duo-DuoVoBranch:

DuoVoBranch
^^^^^^^^^^^
 **Source:** `Voortgezet onderwijs - Adressen - 02. Adressen alle vestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/vestigingen.asp>`_ 

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoVoBranch.csv

.. _duo-DuoVoSchool:

DuoVoSchool
^^^^^^^^^^^
 **Source:** `Voortgezet onderwijs - Adressen - 01. Adressen hoofdvestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/hoofdvestigingen.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoVoSchool.csv

.. _duo-DuoPaoCollaboration:

DuoPaoCollaboration
^^^^^^^^^^^^^^^^^^^
**Source:** `Passend onderwijs - Adressen - 01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/passendow/Adressen/Adressen/passend_po_1.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoPaoCollaboration.csv

.. _duo-DuoMboBoard:

DuoMboBoard
^^^^^^^^^^^
**Source:** `Middelbaar beroepsonderwijs - Adressen - 02. Adressen bevoegde gezagen <http://www.ib-groep.nl/organisatie/open_onderwijsdata/databestanden/mbo_/adressen/Adressen/bevoegde_gezagen.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoMboBoard.csv

.. _duo-DuoMboInstitution:

DuoMboInstitution
^^^^^^^^^^^^^^^^^
**Source:** `Middelbaar beroepsonderwijs - Adressen - 01. Adressen instellingen <http://www.ib-groep.nl/organisatie/open_onderwijsdata/databestanden/mbo_/adressen/Adressen/instellingen.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-DuoMboInstitution.csv

.. _duo-Address:

Address
^^^^^^^

    **Source:** `Primair onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/default.asp>`_
    **Source:** `Voortgezet onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/default.asp>`_
    **Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_
    

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-Address.csv

.. _duo-address_component:

address_component
^^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-address_component.csv

.. _duo-AgesByStudentWeight:

AgesByStudentWeight
^^^^^^^^^^^^^^^^^^^

This dict has three keys *student_weight_0_0*, *student_weight_0_3* and *student_weight_1_2*, the weights are based on the pupil's parents level of education [#weight]_.

**Source:** `Primair onderwijs - Leerlingen - 03. Leerlingen basisonderwijs naar leerlinggewicht en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen3.asp>`_
    

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-AgesByStudentWeight.csv

.. _duo-Coordinates:

Coordinates
^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-Coordinates.csv

.. _duo-department:

department
^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-department.csv

.. _duo-dropout:

dropout
^^^^^^^
**Source:** `Voortijdig schoolverlaten - Voortijdig schoolverlaten - 02. Vsv in het voortgezet onderwijs per vo instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vschoolverlaten/vsvers/vsv_voortgezet.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-dropout.csv

.. _duo-GradesPerCourse:

GradesPerCourse
^^^^^^^^^^^^^^^

**Source:** `08. Examenkandidaten vmbo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp>`_

**Source:** `09. Examenkandidaten havo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp>`_

**Source:** `10. Examenkandidaten vwo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp>`_
    

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-GradesPerCourse.csv

.. _duo-graduates_per_qualification:

graduates_per_qualification
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-graduates_per_qualification.csv

.. _duo-graduation:

graduation
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-graduation.csv

.. _duo-GraudationDepartmentCandidates:

GraudationDepartmentCandidates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-GraudationDepartmentCandidates.csv

.. _duo-participants_per_grade_year_and_qualification:

participants_per_grade_year_and_qualification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-participants_per_grade_year_and_qualification.csv

.. _duo-participants_per_qualification:

participants_per_qualification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-participants_per_qualification.csv

.. _duo-qualifications:

qualifications
^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-qualifications.csv

.. _duo-spo_students_by_birthyear:

spo_students_by_birthyear
^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-spo_students_by_birthyear.csv

.. _duo-spo_students_by_edu_type:

spo_students_by_edu_type
^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-spo_students_by_edu_type.csv

.. _duo-spo_students_per_cluster:

spo_students_per_cluster
^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-spo_students_per_cluster.csv

.. _duo-student_residence:

student_residence
^^^^^^^^^^^^^^^^^

Number of pupils per age group (up to 25, as special education is included).

**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen11.asp>`_
        

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-student_residence.csv

.. _duo-students_by_advice:

students_by_advice
^^^^^^^^^^^^^^^^^^

The level of education [#edu_in_holland]_ that the primary school recommended the student upon leaving primary education
**Source:** `Primair onderwijs - Leerlingen - 12. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar schooladvies <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/Schooladvies.asp>`_
        

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-students_by_advice.csv

.. _duo-students_by_finegrained_structure:

students_by_finegrained_structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-students_by_finegrained_structure.csv

.. _duo-students_by_structure:

students_by_structure
^^^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 01. Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-students_by_structure.csv

.. _duo-students_by_year:

students_by_year
^^^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/leerjaar.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-students_by_year.csv

.. _duo-students_prognosis:

students_prognosis
^^^^^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 11. Prognose aantal leerlingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen11.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-students_prognosis.csv

.. _duo-StudentsByAge:

StudentsByAge
^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-StudentsByAge.csv

.. _duo-StudentsEnrolledInStructure:

StudentsEnrolledInStructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-StudentsEnrolledInStructure.csv

.. _duo-vavo_students:

vavo_students
^^^^^^^^^^^^^
 Students who are registered in secondary education, but are in an adult education program, can still graduate with a secondary education degree (*Rutte - regeling*) 

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-vavo_students.csv

.. _duo-Viewport:

Viewport
^^^^^^^^

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-Viewport.csv

.. _duo-weights_per_school:

weights_per_school
^^^^^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/leerjaar.asp>`_

.. csv-table::
    :delim: ,
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duo-weights_per_school.csv



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
