import os
import time
import base64
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import telebot

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Replace with your Telegram Bot token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Get email service
def get_gmail_service():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  service = build("gmail", "v1", credentials=creds)
  return service


# Get the list of emails in the inbox
def list_messages(service, user_id='me'):
  response = service.users().messages().list(userId=user_id, maxResults=3).execute()
  # response = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
  messages = response.get("messages", [])
  
  return messages


# Get email details
def get_message(service, message_id, user_id='me'):
  message = service.users().messages().get(userId=user_id, id=message_id).execute()
  return message


def send_telegram_message(sender, snippet):
  bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
  bot.send_message(chat_id=CHAT_ID, text=f"New email from：{sender}\n\n{snippet}") # Send a message to the specified chat ID with the sender's name and decoded message data
  print('\n\nSend Successful =W=')


def check_new_emails(gmail_service):
  processed_emails = set()  # Initialize a set to store processed email IDs
  skip_flag = False # Flag to skip processing the first batch of emails
  
  while True:
    messages = list_messages(gmail_service)
    for message in messages:
      message_id = message['id']
      if not skip_flag:
        processed_emails.add(message_id)
      
      if message_id not in processed_emails:
        msg = get_message(gmail_service, message_id)
        payload = msg['payload']
        headers = payload['headers']
        for header in headers:
          if header['name'] == 'From':
            sender = header['value']
            print("Sender: ", sender)
        snippet = msg['snippet']
        print('Snippet: ', snippet)
        
        send_telegram_message(sender, snippet)  # Send notification to Telegram
        processed_emails.add(message_id)
        
        # msg_data = msg['payload']['parts'][0]['parts'][0]['body']['data']
        # decoded_msg_data = base64.urlsafe_b64decode(msg_data).decode('utf-8')
        processed_emails.add(message_id)
    skip_flag = True
    time.sleep(60)  # Wait for 60 seconds before checking for new emails again

def main():
  gmail_service  = get_gmail_service()
  check_new_emails(gmail_service)

if __name__ == "__main__":
  main()