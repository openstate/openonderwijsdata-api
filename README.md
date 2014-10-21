# Open Onderwijs Data API

## Important links
 - [Open Onderwijs Data homepage](http://www.openonderwijsdata.nl/)
 - [Official source code repo](https://github.com/openstate/openonderwijsdata-api/)
 - [Documentation](http://api.openonderwijsdata.nl/documentation/)
 - [Currently included data](http://api.openonderwijsdata.nl/documentation/rst/introduction.html#currently-included-data)
 - [Issue tracker](https://github.com/openstate/openonderwijsdata-api/issues)

## Bugs and feature requests

Have a bug or a feature request? Please first read the [issue guidelines](https://github.com/openstate/openonderwijsdata-api/blob/master/CONTRIBUTING.md) and search for existing and closed issues. If your problem or idea is not addressed yet, [please open a new issue](https://github.com/openstate/openonderwijsdata-api/issues/new).

## API Documentation

The documentation of the Open Onderwijs Data API can be found at [api.openonderwijsdata.nl/documentation](http://api.openonderwijsdata.nl/documentation/). This documentation is for working with the requests and the data available via [the API itself](http://api.openonderwijsdata.nl/).

We use [Sphinx](http://sphinx-doc.org/) to create the documentation. The source files are included in this repo under the `documentation` directory.

## Getting Started

To run the code yourself locally using the Elasticsearch exporter, do the following:

1. Make sure up-to-date versions of Python 2, [bower](http://www.bower.io) and [Elasticsearch](http://www.elasticsearch.org/) are installed, and install the dependencies in `requirements.txt` (Protip: use `pip install -r requirements.txt`).
2. Start elasticsearch and specify its port in `onderwijsscrapers/onderwijsscrapers/settings.py` or `local_settings.py`.
3. Navigate your terminal to `onderwijsscrapers/` and run the scrapy spider for the datasets you're interested in:

	```
		scrapy crawl <spider-name>
	```
4. Install client-side dependencies with `bower install`.
5. Run `app/app.py` to start the webserver and browse the API locally on your machine (http://localhost:5001/)

## Contributing

Please read through our [contributing guidelines](https://github.com/openstate/openonderwijsdata-api/blob/master/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

## Copyright and license

The Open Onderwijs Data API code is distributed under the [GNU Lesser General Public License v3](https://www.gnu.org/licenses/lgpl.html).

The OOD documentation is released under the  [Creative Commons Attribution 4.0 International license](http://creativecommons.org/licenses/by/4.0/).
