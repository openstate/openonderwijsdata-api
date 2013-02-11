API
=============================================
.. http:get:: /api/1/search

   Search for multiple document types across multiple collections. By default we search in all collections for all available document types.

   Hits are sorted by relevance score in descending order.

   .. todo:: Add something about what we mean with 'relevance score'

   **Example request**:

   .. sourcecode:: http

      GET /users/123/posts/web HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [
        {
          "post_id": 12345,
          "author_id": 123,
          "tags": ["server", "web"],
          "subject": "I tried Nginx"
        },
        {
          "post_id": 12346,
          "author_id": 123,
          "tags": ["html5", "standards", "web"],
          "subject": "We go to HTML 5"
        }
      ]

   :query q: a term based query that searchers the ``name``, ``address`` (``street``, ``city``, ``zip_code``) and ``website`` fields. When the query consists of multiple terms, an ``OR`` query is constructed between the terms.
   :statuscode 200: no error

.. http:get:: /get_docment/(str:collection)/(str:doc_type)/(str:doc_id)
   
   :statuscode 200: no error
   :statuscode 404: document, collection or document type does not exist