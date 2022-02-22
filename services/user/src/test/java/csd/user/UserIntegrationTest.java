package csd.user;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.net.URI;
import java.util.*;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;


import csd.user.user.*;

/** Start an actual HTTP server listening at a random port*/
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
class UserIntegrationTest {

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
	private UserRepository users;


	@AfterEach
	void tearDown(){
		// clear the database after each test
		// users.deleteAll();
	}

	@Test
	public void getUsers_Success() throws Exception {
		URI uri = new URI(baseUrl + port + "/users");
		// Need to use array with a ReponseEntity here
		ResponseEntity<User[]> result = restTemplate.getForEntity(uri, User[].class);
		assertEquals(200, result.getStatusCode().value());
	}

	@Test
	public void getUser_ValidUserId_Success() throws Exception {

        
        User user = new User("name", "phone", "email", "password");
        Long id = users.save(user).getId();

		URI uri = new URI(baseUrl + port + "/users/" + id);
		
		ResponseEntity<User> result = restTemplate.getForEntity(uri, User.class);
			
		assertEquals(200, result.getStatusCode().value());
		assertEquals(user.getId(), result.getBody().getId());
        assertEquals(user.getName(), result.getBody().getName());
        assertEquals(user.getPhone(), result.getBody().getPhone());
        assertEquals(user.getEmail(), result.getBody().getEmail());
		assertEquals(user.getPassword(), result.getBody().getPassword());

	}

	@Test
	public void getUser_InvalidUserId_Failure() throws Exception {
		URI uri = new URI(baseUrl + port + "/users/9000");
		
		ResponseEntity<User> result = restTemplate.getForEntity(uri, User.class);
			
		assertEquals(404, result.getStatusCode().value());
	}
    

	@Test
	public void addUserSuccess() throws Exception {
		URI uri = new URI(baseUrl + port + "/users");
        
        User user = new User("name", "phone", "email", "password");
        Long id = users.save(user).getId();
		

		ResponseEntity<User> result = restTemplate.postForEntity(uri, user, User.class);
			
		assertEquals(201, result.getStatusCode().value());
		assertEquals(user.getId(), result.getBody().getId());
        assertEquals(user.getName(), result.getBody().getName());
        assertEquals(user.getPhone(), result.getBody().getPhone());
        assertEquals(user.getEmail(), result.getBody().getEmail());
		assertEquals(user.getPassword(), result.getBody().getPassword());
	}


	@Test
	public void deleteUserSuccess() throws Exception {
        
        User user = new User("name", "phone", "email", "password");
        Long id = users.save(user).getId();

		URI uri = new URI(baseUrl + port + "/users/" + id);

		ResponseEntity<Void> result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);

		assertEquals(200, result.getStatusCode().value());

		result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);
		assertEquals(404, result.getStatusCode().value());
	}

	@Test
	public void deleteUser_InvalidUserId_Failure() throws Exception {
		URI uri = new URI(baseUrl + port + "/users/9000");
		
		ResponseEntity<Void> result = restTemplate.exchange(uri, HttpMethod.DELETE, null, Void.class);

		assertEquals(404, result.getStatusCode().value());
		
	}


	@Test
	public void updateUser_Success() throws Exception {
        User user = new User("name", "phone", "email", "password");
        Long id = users.save(user).getId();

		
		URI uri = new URI(baseUrl + port + "/users/" + id);

		User newUser = new User("name", "phone", "email", "newpassword");

		ResponseEntity<User> result = restTemplate.exchange(uri, HttpMethod.PUT, new HttpEntity<>(newUser), User.class);
		
		assertEquals(200, result.getStatusCode().value());
		assertEquals(user.getId(), result.getBody().getId());
        assertEquals(newUser.getName(), result.getBody().getName());
        assertEquals(newUser.getPhone(), result.getBody().getPhone());
        assertEquals(newUser.getEmail(), result.getBody().getEmail());
		assertEquals(newUser.getPassword(), result.getBody().getPassword());
		}

		
	@Test
	public void updateUser_InvalidUserId_Failure() throws Exception {

        User user = new User("name", "phone", "email", "password");

		URI uri = new URI(baseUrl + port + "/users/9000");
		
		ResponseEntity<User> result = restTemplate.exchange(uri, HttpMethod.PUT, new HttpEntity<>(user), User.class);

		assertEquals(404, result.getStatusCode().value());

	}


}
