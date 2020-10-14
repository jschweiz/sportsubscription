# Authomatized subscription to sport trainings

This script allows to program automatic subscription to sports for which you are too lazy to get up early enough. 

## Filling personal information

* set the username / password in `config.py`
* set the wanted trainings in `config.py`

## Update google cloud function
* To create/update the google cloud function, use :  
`gcloud functions deploy [FUNCTION_NAME] --entry-point main --runtime python37 --trigger-resource [TOPIC_EVENT_NAME] --trigger-event google.pubsub.topic.publish --timeout 540`

## Schedule task during mornings
* To start a schudeled task:  
`gcloud scheduler jobs create pubsub [JOB_NAME] --schedule "1 8 * * 3" --topic [TOPIC_EVENT_NAME] --message-body "Job run to subscribe to volley training"`

[FUNCTION_NAME] = SUBSCRIBE
[TOPIC_EVENT_NAME] = SUBSCRIBETOPIC