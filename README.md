# Servello

Servello is a developing, flask server that will take a configuration file and will build a server automatically. It aims to help creating quick servers for testing.

# Installation

You can install Servello using pip:

```bash
# Install from source
git clone https://github.com/carrerasrodrigo/servello.git
cd servello
pip install -e .

# or
pip install git+https://github.com/carrerasrodrigo/servello.git#egg=servell
```

# Available Commands

After installation, the following command will be available in your terminal:

```bash
servello --config <path-to-config-file>
```

Options:
- `--config`: Path to your JSON configuration file (required)

# How to use it
```
> servello --config file.json
 * Serving Flask app 'Servello Test' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
```
# Configuration File
```
{
    "server_name": "Servello Test",
    "urls": [
        {
            "method_list": ["GET", "POST"],
            "pattern": "/url/",
            "content": "some content",
            "content_file": "path-to-a-file/server-content.txt",
            "content_type": "application/json",
            "status": 200,
            "headers": [["X1", "1"], ["X2", "2"]]
        },
        {
            "pattern": "/url2/",
            "content": "some content",
            "content_type": "application/json",
            "status": 200,
            "headers": []
        },
        {
            "pattern": "/url3/",
            "content": "{}"
        }
    ]

}
```
`server_name` the name of the server
`urls` is a list of pages to define, each url has the following parameters
`urls.pattern` required, the pattern for the url that we want to use. Duplicated patterns will be ignored.
`urls.method_list` optional, a list of allowed method for the request. by default is `["GET"]`
`urls.content` required, the content that we want to return once the pattern match.
`urls.content_file` required, the path of a file that will have the content that we want to return once the pattern match. If `content_file` is defined `content` will be ignored.
`urls.content_type` optional, the content type that will be applied to the response. By default it `application/json`
`urls.status` optional, status code of the response, by default is `200`
`urls.headers` optional, a list of headers that will be attached to the response. Each header has to be defined like a list `["HEADER NAME", "HEADER VALUE"]`. By default is an empty list.

# Testing
```
> pytest tests
```
# Changelog
- 0.0.1 Added regex in url
- 0.0.0 Initial version
