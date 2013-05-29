Introduction
=============================================
The educational system in the Netherlands is `complex <http://en.wikipedia.org/wiki/Education_in_the_Netherlands>`_, and many public bodies are tasked with keeping schools and students on the right track. However, data regarding this task is made available to the general public in a way it is not easily processable, which makes checks by the public (and press) more difficult.

The OpenOnderwijs API alleviates this problem by providing a unified interface to data on education collected from several institutions with different responsibilities with regard to the Dutch educational system, such as `DUO <http://data.duo.nl>`_, `Onderwijsinspectie <http://www.owinsp.nl>`_ and `Vensters voor Verantwoording <http://schoolvo.nl>`_.

The OpenOnderwijs API is built on open source technology, such as `Scrapy <http://doc.scrapy.org/en/latest/>`_ for scraping school data (the scrapers can be found at `Github <https://github.com/Dispectu/onderwijsscrapers>`_), `Sphinx <http://sphinx-doc.org/>`_ for the documentation, and `ElasticSearch <http://www.elasticsearch.org/>`_ for efficient data storage and retrieval. Also, all school addresses are geocoded using the `BAG42 service <http://calendar42.com/bag42/>`_, an Dutch initiative aiming to integrate high quality, official data sources with "regular" geocoding.

Currently included data
---------------------------------

* DUO

  * Boards (*bevoegde gezagen*)

    * Addresses (geocoded)
    * General information: board id (*bevoegd gezag nummer*), denomination, etc.
    * Financial key indicators (*financiële kengetallen*)

  * Schools (*hoofdvestigingen*)

    * Addresses (geocoded)
    * Geo- and administrative regions (COROP, RMC, RPA, etc.)
    * General information: board id, BRIN, website, etc.
    * Dropouts (*voortijdig schoolverlaters*)

  * Branches (*vestigingen*)

    * Addresses (geocoded)
    * Geo- and administrative regions (COROP, RMC, RPA, etc.)
    * General information: board id, BRIN, branch id, website, etc.
    * Origin of students per year (*Leerlingen per vestiging naar postcode leerling en leerjaar*)
    * Students per education structure (*Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding*)
    * Exam candidates per year, education structure and gender (*Examenkandidaten en geslaagden*)
    * School and central exam results per year and education structure (*Geslaagden, gezakten en gemiddelde examencijfers*)

* Onderwijsinspectie

  * Address (geocoded)
  * General information: board id, BRIN, branch id, website, etc.
  * Current ratings of education structures (*huidig inspectieoordeel*)
  * Historical ratings of education structures
  * Links to available inspection reports

* Vensters voor Verantwoording

  * Address (geocoded)
  * General information: board id, BRIN, branch id, website, etc.
  * Average hours of education planned and realized
  * Parent and student satisfaction suruvey results
  * School costs

Access data
--------------------------------
The :doc:`api` section describes how the data in the OpenOnderwijs API can be accessed through a REST interface.

Alternatively, `Mark Marijnissen <http://www.madebymark.nl/>`_ made a tool available on GitHub (https://github.com/markmarijnissen/openonderwijs-csv) that pulls data from the API and merges that data into CSV files.

API features
--------------------------------
* Data sources are scraped on a regular basis
* Each item is validated against a simple set of rules (e.g. a zip code should not be longer than 6 characters)
* Data is available through a simple REST API and as downloadable tarrballs
* The API exposes powerful search capabilities

.. todo::
	Add some links to relevant parts in the documentation. Determine what 'regular basis' will mean.
