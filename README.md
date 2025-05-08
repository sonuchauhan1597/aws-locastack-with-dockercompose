# Reliable Message Processing with Amazon SQS

This project demonstrates how to use **Amazon Simple Queue Service (SQS)** for building scalable, decoupled, and reliable distributed applications. It includes a command-line utility built using Docker to produce and process messages in an SQS queue, with message tracking stored in DynamoDB.

---

## 📌 Why Use Amazon SQS?

Amazon SQS is a fully managed message queue service that enables asynchronous communication between microservices and components. Here's why it's beneficial:

- **Asynchronous Communication**: Components can work independently without waiting for others to respond.
- **Reliability**: Messages are persisted for 4 days by default and can be retained for up to 21 days.
- **Decoupling**: Producer and consumer components remain independent, simplifying scaling and maintenance.
- **Ease of Use**: Simple API and integration with other AWS services like Lambda and CloudWatch.

---

## 🛠️ Tool Introduction

This project includes a command-line utility built using Docker to produce and process messages in an SQS queue. The utility performs the following tasks:

- **Message Production**: Generates messages and sends them to the SQS queue.
- **Message Consumption**: Retrieves and processes messages from the SQS queue.
- **Message Tracking**: Records consumed message IDs in DynamoDB to prevent duplicate processing.

---

## ⚙️ How to Build the Tool

To set up the environment and build the tool, follow these steps:

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Build and start the containers using Docker Compose:

   ```bash
   docker-compose up
   ```

   This command will start the necessary services, including LocalStack (for local AWS services) and the workspace container.

---

## 🔧 How to Configure the Environment

If you prefer to execute scripts without Docker, you can configure the environment as follows:

1. Update the endpoint URL in the configuration files to point to `localhost`:

   ```python
   # Example: Update SQS endpoint in config.py
   SQS_ENDPOINT = "http://localhost:4566"
   ```

2. Start the containers in detached mode:

   ```bash
   docker-compose start
   ```

   This will run the containers in the background, allowing you to interact with the services locally.

---

## 🚀 How to Run the Tool

Ensure that the LocalStack and workspace containers are running. You can check the status of the containers using:

```bash
docker ps
```

Once the containers are up and running, you can execute the following commands:

* **To produce new messages**:

  ```bash
  docker exec -it <workspace-container-name> python /opt/generator.py
  ```

* **To consume existing messages**:

  ```bash
  docker exec -it <workspace-container-name> python /opt/sqs_message_ops.py consume --count 2
  ```

* **To fetch all messages from DynamoDB**:

  ```bash
  docker exec -it <workspace-container-name> python /opt/sqs_message_ops.py show
  ```

* **To clear all messages from DynamoDB**:

  ```bash
  docker exec -it <workspace-container-name> python /opt/sqs_message_ops.py clear
  ```

Replace `<workspace-container-name>` with the actual name of your workspace container, which can be found using `docker ps`.

---

## 🧩 Challenges Encountered

During the development of this tool, the following challenges were encountered:

* **Setting Up LocalStack**: Configuring LocalStack to simulate AWS services locally required careful setup to ensure compatibility with the SQS and DynamoDB services.
* **Networking Between Containers**: Enabling communication between the Docker containers hosting LocalStack and the workspace required configuring Docker networking to allow seamless interaction.

Overcoming these challenges ensured a robust local development environment that closely mirrors AWS services.

---

## ✅ Conclusion

Amazon SQS is a powerful tool for building decoupled, scalable, and reliable applications. By leveraging its features and integrating with other AWS services like Lambda, you can create robust systems that handle varying loads and recover gracefully from failures. Whether you're modernizing legacy applications or building new cloud-native solutions, SQS provides the foundation for effective message queuing and processing.

---

Happy building! 🎉
