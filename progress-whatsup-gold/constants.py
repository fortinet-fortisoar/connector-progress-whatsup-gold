"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

endpoints = {
    "CPU Utilization Report": 'cpu-utilization',
    "Disk Utilization Report": 'disk-utilization',
    "Memory Utilization Report": 'memory-utilization',
    "Ping Availability Report": 'ping-availability',
    "Ping Response Time Report": 'ping-response-time',
    "State Change Timeline Report": 'state-change'
}

report_duration = {
    "Today": "today",
    "Last Polled": "lastPolled",
    "Yesterday": "yesterday",
    "Last Week": "lastWeek",
    "Last Month": "lastMonth",
    "Last Quarter": "lastQuarter",
    "Week-to-Date": "weekToDate",
    "Month-to-Date": "monthToDate",
    "Quarter-to-Date": "quarterToDate",
    "Last X Seconds": "lastNSeconds",
    "Last X Minutes": "lastNMinutes",
    "Last X Hours": "lastNHours",
    "Last X Days": "lastNDays",
    "Last X Weeks": "lastNWeeks",
    "Last X Months": "lastNMonths",
    "Custom Duration": "custom"
}
