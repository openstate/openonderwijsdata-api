Job Vacancies
=============

Data
----



JobFeed
^^^^^^^^^^

The fields in the JobFeed dataset are described below. These are temporarily only available in Dutch.

.. csv-table::
   :header: "Field", "Description"
   :widths: 1, 4
   :delim: ;

    id;Jobfeed vacature ID. Unieke identifier voor een vacature-posting.
    date_found;Datum gevonden
    title;Vacaturetitel
    organization_name;Naam van de adverteerder
    job_location;Standplaats van de vacature (genormaliseerd, b.v. Den Bosch => 's-Hertogenbosch).
    job_location_id;Postcode van de standplaats (genormaliseerd, b.v. Amsterdam = 1000)
    job_location_latitude;Geocoordinaten van de standplaats
    job_location_longitude;Geocoordinaten van de standplaats
    jobfeed_profession;Jobfeed beroep. Genormaliseerd op basis van de vacaturetitel naar een van de beroepen uit de Jobfeed-beroepentaxonomie
    jobfeed_profession_id;Jobfeed beroepscode
    jobfeed_profession_group;Jobfeed beroepsgroep
    jobfeed_profession_group_id;Jobfeed beroepsgroepcode
    jobfeed_profession_class;Jobfeed beroepsklasse omschrijving
    jobfeed_profession_class_id;Jobfeed beroepsklasse code
    source_url;De originele vacature-URL
    source_website;Bron site (b.v. werk.nl).
    source_type;Type bron, b.v. jobsite, bedrijfswebsite.
    source_type_id;Type bron (ID)
    education_level;Opleidingsniveau omschrijving (b.v. HBO). Geëxtraheerd en genormaliseerd uit de vacaturetekst indien genoemd, anders afgeleid van het genormaliseerde beroep.
    education_level_id;Opleidingsniveau code. 
    employment_type;Dienstverband (fulltime, parttime, parttime/fulltime). Werkuren >32 uur wordt gezien als fulltime, <=32 uur parttime.
    employment_type_id;Dienstverband (ID)
    contract_type;Contracttype (vast, tijdelijk, stage, …)
    contract_type_id;Contracttype (ID)
    working_hours;Werktijden (regelmatig/onregelmatig)
    working_hours_id;Werktijden (ID)
    hours_per_week_min;Aantal werkuren per week min
    hours_per_week_max;Aantal werkuren per week max
    salary_min;Salaris per maand min
    salary_max;Salaris per maand max
    experience_min;Aantal jaren werkervaring min
    experience_max;Aantal jaren werkervaring max
    via_intermediary;Vacature is geplaatst door een intermediair (ja/nee)
    expired_at;Datum waarop de vacature verlopen is. D.w.z. de vacature staat niet meer online. Leeg indien de vacature nog niet verlopen is.
    sector;Branche omschrijving van de organisatie. Afgeleid door een match van de adverteerder van de vacature met de KvK-tabel. Vacatures van intermediairs hebben altijd sector 'Arbeidsbemiddeling'
    sector_id;Branchecode van de organisatie. 
    org_size;Organisatiegrootte omschrijving
    org_size_id;Organisatiegrootte (aantal medewerkers). Afgeleid door een match van de adverteerder van de vacature met de KvK-tabel. Bij vacatures van intermediairs is dit dus niet het aantal medewerkers bij de opdrachtgever.
    sic;Standard Industry Code. In Nederland: SBI 2008
    sic_descr;Omschrijving van SBI 2008 code
    job_descr;Functie-omschrijving
    employer_descr;Omschrijving werkgever
    candidate_descr;Omschrijving kandidaat/profiel
    conditions_descr;Omschrijving arbeidsvoorwaarden
    application_descr;Omschrijving sollicitatieprocedure
    fulltxt;Volledige vacaturetekst

API
---

.. http:get:: /api/v2/job_search

   Search for multiple document types across multiple indexes. By default we search in all indexes for all available document types.

   Hits are sorted by relevance based on their similarity to the query (see query parameter ``q``).

   Other query parameters are listed above. 

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v2/job_search?q=ict"

   Example response (only one hit with some of its fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 173883
      Date: Fri, 12 Dec 2014 15:19:49 GMT
      Content-Type: application/json

      {
        "total": 22,
        "took": 14,
        "hits": [
          {
            "_id": "3TWbJ56SRTuYfrlYd3EDeA", 
            "_index": "jobfeed_141212", 
            "_score": 2.5722585, 
            "_type": "job",
            "_source": {
                "candidate_descr": "* MBO werk- en denkniveau\n     * Een \"aanpakker\" en \"teamworker\"\n     * Goede computervaardigheden\n     * Woonachtig in de regio/eigen vervoer", 
                "conditions_descr": "...", 
                "contract_type": "Permanent contract", 
                "contract_type_id": 1, 
                "date": "2014-11-27T00:00:00", 
                "education_level": "MBO", 
                "education_level_id": 9, 
                "employer_descr": "...", 
                "employment_type": "Full-time (> 32 hours)", 
                "employment_type_id": 1, 
                "fulltxt": "...", 
                "hours_per_week_max": 40, 
                "hours_per_week_min": 40, 
                "id": "31828796", 
                "industry_sector_id": 1620909, 
                "job_descr": "...", 
                "jobfeed_profession": "medewerker klantenservice", 
                "jobfeed_profession_class": "Administratie en klantenservice", 
                "jobfeed_profession_class_id": 1, 
                "jobfeed_profession_group": "medewerkers klantenservice", 
                "jobfeed_profession_group_id": 4, 
                "jobfeed_profession_id": 1260, 
                "org_size": "10-49", 
                "org_size_id": 2, 
                "organization_name": "Intrema bv", 
                "sector": "ICT", 
                "sector_id": 12, 
                "sic": 620909, 
                "sic_descr": "Overige dienstverlenende activiteiten op het gebied van informatietechnologie n.e.g.", 
                "title": "Junior Medewerk(st)er Front Office", 
                "via_intermediary": "no", 
                "working_hours": "Regular working hours", 
                "working_hours_id": 1
            }
          }
        ]
      }

.. http:get:: /api/v2/job_doc/(str:index)/(str:doctype)/(str:doc_id)

   This method can be used to retrieve a single document, provided that you know the document's index, type and id.

   **Example: get a job with id q0ruErKwS86s2s8QA2nQgg**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v2/job_doc/jobfeed/job/q0ruErKwS86s2s8QA2nQgg"

   Example response (only one hit with some of its fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 4955
      Date: Wed, 13 Feb 2013 11:20:18 GMT
      Content-Type: text/javascript

      {
        "_type": "job",
        "_id": "q0ruErKwS86s2s8QA2nQgg",
        "_index": "jobfeed_141212",
        "_source": {
          "education_level": "HBO",
          "employment_type": "Full-time (> 32 hours)",
          "job_location": "Lichtenvoorde", 
          (...)
        }
      }


   :statuscode 200: OK, no errors.
   :statuscode 400: Bad Request. An accompanying error message will explain why the request was invalid.
   :statuscode 404: Not Found. The requested document does not exist.
