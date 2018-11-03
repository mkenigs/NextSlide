# Specifications

## Setup
Add configuration, script mainwindow.py  
Create new venv and install requirements  
Set environment variable in configuration:  
GOOGLE_APPLICATION_CREDENTIALS=
/path/to/file

## Summary
Record audio from microphone, and use it to change presentation slides.

## Sound recording/API client
File: mainwindow.py  
Input: audio  
Output: JSON from Google API  
Records audio, sends to Google API, gets JSON back

calls processing.main(options)
Options can include filename, etc.

https://cloud.google.com/speech-to-text/docs/quickstart-protocol?_ga=2.37937189.-782387982.1541168992

## Decision engine
Input: JSON from Google API, presentation file  
Output: commands to OS  
Process JSON and compare to file. Contains logic for when a command should be issued.

main()
	calls transcription.getResponses()
	opens file, etc
	does processing
	makes calls to virtual_keyboard as necessary

## Run command
Input: command  
Output: performs task  
Interacts with operating system, for instance issuing keypress (alternative would be to create a PPT plugin but I'd rather not limit this to Microsoft products)

## GUI
Input API key, presentation file, maybe other options for behavior. Start/stop.
