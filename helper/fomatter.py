

def get_email_content(sender_mail, recipient_mails, subject, reference_mails, body):
    headers = f"From: {sender_mail}\r\n"
    headers += f"To: {', '.join(recipient_mails)}\r\n" 
    headers += f"Subject: {subject}\r\n"
    headers += f"References: {reference_mails}\r\n"
    headers += f"In-Reply-To: {reference_mails}\r\n"
    email_message = headers + "\r\n" + body  
    return email_message.encode()