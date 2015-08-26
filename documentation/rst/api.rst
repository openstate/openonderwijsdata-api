API
=============================================

.. http:get:: /api/v1/search

   Search for multiple document types across multiple indexes. By default we search in all indexes for all available document types.

   Hits are sorted by relevance based on their similarity to the query (see query parameter ``q``).

   The query parameters ``brin``, ``board_id``, ``branch_id``, ``zip_code`` and ``city`` each act as a filter on the result set. When more than one filter is specified, an ``AND`` condition is formed between the filters.

   **Example: find all school branches in Amsterdam Zuidoost**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v1/search?city=AMSTERDAM%20ZUIDOOST&doctypes=vo_branch"

   Example response (only one hit with some of it's fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 173883
      Date: Tue, 12 Feb 2013 12:19:49 GMT
      Content-Type: application/json

      {
        "total": 22,
        "took": 14,
        "hits": [
          {
            "_index": "duo",
            "_type": "vo_branch",
            "_id": "2011-03AQ-0",
            "_score": 1
            "_source": {
              "name": "Open Sgm Bylmer Vath Havo Mavo Lhno Lto Leao",
              "address": {
                "city": "AMSTERDAM ZUIDOOST",
                "street": "Gulden Kruis 5",
                "zip_code": "1103BE"
              }
            }
          }
        ]
      }

   **Example: find all Lyceum's in the Vensters voor Verantwoording and Onderwijsinspectie indexes**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v1/search?q=Lyceum&indexes=schoolvo,onderwijsinspectie"

   Example response (only one hit with some of it's fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 67846
      Date: Tue, 12 Feb 2013 13:09:58 GMT
      Content-Type: text/javascript

      {
        "total": 22,
        "took": 14,
        "hits": [
          {
            "_index": "onderwijsinspectie",
            "_type": "vo_school",
            "_id": "01KL-0",
            "_score": 2.4677997,
            "_source": {
              "name": "Lorentz Lyceum",
              "address": {
                "city": "Arnhem",
                "street": "Groningensingel 1235",
                "zip_code": "6835 HZ"
              }
            }
          }
        ]
      }

   :query q: a term based query that searches the ``name``, ``address`` (``street``, ``city``, ``zip_code``) and ``website`` fields by default. When the query consists of multiple terms, an ``OR`` query is constructed between the terms. Additionally the `Lucene Query syntax <http://lucene.apache.org/core/4_1_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package_description>`_ can be used, including searching in (combinations of) specific fields. *Optional*.
   :query brin: filter results on ``brin``. *Optional*.
   :query board_id: filter results on ``board_id``. *Optional*.
   :query branch_id: filter results on ``branch_id``. *Optional*.
   :query zip_code: filter results on ``address.zip_code``. *Optional*.
   :query geo_location: Filter results on provided coordinate. String, formatted as "*latitude*, *longitude*". *Optional*.
   :query geo_distance: Used in conjuction with **geo_filter**. Maximum distance in km of a result from the coordinate provided by **geo_filter**. *Optional*, *default*: "10km".
   :query sort: sort the search results by a given field. Use the value ``distance`` in conjunction with ``geo_location`` to sort results by distance to a given coordinate. *Optional*, *default*: sort by relevance to query q.
   :query order: Return results in descending (``desc``) or ascending (``asc``) order.*Optional*, *default*: ``asc``.
   :query indexes: comma separated list of index names that should be searched. *Optional*, *default*: search all available indexes.
   :query doctypes: comma separated list of document types that should be included in the search. *Optional*, *default*: search all available doctypes.
   :query size: the number of documents to return. *Optional*, *default*: 10, *min*: 1, *max*: 500.
   :query from: the offset from the first result in the result set. For example, when ``size=10`` and the total number of hits is 20, ``from=10`` will return result 10 to 20. *Optional*, *default*: 0.
   :statuscode 200: OK, no errors.
   :statuscode 400: Bad Request. An accompanying error message will explain why the request was invalid.

.. http:get:: /api/v1/get_document/(str:index)/(str:doctype)/(str:doc_id)

   This method can be used to retrieve a single document, provided that you know the document's index, type and id.

   **Example: get a document from the DUO index that describes board 40586**

   .. parsed-literal::

      $ curl -i "http://<api_domain>/api/v1/get_document/duo/vo_board/40586"

   Example response (only one hit with some of it's fields are shown here):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Length: 4955
      Date: Wed, 13 Feb 2013 11:20:18 GMT
      Content-Type: text/javascript

      {
        "_type": "vo_board",
        "_id": "2011-40586",
        "_index": "duo",
        "_source": {
          "board_id": 40586,
          "website": "www.espritscholen.nl",
          "municipality_code": 363,
          "name": "Onderwijsstichting Esprit",
          "administrative_office_id": 940,
        }
      }


   :statuscode 200: OK, no errors.
   :statuscode 400: Bad Request. An accompanying error message will explain why the request was invalid.
   :statuscode 404: Not Found. The requested document does not exist.

.. http:get:: /api/v1/get_validation_results/(str:index)/(str:doctype)/(str:doc_id)
