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

.. _`COROP-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
.. _`Onderwijsgebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
.. _`Nodaal gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
.. _`Rmc-regio`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
.. _`Rpa-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
.. _`Wgr-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied
.. _`Indicatie Special Basis Onderwijs`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Indicatie%20speciaal%20onderwijs
.. _`Cluster`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Cluster

.. _duovoboard:

vo_board
^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 03. Adressen hoofdbesturen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/besturen.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duodata.csv

.. _duovoschool:

vo_school
^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 01. Adressen hoofdvestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/hoofdvestigingen.asp>`_


.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duovoschool.csv

.. _duovobranch:

vo_branch
^^^^^^^^^
**Source:** `Voortgezet onderwijs - Adressen - 02. Adressen alle vestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/vestigingen.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duovobranch.csv

.. _duopoboard:

po_board
^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 05. Bevoegde gezagen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/po_adressen05.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duopoboard.csv

.. _duoposchool:

po_school
^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 01. Hoofdvestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/hoofdvestigingen.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duoposchool.csv

.. _duopobranch:

po_branch
^^^^^^^^^
**Source:** `Primair onderwijs - Adressen - 03. Alle vestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/vest_bo.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duopobranch.csv

.. _duopaocollaboration:

paocollaboration
^^^^^^^^^^^^^^^^
**Source:** `Passend onderwijs - Adressen - 01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/passendow/Adressen/Adressen/passend_po_1.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duopaocollaboration.csv


.. _duoaddress:

Address
^^^^^^^
**Source:** `Primair onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/default.asp>`_

**Source:** `Voortgezet onderwijs - Adressen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/default.asp>`_

**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duoaddress.csv

.. _duoaddresscomponent:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duoaddresscomponent.csv

.. _agesbystudentweight:

AgesByStudentWeight
^^^^^^^^^^^^^^^^^^^
This dict has three keys *student_weight_0.0*, *student_weight_0.3* and *student_weight_1.2*, the weights are based on the pupil's parents level of education [#weight]_.

**Source:** `Primair onderwijs - Leerlingen - 03. Leerlingen basisonderwijs naar leerlinggewicht en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen3.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/agesbystudentweight.csv

.. _dropout:

Dropout
^^^^^^^
**Source:** `Voortijdig schoolverlaten - Voortijdig schoolverlaten - 02. Vsv in het voortgezet onderwijs per vo instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vschoolverlaten/vsvers/vsv_voortgezet.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/dropout.csv

.. _edutypes:

EduTypes
^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen7.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/edutypes.csv

.. _examgrades:

ExamGrades
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 07. Geslaagden, gezakten en gemiddelde examencijfers per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen7.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/examgrades.csv


.. _finindicator:

FinancialIndicator
^^^^^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Financiën - 15. Kengetallen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Financien/Jaarrekeninggegevens/Kengetallen.asp>`_

**Source:** `Voortgezet onderwijs - Financiën - 15. Kengetallen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/Financien/Financien/Kengetallen.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/finindicator.csv

.. _gradespercourse:

GradesPerCourse
^^^^^^^^^^^^^^^
**Source:** `08. Examenkandidaten vmbo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp>`_

**Source:** `09. Examenkandidaten havo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp>`_

**Source:** `10. Examenkandidaten vwo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/gradespercourse.csv


.. _graduation:

Graduation
^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/graduation.csv


.. _graduationdepartment:

GraduationPerDepartment
^^^^^^^^^^^^^^^^^^^^^^^
Belongs to :ref:`graduationdepartment`.

**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/graduationdepartment.csv

.. _duogeoloc:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duogeoloc.csv

.. _duogeoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duogeoviewport.csv

.. _duometa:

Meta
^^^^
**Source:** `OpenOnderwijs scrapers <http://api.openonderwijsdata.nl/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duometa.csv

.. _students_by_advice:

StudentsByAdvice
^^^^^^^^^^^^^^^^

The level of education [#edu_in_holland]_ that the primary school recommended the student upon leaving primary education
**Source:** `Primair onderwijs - Leerlingen - 12. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar schooladvies <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/Schooladvies.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/students_by_advice.csv

.. _spo_by_birthyear:

SPOStudentsByBirthyear
^^^^^^^^^^^^^^^^^^^^^^

.. spo_law 
.. spo_edu_type
.. spo_cluster

**Source:** `Primair onderwijs - Leerlingen - 05. Leerlingen speciaal (basis)onderwijs naar geboortejaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen5.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/spo_by_birthyear.csv

.. _spo_by_edu_type:

SPOStudentsByEduType
^^^^^^^^^^^^^^^^^^^^

**Source:** `Primair onderwijs - Leerlingen - 06. Leerlingen speciaal (basis)onderwijs naar onderwijssoort <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen6.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/spo_by_edu_type.csv

.. _spo_per_cluster:

SPOStudentsPerCluster
^^^^^^^^^^^^^^^^^^^^^

