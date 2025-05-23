from twilio.rest import Client
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def send_whatsapp_twilio(summaries_path):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    # Load summaries
    if not os.path.exists(summaries_path):
        print("No summary file found.")
        return

    df = pd.read_csv(summaries_path)

    # Create a message with the top 3 cluster summaries
    summaries = df.head().apply(lambda row: f"{row['summary']}", axis=1).tolist()
    summary_text = "\n\n".join(summaries)

    message_body = f"Your News Summary Digest\n\n{summary_text}"

    # Send WhatsApp message
    message = client.messages.create(
        from_=os.getenv("TWILIO_SANDBOX_NUMBER"),  # Twilio sandbox number
        body=message_body,
        to=os.getenv("TWILIO_RECIPIENT_NUMBER")
    )
    print(message.sid)

if __name__ == "__main__":
    summaries_path = 'data/clustered/cluster_summaries.csv'
    send_whatsapp_twilio(summaries_path)