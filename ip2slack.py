#John Paul Morgan
#2EA2
#s088526
import socket
from slackclient import SlackClient
import os
SLACK_TOKEN = 'token hier' #mij ni spammen pls
sc = SlackClient(SLACK_TOKEN)
user_slack_id = '@jpmorgan'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #RETRIEVE IP
s.connect(("gmail.com", 80))
print('Gebruikte IP: ' + s.getsockname()[0])
ip = s.getsockname()[0]
s.close()
def list_channels():
	channels_call = sc.api_call("channels.list")
	if channels_call.get('ok'):
		return channels_call['channels']
	return None
def send_message(channel_id, msg):
	sc.api_call("chat.postMessage", channel=channel_id, text=msg, username='pyBot')
def send_private(msg):
	sc.api_call("chat.postMessage", asuser=True, channel=user_slack_id, text=msg)
if __name__ == '__main__':
	channels=list_channels()
	if channels:
		print("Slack channels: ")
		for channel in channels:
			print(channel['name'] + " (" + channel['id'] + ") ")
			if channel['name'] == 'general':
				send_message(channel['id'], "Hey " + channel['name'])
				f = open(os.path.join(__location__m 'ip.txt'), 'r')
				previous_ip = f.read()
				f.close()

				if previous_ip != '' and ip == previous_ip:
					send_message(channel['id'], "IP is hetzelfde als de vorige keer: " + ip)
					send_private("IP is hetzelfde als de vorige keer: " + ip)
				else:
					send_message(channel['id'], "Jou IP: " + ip)
					send_private("Jou IP: " + ip)

					f = open(os.path.join(__location__, 'ip.txt'), 'w')
					f.write(ip)
					f.close()
		print("##################")
		print("####Send Nudes####")
		print("##################")
	else:
		print("Kan niet verbinden")

