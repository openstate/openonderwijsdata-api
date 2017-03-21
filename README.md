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

Installation:

- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Clone this repository and `cd` to `openonderwijsdata-api/docker`
- (optional) If you're developing then uncomment the ``Development`` and comment the ``Production`` sections in ``docker/nginx/conf.d/default.conf`` and ``conf/supervisor.conf``. You will then use Flask's development webserver instead of uWSGI, which is useful because changes to the code are automatically reloaded. You can also remove the lines ``restart: always`` from ``docker/docker-compose.yml`` otherwise the containers will automatically start when you start your machine. In ``docker/docker-compose.yml`` you might want to remove the line containing ``- nginx-load-balancer`` listed in the networks section of the ``c-ood-nginx`` service as well as the last three lines (shown below) as they are specific to our setup and not needed for general usage:
```
  nginx-load-balancer:
    external:
      name: docker_nginx-load-balancer
```
- Build and start containers: `sudo docker-compose up -d`
- Install bower packages: `sudo docker exec docker_c-ood-app_1 bower install --allow-root`
- Generate documentation: `sudo docker exec docker_c-ood-app_1 sh -c 'cd documentation && make html'`
- The API is now locally accessible from the host via `http://<CONTAINER IP ADDRESS>` (look up the container's IP address using `sudo docker inspect --format='{{range $index, $element := .NetworkSettings.Networks}}{{if eq $index "docker_ood"}}{{.IPAddress}}{{end}}{{end}}' docker_c-ood-nginx_1`)

Run a crawler:

- List all spiders: `sudo docker exec docker_c-ood-app_1 sh -c 'cd onderwijsscrapers && scrapy list'`
- Run the spider you want: `sudo docker exec docker_c-ood-app_1 sh -c 'cd onderwijsscrapers && scrapy crawl <spider-name>'`

## Backup and restore

Some commands on how to [backup and restore Elasticsearch indices](https://www.elastic.co/guide/en/elasticsearch/reference/1.4/modules-snapshots.html#_shared_file_system_repository).

Create a new backup location in the root directory of the OOD repository (do this on the machine which should be backupped AND the machine where you want to restore the backup) and make sure Elasticsearch can write to it, e.g.:
```
mkdir backups
sudo docker exec docker_c-ood-app_1 curl -XPUT 'http://localhost:9200/_snapshot/my_backup' -d '{"type": "fs", "settings": {"location": "/opt/ood/backups"}}'
```

Save all indices/cluster with a snapshot:
```
sudo docker exec docker_c-ood-app_1 curl -XPUT "http://localhost:9200/_snapshot/my_backup/ood_backup"
```

Copy the `backups` directory containing the snapshot into the `openonderwijs-data` directory on the other machine (on this other machine, make sure you created a backup location as described above).

Remove any indices which are already present on the new machine (assuming you don't want to keep that data):
```
sudo docker exec docker_c-ood-app_1 curl -XDELETE 'http://localhost:9200/_all'
```

Restore the snapshot:
```
sudo docker exec docker_c-ood-app_1 curl -XPOST "http://localhost:9200/_snapshot/my_backup/ood_backup/_restore"
```

## Contributing

Please read through our [contributing guidelines](https://github.com/openstate/openonderwijsdata-api/blob/master/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

## Copyright and license

The Open Onderwijs Data API code is distributed under the [GNU Lesser General Public License v3](https://www.gnu.org/licenses/lgpl.html).

The OOD documentation is released under the  [Creative Commons Attribution 4.0 International license](http://creativecommons.org/licenses/by/4.0/).
