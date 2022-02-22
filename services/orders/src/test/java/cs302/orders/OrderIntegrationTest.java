package cs302.orders;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.net.URI;
import java.util.*;

import org.json.JSONObject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;

import cs302.orders.orders_.*;

/** Start an actual HTTP server listening at a random port*/
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
class OrderIntegrationTest {

	@LocalServerPort
	private int port;

	private final String baseUrl = "http://localhost:";

	@Autowired
	/**
		 * Use TestRestTemplate for testing a real instance of your application as an external actor.
		 * TestRestTemplate is just a convenient subclass of RestTemplate that is suitable for integration tests.
		 * It is fault tolerant, and optionally can carry Basic authentication headers.
	 */
	private TestRestTemplate restTemplate;

	@Autowired
	private OrderRepository orders;


	@AfterEach
	void tearDown(){
		// clear the database after each test
		// orders.deleteAll();
	}

	@Test
	public void getOrders_Success() throws Exception {
		URI uri = new URI(baseUrl + port + "/orders");
        List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        

        orders.save(new Order_((long) 1, "some datetime", (long) 100, l1));

		
		// Need to use array with a ReponseEntity here
		ResponseEntity<Order_[]> result = restTemplate.getForEntity(uri, Order_[].class);
		assertEquals(200, result.getStatusCode().value());
	}

	@Test
	public void getOrder_ValidOrderId_Success() throws Exception {
        List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
        Order_ order = new Order_((long) 1, "some datetime", (long) 100, l1);
        Long id = orders.save(order).getId();

		URI uri = new URI(baseUrl + port + "/orders/" + id);
		
		ResponseEntity<Order_> result = restTemplate.getForEntity(uri, Order_.class);
			
		assertEquals(200, result.getStatusCode().value());
		assertEquals(order.getUserId(), result.getBody().getUserId());
        assertEquals(order.getDatetime(), result.getBody().getDatetime());
        assertEquals(order.getTotalPrice(), result.getBody().getTotalPrice());
        assertEquals(order.getDetails().toString(), result.getBody().getDetails().toString());
	}

	@Test
	public void getOrder_InvalidOrderId_Failure() throws Exception {
		URI uri = new URI(baseUrl + port + "/orders/9000");
		
		ResponseEntity<Order_> result = restTemplate.getForEntity(uri, Order_.class);
			
		assertEquals(404, result.getStatusCode().value());
	}
    

	@Test
	public void addOrder_Success() throws Exception {
		URI uri = new URI(baseUrl + port + "/orders");
		List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
        Order_ order = new Order_((long) 1, "some datetime", (long) 100, l1);
        Long id = orders.save(order).getId();
		

		ResponseEntity<Order_> result = restTemplate.postForEntity(uri, order, Order_.class);
			
		assertEquals(201, result.getStatusCode().value());
		assertEquals(order.getUserId(), result.getBody().getUserId());
        assertEquals(order.getDatetime(), result.getBody().getDatetime());
        assertEquals(order.getTotalPrice(), result.getBody().getTotalPrice());
        assertEquals(order.getDetails().toString(), result.getBody().getDetails().toString());	
	}


	@Test
	public void deleteOrder_Success() throws Exception {

		List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
        Order_ order = new Order_((long) 1, "some datetime", (long) 100, l1);
        Long id = orders.save(order).getId();

		URI uri = new URI(baseUrl + port + "/orders/" + id);

		ResponseEntity<Void> result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);

		assertEquals(200, result.getStatusCode().value());

		result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);
		assertEquals(404, result.getStatusCode().value());
	}

	@Test
	public void deleteOrder_InvalidOrderId_Failure() throws Exception {
		URI uri = new URI(baseUrl + port + "/orders/9000");
		
		ResponseEntity<Void> result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);

		assertEquals(404, result.getStatusCode().value());
		
	}


	@Test
	public void updateOrder_Success() throws Exception {
		List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
        Order_ order = new Order_((long) 1, "some datetime", (long) 100, l1);
        Long id = orders.save(order).getId();

		
		URI uri = new URI(baseUrl + port + "/orders/" + id);

		Order_ newOrder = new Order_((long) 1, "another datetime", (long) 100, l1);

		ResponseEntity<Order_> result = restTemplate.exchange(uri, HttpMethod.PUT, new HttpEntity<>(newOrder), Order_.class);
		
		assertEquals(200, result.getStatusCode().value());
		assertEquals(newOrder.getUserId(), result.getBody().getUserId());
        assertEquals(newOrder.getDatetime(), result.getBody().getDatetime());
        assertEquals(newOrder.getTotalPrice(), result.getBody().getTotalPrice());
        assertEquals(newOrder.getDetails().toString(), result.getBody().getDetails().toString());
		}

		
	@Test
	public void updateOrder_InvalidOrderId_Failure() throws Exception {

		List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
        Order_ order = new Order_((long) 1, "some datetime", (long) 100, l1);

		URI uri = new URI(baseUrl + port + "/orders/9000");
		
		ResponseEntity<Order_> result = restTemplate.exchange(uri, HttpMethod.PUT, new HttpEntity<>(order), Order_.class);

		assertEquals(404, result.getStatusCode().value());

	}

	
	@Test
	public void getOrdersByUserId_Success() throws Exception {
        List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        l1.add(i1);

        List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        l2.add(i2);
        l1.add(i2);
        
		Long user_id = (long) 1;
        orders.save(new Order_(user_id, "some datetime", (long) 100, l1));

		URI uri = new URI(baseUrl + port + "/ordersByUserId/" + user_id);

		// Need to use array with a ReponseEntity here
		ResponseEntity<Order_[]> result = restTemplate.getForEntity(uri, Order_[].class);

		assertEquals(200, result.getStatusCode().value());
	}


}
