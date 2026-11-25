from db import initialize_database, save_report, get_latest_reports

initialize_database()

save_report(
    domain="Test Domain",
    report="This is a test report.",
    sources=[
        {
            "title": "Test Source",
            "url": "https://example.com"
        }
    ]
)

reports = get_latest_reports()

print("\nSaved Reports:")

for report in reports:
    print(report)

print("\nDATABASE TEST: SUCCESS")

