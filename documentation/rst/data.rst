Data
=================================================================================
The data that is made available through the API originates from different sources: :ref:`duodata`, :ref:`schoolvodata` and the :ref:`owinspdata`. Each of these sources provides different types of data, from school assessments to financial figures. For each source the available fields are described, as well as the data they contain.

The data sources present their data aggregated on different *granularities*: financial data is usually aggregated to the level of the school *board*, whereas the number of students is available for specific locations (*branch*) of a school. In order to represent the data properly, three entities are defined: *vo_board*, *vo_school* and *vo_branch*.

**vo_board**
    A vo_board represents the school board. [#schoolbestuur]_

**vo_school**
    Henk

**vo_branch**
    Blah

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
