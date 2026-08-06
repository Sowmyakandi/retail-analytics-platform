{% macro generate_schema_name(custom_schema_name, node) -%}

    {#-
        By default dbt prefixes custom schemas with the target schema
        (e.g. target=main + custom=raw -> main_raw), which is confusing
        for a small project with only a handful of schemas. This override
        uses the custom schema name as-is when one is set, and falls back
        to the target's default schema otherwise.
    -#}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
