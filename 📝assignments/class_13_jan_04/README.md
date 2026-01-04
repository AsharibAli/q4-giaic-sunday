# Class 13 Assignment - January 04

## Assignment: Docker Containerization

Create two simple containerized projects (**nextjs-docker** and **fastapi-docker**) and place them in a single GitHub repository with Docker Desktop screenshots.

![dockerfile-image-container](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLsuiyn9J78Km4ZMFPJsTLVk_CpxVx7e-V3Q&s)

---

## Part 1: Next.js Docker

1. Create project:
   ```bash
   npx create-next-app@latest nextjs-docker
   ```

2. Create `Dockerfile` in project root:
   ```dockerfile
   FROM node:22-alpine # Install nodejs version 22
   
   WORKDIR /app # Set working directory means (where the commands will be executed)
   
   COPY package*.json ./ # Copy package.json and package-lock.json to working directory
   
   RUN npm install # Install depedencies
   
   COPY . . # Copy all files to working directory
   
   RUN npm run build # Build the project
   
   EXPOSE 3000 # Application access port, localhost:3000 or 127.0.0.1:3000 
   
   CMD ["npm", "start"] # Run the application
   ```

3. Build & run:
   ```bash
   # Create docker image
   docker build -t nextjs-docker .

   # Run docker container
   docker run -p 3000:3000 nextjs-docker
   ```

---

## Part 2: FastAPI Docker

1. Create project:
   ```bash
   uv init fastapi-docker

   cd fastapi-docker
   
   uv add fastapi[standard]
   ```

2. Update `main.py`:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"message": "Hello from FastAPI Docker!"}
   ```

3. Create `Dockerfile` in project root:
   ```dockerfile
   FROM python:3.12-slim # Install python version 3.12
   
   WORKDIR /app # Set working directory means (where the commands will be executed)
   
   COPY . . # Copy all files to working directory
   
   RUN pip install uv # Install uv
   
   RUN uv sync # Install all dependencies in project
   
   EXPOSE 8000 # Application access port, localhost:8000 or 127.0.0.1:8000
   
   CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0"] # Run the application
   ```

4. Build & run:
   ```bash
   # Create docker image
   docker build -t fastapi-docker .

   # Run docker container
   docker run -p 8000:8000 fastapi-docker
   ```

---

## Submission Requirements

1. Create a GitHub repo with both folders (`nextjs-docker` & `fastapi-docker`)
2. Add screenshots to README showing:
   - Docker Desktop **Images** (both projects)
   - Docker Desktop **Containers** (both running)

---

**Submit Assignment Form:** [https://forms.gle/tKYj7EDGm99jLhsS6](https://forms.gle/tKYj7EDGm99jLhsS6)

## Note

- Feel free to complete the assignment in any way you like, using resources from the internet such as YouTube videos, articles, etc.
- You can use ChatGPT or any other AI tools to learn the concepts, but you should write the code yourself (do not copy-paste).
