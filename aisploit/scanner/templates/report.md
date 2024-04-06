## ScanReport 
> RunID: {{ run_id }}

{% for category, issues in issues_by_category.items() -%}
### {{ category.name }} issues
> {{ category.description }}

{% for issue in issues -%}
| Prompt | Converter | Response |
|--------|-----------|----------|
|{{ issue.prompt }}|{{ issue.converter }}|{{ issue.response }}|
{% endfor %}

{% endfor %}