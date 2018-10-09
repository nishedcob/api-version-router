# api-version-router
Prototype API Version Router Microservice

Maps API versions for clients (known as `app`) to backends (known as `server`). By default, the rules (written for testing purposes) are:
```
app_version='DEFAULT' => server_version='DEFAULT' (server_domain='api.domain.com')
app_version='v1' => server_version='v2' (server_domain='apiv3.domain.com')
app_version='v2' => server_version='v1' (server_domain='apiv2.domain.com')
app_version='v3' => server_version='v3' (server_domain='apiv1.domain.com')
```
App versions who have no rule will fall back on the `DEFAULT` app rule.

These rules can be edited and/or replaced in `migrate.py`.

## API Endpoints:

`GET /<string:app_version>`
Returns `server_version` and `server_domain` that should be used.

For example, with the current ruleset:
`GET /v1`
should return:
```
{"server_version": "v2", "server_domain": "apiv3.domain.com", "app_version": "v1"}
```
