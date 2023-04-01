{% macro convert_date(date_field) %}
   FORMAT_TIMESTAMP('%Y-%m-%d', PARSE_TIMESTAMP('%d %b %Y %T %Z', {{ date_field }}))
{% endmacro %}