# nfl38
A quick job that uses ESPNs hidden APIs to check NFL scores for a given score and then uses a separate service to post notifications to a WhatsApp group

This service checks ESPN's hidden sports APIs and checks for a final score of 38 or an in progress score of either 31 or 35 (-1td or -1fg respectively). 
https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b


It then posts to a simple phone notification service here: https://ntfy.sh/

ntfy and tasker are running on an old android phone that then uses a Tasker utility created to remotely login to Whatsapp on an old phone and post as the authenticated user:
https://old.reddit.com/r/tasker/comments/15ydqa1/project_share_sendreceive_whatsapp_message/

This ended up being far more complicated due to the difficulty of interacting with groups in Whatsapp. Telegram would have been far easier but it's a viable workaround.
