# TODO Exercise 1: Complete this multi-stage Dockerfile
# Stage 1: Builder
# FROM maven:3.9-eclipse-temurin-21 AS builder
# WORKDIR /app
# COPY pom.xml .
# RUN mvn dependency:go-offline -B
# COPY src ./src
# RUN mvn package -DskipTests -B

# Stage 2: Runtime
# FROM eclipse-temurin:21-jre-alpine
# WORKDIR /app
# COPY --from=builder /app/target/*.jar app.jar
# EXPOSE 8080
# ENTRYPOINT ["java", "-Dspring.profiles.active=azure", "-jar", "app.jar"]
