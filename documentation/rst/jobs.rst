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

    id;Jobfeed job ID. Unique identifier for a job posting.
    possible_startersjob;Indicator of possible startersjob (1 = true)
    date_found;Date found
    title;Vacancy title
    organization_name;Advertiser name
    job_location;Job location (normalized, e.g. Den Bosch => 's-Hertogenbosch)
    job_location_id;Postal code of the job location (normalized, e.g. Amsterdam = 1000)
    job_location_latitude;Geocoordinates of the job location
    job_location_longitude;Geocoordinates of the job location
    jobfeed_profession;Jobfeed profession code. Normalized based on the vacancy title to one of the professions in the Jobfeed professions taxonomy
    jobfeed_profession_id;Jobfeed profession code
    jobfeed_profession_group;Jobfeed profession group
    jobfeed_profession_group_id;Jobfeed profession group code
    jobfeed_profession_class;Jobfeed profession class
    jobfeed_profession_class_id;Jobfeed profession class code
    source_url;The original vacancy URL
    source_website;"Source site (e.g. ""werk.nl"")."
    source_type;Type of source (e.g. jobsite, company site)
    source_type_id;Source type (ID)
    education_level;Education level. Extracted and normalized from the vacancy text, otherwise derived from the normalized profession.
    education_level_id;Education level code
    employment_type;Employment type (fulltime, parttime, fulltime/parttime). Working hours >32 hours are considered fulltime, hours <=32 hours parttime.
    employment_type_id;Employment type (ID)
    contract_type;Contract type (permanent, temporary, internship, …)
    contract_type_id;Contract type (ID)
    working_hours;Working hours (regular/irregular)
    working_hours_id;Working hours (ID)
    hours_per_week_min;Number of hours per week min
    hours_per_week_max;Number of hours per week max
    salary_min;Minimum salary per month
    salary_max;Maximum salary per month
    experience_min;Number of years of experience min
    experience_max;Number of years of experience max
    via_intermediary;Job has been posted by an intermediary (yes/no)
    expired_at;Date the vacancy expired, meaning that the vacancy is no longer online. If empty, the vacancy has not yet expired.
    sector;Organisation sector/industry). Derived by matching the advertiser of the job to the Chamber of Commerce table. For jobs posted by intermediaries, the sector is unknown and the sector of the intermediary is returned, instead of the actual employer's sector
    sector_id;Industry code of the organisation
    org_size;Organisation size (number of employees). Derived by matching the advertiser of the job to the Chamber of Commerce table. For jobs posted by intermediaries, this number represents the size of the employee, not the size of the actual employer.
    org_size_id;Organisation size (ID)
    sic;Standard Industry Code. In The Netherlands: SBI 2008 (based on NACE)
    sic_descr;Description of SBI 2008 code
    job_descr;Job description
    employer_descr;Employer description
    candidate_descr;Candidate description
    conditions_descr;Job conditions and benefits description
    application_descr;Application procedure description
    fulltxt;Full job text

The full data model is available at (http://api.openonderwijsdata.nl/sources/jobfeed/datamodel.xlsx).

API
---

.. http:get:: /api/v2/job_search

   Search for multiple document types across multiple indexes. By default we search in all indexes for all available document types.

   Hits are sorted by relevance based on their similarity to the query (see query parameter ``q``).

   Other query parameters are listed above. Additionally, you can use the following parameters for specifying the format of results:

    .. csv-table::
       :header: "Parameter", "Description"
       :widths: 1, 4
       :delim: ;

        size;Number of results (default: 10)
        from;Starting point for results
        order;Order of results (``asc`` or ``desc``)


   **Example: search for an "ict" job**

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
