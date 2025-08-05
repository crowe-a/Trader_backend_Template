from O365 import Account
import re
from backend.config import CLIENT_ID,CLIENT_SECRET
def checkmail():
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET

    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)

    if not account.is_authenticated:
        account.authenticate(
            scopes=['https://graph.microsoft.com/Mail.Read'],
            redirect_uri='https://login.microsoftonline.com/common/oauth2/nativeclient'
        )

    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()

    messages = inbox.get_messages(limit=5, order_by='receivedDateTime DESC')

    verification_code = None

    for message in messages:
        body = message.get_body_text() or ""
        match = re.search(r"\d{6}", body)  # kelime sınırı kaldırıldı
        if match:
            verification_code = match.group(0)
            break

    if verification_code:
        print("Doğrulama kodu:", verification_code)
    else:
        print("Kod bulunamadı.")
    return verification_code
# checkmail()