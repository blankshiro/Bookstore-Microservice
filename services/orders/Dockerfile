#
# Build stage
#
FROM maven:3.6.0-jdk-11-slim AS build
COPY src /orders/src
COPY pom.xml /orders
RUN mvn -f /orders/pom.xml clean package

#
# Package stage
#
FROM openjdk:11-jre-slim
COPY --from=build /orders/target/orders-0.0.1-SNAPSHOT.jar /orders/target/orders-0.0.1-SNAPSHOT.jar
EXPOSE 8083
ENTRYPOINT ["java","-jar","/orders/target/orders-0.0.1-SNAPSHOT.jar"]
