# Bookstore-Microservice - Chris Bookstore

CS302 Final Project <br />
Developed by: Team 9 <br />
Edwin Tok Wei Liang, Ezekiel Ong Young, Jerome Goh Ting Chuan,
Miguel Alonzo Ortega, Tay Wei Jie

## Description

Simple bookstore application to showcase CI/CD and DevOps practices.<br />

## Getting Started
Building a local version of our application with mock databases and message queues

1. Open a terminal in the root directory
2. Run  ```docker compose up --build```
3. After a few minutes, all the services should be fully built
4. The end-to-end test should show 13/13 passes <br />
   If there are health check failures ie. the tests are ran before the containers have start up, increase the delay in */orders_test/tests/test_orders.py*
5. Check out our key API in *DemoClient.http* to recreate the key use cases. <br>
   *The *id* to be used in the API may be different. Please use ```GET``` calls to ensure that the users/products/order id are present
