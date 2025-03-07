(plugins-snowflake)=

# Snowflake

```{eval-rst}
.. tags:: Integration, Data, Advanced, SQL
```

Flyte backend can be connected with snowflake service. Once enabled it can allow you to query a snowflake service.
This section will provide how to use the Snowflake Query Plugin using flytekit python.

## Installation

To use the flytekit snowflake plugin simply run the following:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-snowflake
```

## No Need of a dockerfile

This plugin is purely a spec. Since SQL is completely portable there is no need to build a Docker container.

## Configuring the backend to get snowflake working

1. Make sure to add "snowflake" in `tasks.task-plugins.enabled-plugin` in [enabled_plugins.yaml](https://github.com/flyteorg/flyte/blob/master/deployment/sandbox/flyte_generated.yaml#L2296)
2. Add snowflake JWT token to Flytepropeller. [here](https://docs.snowflake.com/en/developer-guide/sql-api/guide.html#using-key-pair-authentication) to see more detail to setup snowflake JWT token.

```bash
kubectl edit secret -n flyte flyte-propeller-auth
```

Configuration will be like below

```bash
apiVersion: v1
data:
  FLYTE_SNOWFLAKE_CLIENT_TOKEN: <JWT_TOKEN>
  client_secret: Zm9vYmFy
kind: Secret
metadata:
  annotations:
    meta.helm.sh/release-name: flyte
    meta.helm.sh/release-namespace: flyte
...
```

```{auto-examples-toc}
snowflake
```
