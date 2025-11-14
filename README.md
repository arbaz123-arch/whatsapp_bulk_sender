####  WhatsApp Bulk Sender (Python + Selenium)

A simple and lightweight automation tool that helps you send WhatsApp messages and attachments in bulk using data from a CSV file. It uses Selenium to open WhatsApp Web in an automated Chrome browser, search for each phone number, load the chat, and send personalized messages without any manual typing.

The tool also supports sending images, PDFs, and documents by reading their paths directly from the CSV file. This helps automate repetitive WhatsApp messaging tasks with minimum effort and without relying on any unofficial API.

# Features:-

Reads name, phone, message, and attachment paths from a CSV file
Opens WhatsApp Web through Selenium and loads each chat
Sends personalized text messages using placeholders
Sends attachments (images, PDFs, documents) automatically
Error handling for missing chats or invalid files
Works without manually typing captions


# Requirements:-

Python 3.x
Selenium
Chrome Browser
ChromeDriver (matching your Chrome version)


# How It Works:-

User logs into WhatsApp Web once.
Script loads the CSV file.
For each row, it opens the chat, formats the message, and sends the text and attachment.
Continues until all entries are processed.


# Use Cases:-

Bulk greetings or announcements
Client communication
Sending documents or images to multiple recipients
Automated follow-ups