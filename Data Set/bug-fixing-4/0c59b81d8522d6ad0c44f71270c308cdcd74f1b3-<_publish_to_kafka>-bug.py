def _publish_to_kafka(self, request):
    '\n        Sends raw event data to Kafka for later offline processing.\n        '
    try:
        if (len(request.body) > options.get('kafka-publisher.max-event-size')):
            return
        if (random.random() >= options.get('kafka-publisher.raw-event-sample-rate')):
            return
        meta = {
            
        }
        for (key, value) in request.META.items():
            try:
                json.dumps([key, value])
                meta[key] = value
            except TypeError:
                pass
        meta['SENTRY_API_VIEW_NAME'] = self.__class__.__name__
        kafka_publisher.publish(channel=getattr(settings, 'KAFKA_RAW_EVENTS_PUBLISHER_TOPIC', 'raw_store_events'), value=json.dumps([meta, request.body]))
    except Exception as e:
        logger.debug('Cannot publish event to Kafka: {}'.format(e.message))