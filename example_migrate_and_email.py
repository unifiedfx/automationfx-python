from automationfx import *
from migrate_client import MigrateClient
from smtp_client import SmtpClient

migrate_client = MigrateClient()
email_client = SmtpClient()

# settings.json file should be configured to use an existing AutomationFX(MigrationFX) instance (valid ApiKey, Host etc..)
# ignore_status parameter value "True" will processs all records/rows in the input csv file, value "False" will only process remaining and failed records/rows.
migrate_client.migrate(ignore_status=False, input_file="example_migration.csv")

# Used for sending Activation Code to end users. Requires UCM 12.5+ and Device Default 'Onboarding Method' for model should be configured to 'Activation Code'
# smtp_settings.json file should be configured with valid smtp settings (sample text and html templates exist in the repository)
migrate_client.send_activation_email(email_client)
