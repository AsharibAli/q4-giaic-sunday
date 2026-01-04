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
   # Install nodejs version 22
   FROM node:22-alpine 
   
   # Set working directory means (where the commands will be executed)
   WORKDIR /app 
   
   # Copy package.json and package-lock.json to working directory
   COPY package*.json ./ 
   
   # Install depedencies
   RUN npm install
   
   # Copy all files to working directory
   COPY . . 
   
   # Build the project
   RUN npm run build
   
   # Application access port, localhost:3000 or 127.0.0.1:3000 
   EXPOSE 3000 
   
   # Run the application
   CMD ["npm", "start"] 
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
   # Install python version 3.12
   FROM python:3.12-slim 
   
   # Set working directory means (where the commands will be executed)
   WORKDIR /app 
   
   # Copy all files to working directory
   COPY . . 
   
   # Install uv using pip
   RUN pip install uv 
   
   # Install all dependencies in a project
   RUN uv sync 
   
   # Application access port, localhost:8000 or 127.0.0.1:8000
   EXPOSE 8000 
   
   # Run the application
   CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0"]
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
