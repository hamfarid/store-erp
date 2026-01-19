"""
RabbitMQ Client Utility

Provides functions to connect, publish, and consume messages from RabbitMQ.
"""

import pika
import logging
import json
import time
import threading
from functools import partial

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RabbitMQClient:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establishes connection and channel to RabbitMQ."""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logging.info("Successfully connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None
            # Implement retry logic if necessary

    def _ensure_connected(self):
        """Ensures the connection is active, reconnects if necessary."""
        if not self.connection or self.connection.is_closed:
            logging.warning("RabbitMQ connection lost. Attempting to reconnect...")
            self.connect()
        if not self.channel or self.channel.is_closed:
            if self.connection and self.connection.is_open:
                self.channel = self.connection.channel()
                logging.info("RabbitMQ channel reopened.")
            else:
                self.connect() # Re-establish connection and channel

        return self.channel is not None

    def declare_queue(self, queue_name):
        """Declares a durable queue."""
        if self._ensure_connected():
            try:
                self.channel.queue_declare(queue=queue_name, durable=True)
                logging.info(f"Queue 	'{queue_name}	' declared successfully.")
            except Exception as e:
                logging.error(f"Failed to declare queue 	'{queue_name}	': {e}")
        else:
            logging.error(f"Cannot declare queue 	'{queue_name}	', not connected.")

    def publish_message(self, queue_name, message):
        """Publishes a persistent message to the specified queue."""
        if not self._ensure_connected():
            logging.error(f"Cannot publish message to 	'{queue_name}	', not connected.")
            return False

        try:
            self.declare_queue(queue_name) # Ensure queue exists
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                ))
            logging.info(f"Message published to queue 	'{queue_name}	': {message}")
            return True
        except Exception as e:
            logging.error(f"Failed to publish message to 	'{queue_name}	': {e}")
            # Connection might be broken, try reconnecting for next attempt
            self.connection.close() # Force reconnect on next call
            self.connection = None
            self.channel = None
            return False

    def start_consuming(self, queue_name, callback_func):
        """Starts consuming messages from a queue in a separate thread."""
        if not self._ensure_connected():
            logging.error(f"Cannot start consuming from 	'{queue_name}	', not connected.")
            return

        self.declare_queue(queue_name)

        # Use a partial function to pass 'self' to the thread target
        thread_target = partial(self._consume_loop, queue_name, callback_func)
        consumer_thread = threading.Thread(target=thread_target, daemon=True)
        consumer_thread.start()
        logging.info(f"Started consuming messages from queue 	'{queue_name}	' in a background thread.")

    def _consume_loop(self, queue_name, callback_func):
        """The actual consuming loop running in a thread."""
        while True:
            try:
                if not self._ensure_connected():
                    logging.warning("Consumer waiting for RabbitMQ connection...")
                    time.sleep(5)
                    continue

                self.channel.basic_qos(prefetch_count=1) # Process one message at a time
                # Pass the channel and method/properties to the callback
                on_message_callback = lambda ch, method, properties, body: self._handle_message(ch, method, properties, body, callback_func)
                self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback)
                logging.info(f"Consumer thread waiting for messages on 	'{queue_name}	'.")
                self.channel.start_consuming()
            except pika.exceptions.ConnectionClosedByBroker:
                logging.warning("Connection closed by broker. Reconnecting...")
                time.sleep(5)
            except pika.exceptions.AMQPChannelError as err:
                logging.error(f"Caught a channel error: {err}, stopping consumer loop.")
                break
            except pika.exceptions.AMQPConnectionError:
                logging.warning("Connection was closed. Reconnecting...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Unexpected error in consumer loop: {e}. Restarting consumption...")
                # Attempt to close channel/connection cleanly before retrying
                try:
                    if self.channel and self.channel.is_open:
                        self.channel.close()
                    if self.connection and self.connection.is_open:
                        self.connection.close()
                except Exception as close_err:
                    logging.error(f"Error closing RabbitMQ resources: {close_err}")
                self.connection = None
                self.channel = None
                time.sleep(5)

    def _handle_message(self, channel, method, properties, body, user_callback):
        """Internal handler to process message and manage acknowledgments."""
        logging.info(f"Received message from queue: {method.routing_key}")
        try:
            message_data = json.loads(body)
            logging.debug(f"Message body: {message_data}")
            # Call the user-provided callback function
            success = user_callback(message_data)
            if success:
                channel.basic_ack(delivery_tag=method.delivery_tag)
                logging.info("Message acknowledged.")
            else:
                # Optionally implement nack or requeue logic here
                channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Don't requeue on failure
                logging.warning("Message processing failed, NACK sent.")
        except json.JSONDecodeError:
            logging.error("Failed to decode message body (JSON). Discarding message.")
            channel.basic_ack(delivery_tag=method.delivery_tag) # Ack to remove invalid message
        except Exception as e:
            logging.error(f"Error processing message: {e}. Discarding message.")
            # Acknowledge the message to prevent it from being redelivered indefinitely
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        """Closes the connection to RabbitMQ."""
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                logging.info("RabbitMQ connection closed.")
        except Exception as e:
            logging.error(f"Error closing RabbitMQ connection: {e}")

