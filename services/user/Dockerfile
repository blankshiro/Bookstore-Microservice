#
# Build stage
#
FROM maven:3.6.0-jdk-11-slim AS build
COPY src /user/src
COPY pom.xml /user
RUN mvn -f /user/pom.xml clean package

#
# Package stage
#
FROM openjdk:11-jre-slim
COPY --from=build /user/target/user-0.0.1-SNAPSHOT.jar /user/target/user-0.0.1-SNAPSHOT.jar
EXPOSE 8083
ENTRYPOINT ["java","-jar","/user/target/user-0.0.1-SNAPSHOT.jar"]
