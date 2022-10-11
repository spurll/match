from email.mime.text import MIMEText
from smtplib import SMTP


# Each notification function should take a list of User objects.


def email(users, host, user, password, addendum=None):
    if not users: return

    # Build message.
    matches = [
        f'<tr><td style="min-width: 100px;">{u.name}</td>'
        f'<td style="min-width: 150px;">{u.match_name}</td></tr>'
        for u in users
    ]
    header = (
        '<thead><tr style="font-weight: bold;">'
        '<td style="min-width: 100px;">User</td>'
        '<td style="min-width: 100px;">Match</td>'
        '</tr></thead>'
    )
    message = (
        '<p>Match complete! Here are the results:</p>'
        f'<table style="border: solid 2px black;">{header}'
        + '\n'.join(matches) + '</table>'
    )

    if addendum:
        message += '<p>{}</p>'.format(addendum)

    message = MIMEText(message, 'html')
    message['subject'] = 'Match: Results'
    message['to'] = ', '.join(u.email for u in users)

    # Set up SMTP.
    smtp = SMTP(host)
    smtp.starttls()
    smtp.login(user, password)

    print([u.email for u in users])

    # Send message.
    smtp.sendmail(user, [u.email for u in users], message.as_string())

    smtp.close()

