Introduction
=============================================
The educational system in the Netherlands is `complex <http://en.wikipedia.org/wiki/Education_in_the_Netherlands>`_, and many public bodies are tasked with keeping schools and students on the right track. However, data regarding this task is made available to the general public in a way it is not easily processable, which makes checks by the public (and press) more difficult.

The OpenOnderwijs API alleviates this problem by providing a unified interface to data on education collected from several institutions with different responsibilities with regard to the Dutch educational system, such as `DUO <http://data.duo.nl>`_, `Onderwijsinspectie <http://www.owinsp.nl>`_ and `Vensters voor Verantwoording <http://schoolvo.nl>`_.

The OpenOnderwijs API is built on open source technology, such as `Scrapy <http://doc.scrapy.org/en/latest/>`_ for scraping school data (the scrapers can be found at `Github <https://github.com/Dispectu/onderwijsscrapers>`_), `Sphinx <http://sphinx-doc.org/>`_ for the documentation, and `ElasticSearch <http://www.elasticsearch.org/>`_ for efficient data storage and retrieval. Also, all school addresses are geocoded using the `BAG42 service <http://calendar42.com/bag42/>`_, an Dutch initiative aiming to integrate high quality, official data sources with "regular" geocoding.
