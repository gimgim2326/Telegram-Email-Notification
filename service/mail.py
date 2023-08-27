import imaplib
import requests
import email
from email import policy 
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from helper.config import get_telegram_uri, imap_config, mail_config, telegram_config
from helper.fomatter import get_email_content
import redis


def handle_response(recipient, text) -> str:
    send_email( recipient, text)
    return "Email sent to " + recipient


def send_email(recipient, text):
    search_email(recipient, text) #search first email by the sender
    ''' Commented out --- 
    from_email = f"{mail_config['name']} <{mailConfig['mail']}>"
    to_emails = [recipient]
    body = text
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n" 
    headers += f"Subject: IS238\r\n"
    email_message = headers + "\r\n" + body

    #Connect
    smtp_server = SMTP_SSL(smtp_host, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1) 
    smtp_server.login(email_user, email_pass)
    smtp_server.sendmail(from_email, to_emails, email_message)

    #Disconnect
    smtp_server.quit()
    '''

def read_email() -> None:
    r = redis.Redis(host='redis', port=6379, db=0)
    
    if r.get("chat_id") is None:
        print("Chat id is not set. Enter the /start command first.")
        return
    
    print(" read_email invoked ")
    imap = imaplib.IMAP4_SSL(imap_config["mail"], imap_config["port"])
    imap.login(mail_config['mail'], mail_config['secret'])
    imap.select("inbox")
    status, data = imap.search(None, "(UNSEEN)")
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = imap.fetch(i, "(RFC822)")

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1], policy = policy.default)
                mail_from = message["from"]
                mail_subject = message["subject"]
                
                if message.is_multipart():
                    mail_content = ""
                    for m in message.walk():
                        if (m.get_content_type() == 'text/plain') and (m.get('Content-Disposition') is None):
                            mail_content += m.get_payload()
                            break
                else:
                    mail_content = message.get_payload(decode=True)
                    mail_content = mail_content.decode('utf-8')
                
                print("----------")
                print(f"From: {mail_from}")
                print(f"Subject: {mail_subject}")
                print("----------")
                
                f_msg = "From: " + mail_from + "\n" + "Subject: " + mail_subject + "\n" + "\nContent: \n" + mail_content
                
                chat_id = str(r.get("chat_id"), 'utf-8')
                key = mail_from.split("<", 1)[1].split(">", 1)[0] + "." + chat_id
                set_cache = False
                
                if r.get(key) is None:
                    reply_message_id = None
                    set_cache = True
                else:
                    reply_message_id = str(r.get(key), 'utf-8')
                
                uri = get_telegram_uri(f_msg, telegram_config['token'], chat_id, reply_message_id)
                response = requests.get(uri).json()
                
                if response["ok"] != True:
                    if response["description"] == "Bad Request: replied message not found":
                        uri = get_telegram_uri(f_msg, telegram_config['token'], chat_id)
                        retry_response = requests.get(uri).json()
                        r.set(key, retry_response['result']['message_id'])
                else:
                    if set_cache:
                        r.set(key, response['result']['message_id'])
    imap.close()
    imap.logout()


def search_email(email_sender, reply_body):
    print(" search_email invoked ")

    imap = imaplib.IMAP4_SSL(imap_config["mail"], imap_config["port"])
    imap.login(mail_config['mail'], mail_config['secret'])
    imap.select()
    status, data = imap.search(None, f"(HEADER FROM {email_sender})")

    if status == 'OK':
        if data[0]:
            mid = data[0].split()[0]
            status, data = imap.fetch(mid, "(RFC822)")
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    email_details = email.message_from_bytes(response_part[1],policy = policy.default)
                    from_email = f"{mail_config['name']} <{mail_config['mail']}>"
                    to_emails = [ email_details["from"] ]
                    subject = email_details["subject"]
                    ref_email = email_details["Message-ID"]
                    email_message = get_email_content(from_email, to_emails, subject, ref_email, reply_body)                  

                    #Connect
                    smtp_server = SMTP_SSL(mail_config['host'], port = SMTP_SSL_PORT)
                    smtp_server.set_debuglevel(1)  # Show SMTP server interactions
                    smtp_server.login(mail_config['mail'], mail_config['secret'])
                    smtp_server.sendmail(from_email, to_emails, email_message)

                    #Disconnect
                    smtp_server.quit()
                    break #reply to first email only
        else:
            print('No results')
    else:
        print('unable to search', data)

    imap.close()
    imap.logout()

