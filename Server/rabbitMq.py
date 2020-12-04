import pika
import time
import os

class RabbitMq(object):
    def __init__(self, timeout=20):
        self.RABBIT_HOST = os.getenv('RABBIT_HOST', "127.0.0.1")
        
        
        self.queue_receive = "recv_cmds_queue"
        self.queue_reply_cmds = "reply_cmds_queue"

        self.timeout = timeout 
    

    def blockingSender(self, msg):
        msg = str(msg)
        connection = pika.BlockingConnection(f"amqp://guest:guest@{self.RABBIT_HOST}/")
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=self.queue_receive,
                properties=pika.BasicProperties(expiration='30000'),
                body=msg)
        connection.close()


    
    def blockingReceive(self, hostname):
        connection = pika.BlockingConnection(f"amqp://guest:guest@{self.RABBIT_HOST}/")
        channel = connection.channel()
        start = time.time()
        end = time.time()

        #Keep checking for message for as long as class var timeout is stated
        while (end - start) < self.timeout:
            method_frame, header_frame, body = channel.basic_get(self.queue_reply_cmds)

            end = time.time()
            if method_frame:
                print(method_frame, header_frame, body)
                if hostname in str(body):
                    channel.basic_ack(method_frame.delivery_tag)
                    return body
                else:
                    print(f"{hostname} not in message")
                    channel.basic_nack(method_frame.delivery_tag)

            time.sleep(1)



    def process_api_call(self, webReqstData=None):
        if not webReqstData: return

        print(webReqstData)

        # Format expected: {hostName: cmdsToRun}
        self.blockingSender(webReqstData)

        for k,v in webReqstData.items():

            return self.blockingReceive(k)
            

def main():
    rbMq = RabbitMq()

    rbMq.process_api_call({"AG0119WA016702": "hostname"})

if __name__ == "__main__":
    main()
