from kafka import KafkaProducer, KafkaConsumer

def sendKafka():
    my_producer = KafkaProducer(
        bootstrap_servers=['localhost:29092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    message = "1"
    while message != "0":
        message = input("Type your message: ")
        my_producer.send("testnum", value=message)
        getKafka()

def getKafka():
    consumer = KafkaConsumer('testnum',
                             bootstrap_servers=['localhost:29092'],
                             group_id='test',
                             auto_offset_reset='earliest')
    for msg in consumer:
        res_str = msg.value.decode("utf-8")
        print("Text:", res_str)