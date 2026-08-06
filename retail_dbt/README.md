# retail_dbt

Staging + mart models for the retail analytics platform. See the top-level
repo README for the full pipeline context.

## Quickstart (DuckDB, no cloud credentials)

```bash
pip install -r requirements.txt
dbt seed --profiles-dir ./ci_profiles
dbt run  --profiles-dir ./ci_profiles
dbt test --profiles-dir ./ci_profiles
```

## Project layout

- `seeds/` — copies of `data/raw/*.csv`, loaded into a `raw` schema so the
  project is runnable with zero cloud dependencies.
- `models/staging/` — one cleaned view per source table.
- `models/marts/` — `dim_customers`, `dim_products`, `fct_orders`,
  `fct_payments`, `fct_inventory`. These are what Power BI (or any BI tool)
  should query.
- `ci_profiles/profiles.yml` — DuckDB profile used by CI and local dev.
- `macros/get_custom_schema.sql` — keeps schema names predictable
  (`raw`, `staging`, `marts`) instead of dbt's default
  `<target_schema>_<custom_schema>` prefixing.

## Production target

Point dbt at Snowflake instead of DuckDB by configuring a `prod` target (see
`retail_dbt` profile block referenced in the top-level `.env.example`) with
`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, etc., then run
with `--target prod`.
