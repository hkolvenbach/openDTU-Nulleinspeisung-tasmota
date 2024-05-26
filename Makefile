# Name of the Docker image and container
IMAGE_NAME = nulleinspeisung
CONTAINER_NAME = nulleinspeisung

# Default target
.PHONY: all
all: build

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
.PHONY: run
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env $(IMAGE_NAME)

# Run the Docker container in debug mode
.PHONY: debug
debug:
	docker-compose -f docker-compose.debug.yml up --build

# Stop the Docker container
.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Remove the Docker image
.PHONY: clean
clean: stop
	docker rmi $(IMAGE_NAME) || true

# Show logs from the running container
.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)