**Source:** `Primair onderwijs - Leerlingen - 04. Leerlingen speciaal onderwijs naar cluster <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen4.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/spo_per_cluster.csv


.. _dustrespo:

StudentResidences
^^^^^^^^^^^^^^^^^
Number of pupils per age group (up to 25, as special education is included).

**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen11.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/dustrespo.csv

.. _duostpores:

StudentResidence
^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duostpores.csv

.. _students_prognosis:

StudentPrognosis
^^^^^^^^^^^^^^^^

**Source:** `Primair onderwijs - Leerlingen - 11. Prognose aantal leerlingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen11.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/students_prognosis.csv

.. _students_by_origin:

StudentsByOrigin
^^^^^^^^^^^^^^^^
Number of students born in countries other than The Netherlands, by country.

**Source:** `Primair onderwijs - Leerlingen - 09. Leerlingen basisonderwijs met een niet-Nederlandse achtergrond naar geboorteland <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen9.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/students_by_origin.csv

.. _duostdres:

StudentResidence
^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 02. Leerlingen per vestiging naar postcode leerling en leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen2.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duostdres.csv

.. _duostdstruct:

StudentPerStructure
^^^^^^^^^^^^^^^^^^^
**Source:** `Voortgezet onderwijs - Leerlingen - 01. Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/duostdstruct.csv

.. _students_by_year:

StudentsByYear
^^^^^^^^^^^^^^

**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/leerjaar.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/students_by_year.csv


.. _studentweights:

StudentWeights
^^^^^^^^^^^^^^
**Source:** `Primair onderwijs - Leerlingen - 01. Leerlingen basisonderwijs naar leerlinggewicht en per vestiging het schoolgewicht en impulsgebied <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen1.asp>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/studentweights.csv

.. _schoolvodata:

Vensters voor Verantwoording
----------------------------
`Vensters voor Verantwoording <http://schoolvo.nl/>`_ provides VO schools with a platform where they can share data on their performance with the public. The data described here is currently **not** available to the public through the `OpenOnderwijs API <http://api.openonderwijsdata.nl/>`_.

vo_branch
^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvodata.csv


.. _schoolvoaddress:

Address
^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvoaddress.csv

.. _schoolvoaddrcomp:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvoaddrcomp.csv

.. _costs:

Costs
^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/costs.csv

.. _costsperyear:

CostsPerYear
^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/costsperyear.csv

.. _eduhours:

EduHoursPerStudent
^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/eduhours.csv

.. _eduhoursstructure:

EduHoursPerStructure
^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/eduhoursstructure.csv

.. _schoolvo_coordinates:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvo_coordinates.csv

.. _schoolvoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvoviewport.csv

.. _indicator:

Indicator
^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/indicator.csv

.. _schoolvometa:

Meta
^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/schoolvometa.csv

.. _satisfaction:

Satisfaction
^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/satisfaction.csv

.. _owinspdata:

Onderwijsinspectie
------------------
The Inspectie voor het Onderwijs [#owinsp]_ is tasked with inspecting Dutch schools. Since 1997, they are required to publish reports on their findings when inspecting schools.

.. _owinspdatavobranch:

vo_branch
^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspdata.csv

.. _owinspdatapobranch:

po_branch
^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspdatapobranch.csv

.. _owinspaddress:

Address
^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspaddress.csv

.. _owinspaddrcomp:

AddressComponent
^^^^^^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspaddrcomp.csv

.. _exam_avg_grades:

AverageExamGrades
^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/exam_avg_grades.csv

.. _owinspcurrat:

CurrentRating
^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspcurrat.csv

.. _exam_part_prof:

ExamParticipationPerProfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/exam_part_prof.csv

.. _first_year_comp:

FirstYearComposition
^^^^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/first_year_comp.csv

.. _first_year_perf:

FirstYearPerformance
^^^^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/first_year_perf.csv

FirstYearsPerformance

.. _owinsp_coordinates:

GeoLocation
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinsp_coordinates.csv

.. _owinspgeoviewport:

GeoViewport
^^^^^^^^^^^
**Source:** `BAG42 Geocoding service <http://calendar42.com/bag42/>`_

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspgeoviewport.csv

.. _owinsprathist:

HistoricalRating
^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinsprathist.csv

.. _owinspmeta:

Meta
^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspmeta.csv

.. _perf_ass:

PerformanceAssessments
^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/perf_ass.csv

.. _advice_struct_3:

PrimarySchoolAdvices
^^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/advice_struct_3.csv

.. _advice_struct_comp:

PrimarySchoolAdvice
^^^^^^^^^^^^^^^^^^^

.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/advice_struct_comp.csv

.. _owinspreport:

Report
^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/owinspreport.csv

.. _straight_grad:

StraightToGraduation
^^^^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/straight_grad.csv

.. _3yearnoretakes:

StraightToThirdYear
^^^^^^^^^^^^^^^^^^^
.. csv-table::
    :delim: ;
    :widths: 2, 1, 3, 10
    :header-rows: 1
    :file: tables/3yearnoretakes.csv

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

