from automationfx import *
from migrate_client import MigrateClient
from smtp_client import SmtpClient

migrate_client = MigrateClient()
email_client = SmtpClient()

# settings.json file should be a configured to use an AutomationFX instance (valid ApiKey)
# process_all_records if Flase, this will only process remaining and failed migrations.
migrate_client.migrate(process_all_records=False, input_file="example_migration.csv")

# Used for sending Activation Code to end users. Requires UCM 12.5+ and Device Default 'Onboarding Method' for model should be configured to 'Activation Code'
# smtp_settings.json file should have valid smtp confgurations (sample text and html templates exist in the repository)
migrate_client.send_activation_email(email_client)
