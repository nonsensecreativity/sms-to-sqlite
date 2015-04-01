from xml.dom import minidom
import re
import sqlite3

dom = minidom.parse('messages.xml')
messages = dom.getElementsByTagName('sms')

# Create the database and its tables
db = sqlite3.connect('messages.db')
cursor = db.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS messages (
       message_id INTEGER PRIMARY KEY,
       person_name INTEGER,
       phone_number VARCHAR(20),
       message TEXT,
       date_sent DATETIME,
       date DATETIME,
       inbound BOOLEAN
    )
    """
)

for message in messages:
    cursor.execute(
        """
        INSERT INTO messages (
           person_name,
           phone_number,
           message,
           date_sent,
           date,
           inbound
        ) VALUES (
           ?,
           ?,
           ?,
           datetime(?, 'unixepoch'),
           datetime(?, 'unixepoch'),
           ?
        )
        """,
        (
            message.attributes['contact_name'].value,
            re.sub("[^0-9]", "", message.attributes['address'].value),
            message.attributes['body'].value,
            message.attributes['date_sent'].value[0:-3] or None,
            message.attributes['date'].value[0:-3] or None,
            message.attributes['type'].value == '1',
        )
    )

db.commit()
