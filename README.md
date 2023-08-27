# Telegram Chatbot - IS238 Project SY2022

### About the Project
The team has built a **Telegram chatbot** that has the capability to send and receive email messages using a Gmail account. The chatbot will cater to multiple users that are part of a Telegram chat group. When one of the chat group members responds to the message thread, an email will be sent back to the email's sender. All email messages are grouped using the sender's email address. Email attachments and other text formatting are stripped. To give different users an idea which users are involved in the conversation, the username or name of the member responding to the message will be appended to the email details. Lastly, a background job that runs every 5 seconds has been incorporated into the system to check for incoming messages from the email.

**Python** was the programming language of choice by the group to create the Telegram Bot. The built-in **imap** library of Python was used to read email messages and also to send replies from the Telegram chat group. The **BlockingScheduler** class was used to run a job that reads the inbox of the email and forwards new messages to the Telegram chat group. The **Python-Telegram-Bot** package was used to get access to Telegram Bot functionalities such as sending messages, confirming user actions and providing custom commands to help users use the bot. In addition, the system is also using **Redis** (an open-source, in-memory, and key-value data store) to save and retrieve data about the senders, which will be used to group messages coming from the same sender. To make the solution align with security standards, the **Python-DotEnv** package was also installed to manage sensitive information needed to run the bot such as the email account and password and the chatbot token and should be configured manually in the deployment server. **Docker** was also used to containerize the application to make it easier to run the application and to ensure that the application has the same environment in every installation. The Telegram bot can be easily installed on an **AWS EC2** instance (running on Ubuntu operating system), following the **Setup Guide** of this README. 


### Members

| Name                          | Email                     |
| -------------                 |:-------------:            |
| Darryl Anaud                  | dcanaud@up.edu.ph         |
| Federick Joe Fajardo          | fpfajardo1@up.edu.ph      |
| Christian Gaylord Gaylan      | cdgaylan1@up.edu.ph       |
| Dave Infante                  | juinfante@up.edu.ph       |
| Gimelle Ann Dela Peña         | gsdelapena@up.edu.ph      |

### Requirements

- A gmail account with app password setup (https://support.google.com/accounts/answer/185833?hl=en)
- A telegram bot (https://defstudio.github.io/telegraph/quickstart/new-bot)

### Setup Guide (from a fresh Ubuntu Installation)

- Install dependencies ```sudo apt update && sudo apt install -y docker docker-compose```
- Clone the repository ```git clone https://github.com/juinfanteUP/is238-g2-project.git```
- Go inside the project folder ```cd is238-g2-project```
- Set your gmail password and telegram bot credentials in the .env file. ```nano .env```. Refer to the sample .env format below:

*Example:*
```
MAIL_USER=test@gmail.com
MAIL_PASSWORD=mypassword
TELEGRAM_BOT_NAME=@my_bot_name
TELEGRAM_BOT_TOKEN=1234567890:AjfkvldiJJKi3urhsbv-B9igjglsJKLO1HB
```

- Run the application using docker-compose ```sudo docker-compose up --build -d --remove-orphans```


### Usage Guide

- Create a telegram group chat with the bot as a member and a welcome message with further instructions will be given
- Enter the `/start` command to set the chat group as the receiver for the emails.
- Set the `Chat History` setting to `Visible` to enable threaded replies

Other available commands:
- `/commands` - List the available commands
- `/help` - Display instructions on how to use the bot
- `/chatid` - Displays the chat id
- `/status` - Check if the bot is ready to use

**Telegram Bot Usage Instructions**

1. Send an email to the system's email (You may configure this in the .env file), and it will be forwarded to this chat group
2. In the Telegram app, tap 'Reply' on the message and enter your reply message to send it back to the email sender
3. A confirmation prompt will show. Tap on 'Yes' to send or 'No' to cancel
4. Replying to the same email sender will be grouped on the same thread (You don't have to scroll to the sender's first message)
5. New emails from the same sender will also be grouped together
6. Tap on 'View Replies' on the sender's very first email message to view all the messages in the thread
7. Have fun!"