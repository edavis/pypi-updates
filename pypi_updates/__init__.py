import os
import time
import postmark
from pkgtools.pypi import PyPIXmlRpc
from jinja2 import Environment, PackageLoader
from email.utils import formatdate

LAST_UPDATE_STATE_FILE = "/tmp/pypi-last-update"
TO_ADDR = "pypi.updates@librelist.com"
SENDER_ADDR = "Eric Davis <ed@npri.org>"
POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']

template_env = Environment(loader=PackageLoader('pypi_updates'))
pypi = PyPIXmlRpc()

def get_last_update_timestamp():
    state_file = LAST_UPDATE_STATE_FILE
    if not os.path.exists(state_file):
        with open(state_file, "w") as fp:
            fp.write("")
        return int(time.time() - 60*60)
    else:
        return int(os.stat(state_file).st_mtime)

def get_updates(timestamp):
    updates = pypi.changelog(timestamp)
    for info in updates:
        if info[-1] == "new release":
            yield info[:3]

def render(template, context):
    template = template_env.get_template(template)
    return template.render(**context)

def build_email(info):
    (name, version, timestamp) = info
    release_data = pypi.release_data(name, version)
    release_data['date'] = formatdate(timestamp)

    mail = postmark.PMMail()
    mail.api_key = POSTMARK_API_KEY
    mail.to = TO_ADDR
    mail.sender = SENDER_ADDR
    mail.subject = render('subject.txt', release_data)
    mail.text_body = render('body.txt', release_data)
    return mail

def main():
    timestamp = get_last_update_timestamp()
    updates = list(get_updates(timestamp))

    if not updates:
        return

    batch = postmark.PMBatchMail()
    batch.api_key = POSTMARK_API_KEY

    for update in updates:
        message = build_email(update)
        print message.subject
        batch.add_message(message)

    batch.send()

    last_update = updates[-1][2]
    os.utime(LAST_UPDATE_STATE_FILE, (last_update, last_update))
