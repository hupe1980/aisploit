## ScanReport 
> RunID: {{ run_id }}

{% if issues_by_category|length == 0 %}
No issues!
{% else %}
{% for category, issues in issues_by_category.items() -%}
### {{ category.name }} issues
> {{ category.description }}

{% for issue in issues -%}
| Prompt | Converter | Response |
|--------|-----------|----------|
|{{ issue.prompt }}|{{ issue.converter }}|{{ issue.response }}|
{% endfor %}
{% endfor %}
{% endif %}