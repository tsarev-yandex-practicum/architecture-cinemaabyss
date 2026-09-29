FROM sbtscala/scala-sbt:eclipse-temurin-jammy-17.0.10_7_1.10.2_2.13.14 AS builder

WORKDIR /app

COPY project project
COPY build.sbt .
RUN sbt -batch update

COPY src src
RUN sbt -batch assembly

FROM eclipse-temurin:17-jre-jammy

WORKDIR /app

COPY --from=builder /app/target/scala-2.13/proxy-service.jar app.jar

EXPOSE 8000

CMD ["java", "-jar", "app.jar"]
