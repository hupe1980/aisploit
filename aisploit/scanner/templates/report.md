## ScanReport
| RunID | CreatedAt |
|-------|-----------| 
|{{ run_id }}|{{ created_at }}|

{% if issues_by_category|length == 0 %}
No issues!
{% else %}
{% for category, issues in issues_by_category.items() -%}
### {{ category.name }} issues
> {{ category.description }}

| Prompt | Converter | Response | RTT (seconds) |
|--------|-----------|----------|---------------|
{% for issue in issues -%}
|{{ issue.send_report_entry.prompt }}|{{ issue.send_report_entry.converter }}|{{ issue.send_report_entry.response|replace('\n', '<br>') }}| {{ issue.send_report_entry.round_trip_time }} |
{% endfor %}
{% endfor %}
{% endif %}