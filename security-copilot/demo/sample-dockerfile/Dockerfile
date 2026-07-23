FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
COPY . /app
ENV API_KEY=DEMO_ONLY_NOT_A_REAL_SECRET
USER root
CMD ["/bin/bash"]

