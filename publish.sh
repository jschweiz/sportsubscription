gcloud functions deploy SUBSCRIBE --entry-point main --runtime python37 --trigger-resource SUBSCRIBETOPIC --trigger-event google.pubsub.topic.publish --timeout 540
