# CommSecRecords

This project contains automation which parses through emails received from CommSec.
The emails have their transactions extracted and outputs in CSV form so that you can put this data into a spreadsheet.

This is mainly for tracking your transactions of shares and ETFs so you can easily collate them during tax time.

## Setup

1. Set up a filter on your email to put all your CommSec emails into a particular folder
2. Download all the emails which you want to have your transactions extracted from, and download them into a folder called Emails
3. Validate that all emails are of the extension .eml
4. Run the following command

```
python3 parse_emails.py Emails
```

## Disclaimer 

This was hacked in 2 hours and probably does not cover all edge cases.
