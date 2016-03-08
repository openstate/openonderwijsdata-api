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


{% for resource in resources %}

{{ resource.name }}
^^^^

{% for schema_name, schema in resource.schemas.items() %}
{% for source in resource.sources[schema_name] %}
**Source:** `source <{{source.web}}>_
{% endfor %}
.. csv-table:: schema_name
   :header: {{ schema.header }}
   {{ schema.content }}

{% endfor %}

{% endfor %}

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
