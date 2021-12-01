# TODO got lazy...

data = {
    'https://example.com/api/v1/plugins/4/': {},

    'https://example.com/api/v1/plugins/5/': {},

    'https://example.com/api/v1/plugins/6/': {},

    'https://example.com/api/v1/pipelines/': {
        "collection_links": {
            "plugins": "https://example.com/api/v1/plugins/"
        },
        "count": 2,
        "next": None,
        "previous": None,
        "queries": [
            {
                "data": [
                    {
                        "name": "id",
                        "value": ""
                    },
                    {
                        "name": "owner_username",
                        "value": ""
                    },
                    {
                        "name": "name",
                        "value": ""
                    },
                    {
                        "name": "category",
                        "value": ""
                    },
                    {
                        "name": "description",
                        "value": ""
                    },
                    {
                        "name": "authors",
                        "value": ""
                    },
                    {
                        "name": "min_creation_date",
                        "value": ""
                    },
                    {
                        "name": "max_creation_date",
                        "value": ""
                    }
                ],
                "href": "https://example.com/api/v1/pipelines/search/",
                "rel": "search"
            }
        ],
        "results": [
            {
                "authors": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>",
                "category": "",
                "creation_date": "2021-11-12T23:03:58.401890-05:00",
                "default_parameters": "https://example.com/api/v1/pipelines/1/parameters/",
                "description": "A linear and boring pipeline.",
                "id": 1,
                "instances": "https://example.com/api/v1/pipelines/1/instances/",
                "locked": False,
                "modification_date": "2021-11-12T23:03:58.401912-05:00",
                "name": "Example linear pipeline",
                "owner_username": "chris",
                "plugin_pipings": "https://example.com/api/v1/pipelines/1/pipings/",
                "plugins": "https://example.com/api/v1/pipelines/1/plugins/",
                "url": "https://example.com/api/v1/pipelines/1/"
            },
            {
                "authors": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>",
                "category": "",
                "creation_date": "2021-11-12T23:03:58.742417-05:00",
                "default_parameters": "https://example.com/api/v1/pipelines/2/parameters/",
                "description": "A fun but nonetheless useless pipeline.",
                "id": 2,
                "instances": "https://example.com/api/v1/pipelines/2/instances/",
                "locked": False,
                "modification_date": "2021-11-12T23:03:58.742439-05:00",
                "name": "Example branching pipeline",
                "owner_username": "chris",
                "plugin_pipings": "https://example.com/api/v1/pipelines/2/pipings/",
                "plugins": "https://example.com/api/v1/pipelines/2/plugins/",
                "url": "https://example.com/api/v1/pipelines/2/"
            }
        ],
        "template": {
            "data": [
                {
                    "name": "name",
                    "value": ""
                },
                {
                    "name": "authors",
                    "value": ""
                },
                {
                    "name": "category",
                    "value": ""
                },
                {
                    "name": "description",
                    "value": ""
                },
                {
                    "name": "locked",
                    "value": ""
                },
                {
                    "name": "plugin_tree",
                    "value": ""
                },
                {
                    "name": "plugin_inst_id",
                    "value": ""
                }
            ]
        }
    },

    'https://example.com/api/v1/pipelines/2/': {
        "authors": "Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>",
        "category": "",
        "creation_date": "2021-11-12T23:03:58.742417-05:00",
        "default_parameters": "https://example.com/api/v1/pipelines/2/parameters/",
        "description": "A fun but nonetheless useless pipeline.",
        "id": 2,
        "instances": "https://example.com/api/v1/pipelines/2/instances/",
        "locked": False,
        "modification_date": "2021-11-12T23:03:58.742439-05:00",
        "name": "Example branching pipeline",
        "owner_username": "chris",
        "plugin_pipings": "https://example.com/api/v1/pipelines/2/pipings/",
        "plugins": "https://example.com/api/v1/pipelines/2/plugins/",
        "template": {
            "data": [
                {
                    "name": "name",
                    "value": ""
                },
                {
                    "name": "authors",
                    "value": ""
                },
                {
                    "name": "category",
                    "value": ""
                },
                {
                    "name": "description",
                    "value": ""
                }
            ]
        },
        "url": "https://example.com/api/v1/pipelines/2/"
    },

    'https://exmaple.com/api/v1/pipelines/2/pipings/': {
        "collection_links": {
            "pipeline": "https://example.com/api/v1/pipelines/2/"
        },
        "count": 8,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 4,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": None,
                "url": "https://example.com/api/v1/pipelines/pipings/4/"
            },
            {
                "id": 5,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/4/",
                "previous_id": 4,
                "url": "https://example.com/api/v1/pipelines/pipings/5/"
            },
            {
                "id": 6,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/4/",
                "previous_id": 4,
                "url": "https://example.com/api/v1/pipelines/pipings/6/"
            },
            {
                "id": 7,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/5/",
                "previous_id": 5,
                "url": "https://example.com/api/v1/pipelines/pipings/7/"
            },
            {
                "id": 8,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/6/",
                "previous_id": 6,
                "url": "https://example.com/api/v1/pipelines/pipings/8/"
            },
            {
                "id": 9,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/6/",
                "previous_id": 6,
                "url": "https://example.com/api/v1/pipelines/pipings/9/"
            },
            {
                "id": 10,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/6/",
                "previous_id": 6,
                "url": "https://example.com/api/v1/pipelines/pipings/10/"
            },
            {
                "id": 11,
                "pipeline": "https://example.com/api/v1/pipelines/2/",
                "pipeline_id": 2,
                "plugin": "https://example.com/api/v1/plugins/4/",
                "plugin_id": 4,
                "previous": "https://example.com/api/v1/pipelines/pipings/10/",
                "previous_id": 10,
                "url": "https://example.com/api/v1/pipelines/pipings/11/"
            }
        ]
    },

    'https://example.com/api/v1/pipelines/2/parameters/': {
        "count": 40,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 8,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/4/",
                "plugin_piping_id": 4,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": None,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/8/",
                "value": "0"
            },
            {
                "id": 7,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/4/",
                "plugin_piping_id": 4,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": None,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/7/",
                "value": "a"
            },
            {
                "id": 10,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/5/",
                "plugin_piping_id": 5,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/10/",
                "value": "0"
            },
            {
                "id": 9,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/5/",
                "plugin_piping_id": 5,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/9/",
                "value": "b"
            },
            {
                "id": 12,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/6/",
                "plugin_piping_id": 6,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/12/",
                "value": "0"
            },
            {
                "id": 11,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/6/",
                "plugin_piping_id": 6,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/11/",
                "value": "c"
            },
            {
                "id": 14,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/7/",
                "plugin_piping_id": 7,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 5,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/14/",
                "value": "0"
            },
            {
                "id": 13,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/7/",
                "plugin_piping_id": 7,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 5,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/13/",
                "value": "d"
            },
            {
                "id": 16,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/8/",
                "plugin_piping_id": 8,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/16/",
                "value": "0"
            },
            {
                "id": 15,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/8/",
                "plugin_piping_id": 8,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/15/",
                "value": "e"
            },
            {
                "id": 18,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/9/",
                "plugin_piping_id": 9,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/18/",
                "value": "0"
            },
            {
                "id": 17,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/9/",
                "plugin_piping_id": 9,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/17/",
                "value": "f"
            },
            {
                "id": 20,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/10/",
                "plugin_piping_id": 10,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/20/",
                "value": "0"
            },
            {
                "id": 19,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/10/",
                "plugin_piping_id": 10,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/19/",
                "value": "g"
            },
            {
                "id": 22,
                "param_id": 11,
                "param_name": "sleepLength",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/11/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/11/",
                "plugin_piping_id": 11,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 10,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/22/",
                "value": "0"
            },
            {
                "id": 21,
                "param_id": 9,
                "param_name": "prefix",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/9/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/11/",
                "plugin_piping_id": 11,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 10,
                "type": "string",
                "url": "https://example.com/api/v1/pipelines/string-parameter/21/",
                "value": "h"
            },
            {
                "id": 4,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/4/",
                "plugin_piping_id": 4,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": None,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/4/",
                "value": 1
            },
            {
                "id": 5,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/5/",
                "plugin_piping_id": 5,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/5/",
                "value": 1
            },
            {
                "id": 6,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/6/",
                "plugin_piping_id": 6,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/6/",
                "value": 1
            },
            {
                "id": 7,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/7/",
                "plugin_piping_id": 7,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 5,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/7/",
                "value": 1
            },
            {
                "id": 8,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/8/",
                "plugin_piping_id": 8,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/8/",
                "value": 1
            },
            {
                "id": 9,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/9/",
                "plugin_piping_id": 9,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/9/",
                "value": 1
            },
            {
                "id": 10,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/10/",
                "plugin_piping_id": 10,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/10/",
                "value": 1
            },
            {
                "id": 11,
                "param_id": 12,
                "param_name": "dummyInt",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/12/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/11/",
                "plugin_piping_id": 11,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 10,
                "type": "integer",
                "url": "https://example.com/api/v1/pipelines/integer-parameter/11/",
                "value": 1
            },
            {
                "id": 4,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/4/",
                "plugin_piping_id": 4,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": None,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/4/",
                "value": 1.1
            },
            {
                "id": 5,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/5/",
                "plugin_piping_id": 5,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/5/",
                "value": 1.1
            },
            {
                "id": 6,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/6/",
                "plugin_piping_id": 6,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/6/",
                "value": 1.1
            },
            {
                "id": 7,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/7/",
                "plugin_piping_id": 7,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 5,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/7/",
                "value": 1.1
            },
            {
                "id": 8,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/8/",
                "plugin_piping_id": 8,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/8/",
                "value": 1.1
            },
            {
                "id": 9,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/9/",
                "plugin_piping_id": 9,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/9/",
                "value": 1.1
            },
            {
                "id": 10,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/10/",
                "plugin_piping_id": 10,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/10/",
                "value": 1.1
            },
            {
                "id": 11,
                "param_id": 13,
                "param_name": "dummyFloat",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/13/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/11/",
                "plugin_piping_id": 11,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 10,
                "type": "float",
                "url": "https://example.com/api/v1/pipelines/float-parameter/11/",
                "value": 1.1
            },
            {
                "id": 4,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/4/",
                "plugin_piping_id": 4,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": None,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/4/",
                "value": False
            },
            {
                "id": 5,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/5/",
                "plugin_piping_id": 5,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/5/",
                "value": False
            },
            {
                "id": 6,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/6/",
                "plugin_piping_id": 6,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 4,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/6/",
                "value": False
            },
            {
                "id": 7,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/7/",
                "plugin_piping_id": 7,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 5,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/7/",
                "value": False
            },
            {
                "id": 8,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/8/",
                "plugin_piping_id": 8,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/8/",
                "value": False
            },
            {
                "id": 9,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/9/",
                "plugin_piping_id": 9,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/9/",
                "value": False
            },
            {
                "id": 10,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/10/",
                "plugin_piping_id": 10,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 6,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/10/",
                "value": False
            },
            {
                "id": 11,
                "param_id": 10,
                "param_name": "b_ignoreInputDir",
                "plugin_id": 4,
                "plugin_name": "pl-simpledsapp",
                "plugin_param": "https://example.com/api/v1/plugins/parameters/10/",
                "plugin_piping": "https://example.com/api/v1/pipelines/pipings/11/",
                "plugin_piping_id": 11,
                "plugin_version": "2.0.2",
                "previous_plugin_piping_id": 10,
                "type": "boolean",
                "url": "https://example.com/api/v1/pipelines/boolean-parameter/11/",
                "value": False
            }
        ]
    }
}
