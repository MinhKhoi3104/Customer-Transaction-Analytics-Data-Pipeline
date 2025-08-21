{% macro positive_quantity(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} <= 0
   or {{ column_name }} is null

{% endmacro %}
