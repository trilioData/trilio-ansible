
from jinja2 import Template

# Simulate variables from Ansible run
vars = {
    'trilio_kubernetes_backupplan_name': 'smoketest-backupplan',
    'trilio_kubernetes_backupplan_override': False, 
    'trilio_kubernetes_backupplan_type': 'ns',
    'item': 'ansible-demo1'
}

# The failing template
template_str = """
{{ trilio_kubernetes_backupplan_name 
   if (trilio_kubernetes_backupplan_override | bool) 
   else (item ~ '-' ~ trilio_kubernetes_backupplan_type) }}
"""

try:
    t = Template(template_str)
    # Jinja2 in Python doesn't have the 'bool' filter by default in the same way Ansible does if not added, 
    # but let's see if we can reproduce basic concatenation issues or logic.
    # We'll mock the bool filter.
    def bool_filter(v):
        return bool(v)
    
    t.environment.filters['bool'] = bool_filter
    
    result = t.render(**vars)
    print(f"Result: '{result.strip()}'")
except Exception as e:
    print(f"Error: {e}")
