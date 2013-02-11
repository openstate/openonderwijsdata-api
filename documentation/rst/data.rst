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
.. table:: Descriptions of fields and their types for SchoolVO branches

    ======== ======== ========================================================
    Field    Type     Description
    ======== ======== ========================================================
    address  Address  An addressnfioqwwfnifniowefepfmqpifjeopwfkoqwp
    ======== ======== ========================================================

.. _owinspdata:

Onderwijsinspectie
---------------------------------------------------------------------------------
`Inspectierapporten archief <http://www.owinsp.nl/>`_

.. [#schoolbestuur] http://nl.wikipedia.org/wiki/Schoolbestuur
.. [#brin] http://nl.wikipedia.org/wiki/BRIN
.. [#edu_in_holland] http://en.wikipedia.org/wiki/Education_in_the_Netherlands#High_school
