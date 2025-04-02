# some shared variables.
# Quick & dirty
server_fields = {'server_hostname': {'type': 'string'},
                 'server_port': {'type': 'number'},
                 'case_sensitive_url': {'type': 'yesno', 'max_version': "10.0.6.0"},
                 'case_insensitive_url': {'type': 'yesno', 'min_version': "10.0.6.0"},
                 'http_port': {'type': 'number'},
                 'local_ip': {'type': 'string'},
                 'query_contents': {'type': 'string', 'alt_name': 'query_content_url'},
                 'server_dn': {'type': 'string'},
                 'server_uuid': {'type': 'ignore'},
                 'virtual_hostname': {'type': 'string', 'alt_name': 'virtual_junction_hostname'},
                 'windows_style_url': {'type': 'yesno'},
                 'current_requests': {'type': 'ignore'},
                 'total_requests': {'type': 'ignore'},
                 'operation_state': {'type': 'ignore'},
                 'server_state': {'type': 'ignore'},
                 'priority': {'type': 'number', 'min_version': "10.0.2.0"},
                 'server_cn': {'type': 'string', 'min_version': "10.0.2.0"}}
