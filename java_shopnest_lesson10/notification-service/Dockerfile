# TODO Exercise 1: Complete this multi-stage Dockerfile
# Stage 1 (build): FROM maven:3.9-eclipse-temurin-21 AS build
#   WORKDIR /app, COPY pom.xml ., RUN mvn dependency:go-offline
#   COPY src ./src, RUN mvn package -DskipTests
# Stage 2 (runtime): FROM eclipse-temurin:21-jre
#   WORKDIR /app, COPY --from=build /app/target/*.jar app.jar
#   EXPOSE 8083, ENTRYPOINT ["java", "-jar", "app.jar"]

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8083
ENTRYPOINT ["java", "-jar", "app.jar"]
