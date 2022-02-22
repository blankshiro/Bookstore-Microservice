package csd.user;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import csd.user.user.*;

@SpringBootApplication
public class Week4Application {

	public static void main(String[] args) {
		
		ApplicationContext ctx = SpringApplication.run(Week4Application.class, args);

        // JPA repository init
        UserRepository jpaRepo = ctx.getBean(UserRepository.class);
        // System.out.println(jpaRepo.save(new User("JPA Fundamentals", "01234", "Author1", "Pub1")).getName());
        // System.out.println(jpaRepo.save(new User("Gone With The Wind", "01234", "Author1", "Pub1")).getName());
    }
    
}
