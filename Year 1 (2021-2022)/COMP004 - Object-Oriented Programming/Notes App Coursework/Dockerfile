FROM maven:3.9.7-eclipse-temurin-17

WORKDIR /app

COPY . .

RUN mvn clean && mvn package

EXPOSE 8080

ENTRYPOINT [ "mvn", "exec:exec"]
