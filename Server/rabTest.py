import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )

    async with connection:
        routing_key = queue_receive

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=str(dictToSend).encode()),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    hostNameNum = input("Hostname num: ")
    hostName = f"linux-HP-ProBook-450-G5+{hostNameNum}"
    cmdsToRun = input("Cmds: ")
    queue_receive = "recv_cmds_queue"
    queue_reply_cmds = "reply_cmds_queue"
    dictToSend = {hostName: cmdsToRun}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()