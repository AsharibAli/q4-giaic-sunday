# Class 14 Assignment - January 11

## Assignment: Publishing Docker Images to Docker Hub

Publish your **nextjs** & **fastapi** docker images that you created last week to Docker Hub.

![dockerhub](https://media.geeksforgeeks.org/wp-content/uploads/20230419170724/Docker-hub-registry.webp)

---

## Step 1: Create a Docker Hub Account

If you don't have one already:

- Go to https://hub.docker.com
- Sign up for a free account
- Remember your username (you'll need it for tagging images)

---

## Step 2: Login to Docker Hub from Terminal

Run this command and enter your Docker Hub credentials when prompted:

```bash
docker login
```

---

## Step 3: Build Your Docker Images with Proper Tags

Docker Hub images must be tagged in the format:

- **`<your-dockerhub-username>/<image-name>:<tag>`**

For the Next.js project:

```bash
docker build -t <your-dockerhub-username>/nextjs-docker:latest .
```

For the FastAPI project:

```bash
docker build -t <your-dockerhub-username>/fastapi-docker:latest .
```

***⚠️ Replace <your-username> with your actual Docker Hub username!***

---

## Step 4: Push Your Images to Docker Hub

```bash
# Next.js
docker push <your-dockerhub-username>/nextjs-docker:latest

# FastAPI
docker push <your-dockerhub-username>/fastapi-docker:latest
```

---

## Step 5: Verify on Docker Hub

- Go to https://hub.docker.com
- Navigate to your repositories by clicking on **My Profile** in the top right corner.
- You should see both *fastapi-docker* and *nextjs-docker* listed!

---

## Step 6: Pull & Run Your Images

Pull the images from Docker Hub:

```bash
# Next.js
docker pull <your-dockerhub-username>/nextjs-docker:latest

# FastAPI
docker pull <your-dockerhub-username>/fastapi-docker:latest
```

Run the images as docker containers:

```bash
# Next.js
docker run -d -p 3000:3000 --name my-nextjs-docker <your-dockerhub-username>/nextjs-docker:latest

# FastAPI
docker run -d -p 8000:8000 --name my-fastapi-docker <your-dockerhub-username>/fastapi-docker:latest
```

---


## Submission Requirements

1. Copy the docker images repository links from your Docker Hub account (nextjs-docker & fastapi-docker)
2. Put the links to the form below

---

**Submit Assignment Form:** [https://forms.gle/Stobn9ERxmcTwzMbA](https://forms.gle/Stobn9ERxmcTwzMbA)

---

## Note

- Feel free to complete the assignment in any way you like, using resources from the internet such as YouTube videos, articles, etc.
- You can use ChatGPT or any other AI tools to learn the concepts, but you should write the code yourself (do not copy-paste).
