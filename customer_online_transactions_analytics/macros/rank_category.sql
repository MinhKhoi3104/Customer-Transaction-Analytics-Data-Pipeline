{% macro rank_category(rank_column) %}
    case 
        when {{ rank_column }} <= max({{ rank_column }}) over () / 3 then 'Gold'
        when {{ rank_column }} >  max({{ rank_column }}) over () / 3
         and {{ rank_column }} <= max({{ rank_column }}) over () * 2/3 then 'Silver'
        when {{ rank_column }} >  max({{ rank_column }}) over () * 2/3 then 'Bronze'
        else null
    end
{% endmacro %}

