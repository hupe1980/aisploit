## ScanReport 
> RunID: {{ run_id }}

{% if issues_by_category|length == 0 %}
No issues!
{% else %}
{% for category, issues in issues_by_category.items() -%}
### {{ category.name }} issues
> {{ category.description }}

| Prompt | Converter | Response |
|--------|-----------|----------|
{% for issue in issues -%}
|{{ issue.send_report_entry.prompt }}|{{ issue.send_report_entry.converter }}|{{ issue.send_report_entry.response }}|
{% endfor %}
{% endfor %}
{% endif %}