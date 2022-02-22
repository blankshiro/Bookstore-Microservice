package cs302.orders;


import org.hibernate.cache.spi.support.AbstractReadWriteAccess.Item;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import cs302.orders.orders_.*;

import java.util.*;

@SpringBootApplication
public class Week4Application {

	public static void main(String[] args) {
		
		ApplicationContext ctx = SpringApplication.run(Week4Application.class, args);

        // JPA repository init
        OrderRepository jpaRepo = ctx.getBean(OrderRepository.class);
        // List<ItemDetails> l1 = new ArrayList<ItemDetails>();
        // ItemDetails i1 = new ItemDetails((long) 1, 10, (long) 10, "Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib");
        // l1.add(i1);

        // List<ItemDetails> l2 = new ArrayList<ItemDetails>();
        // ItemDetails i2 = new ItemDetails((long) 2, 5, (long) 10, "Classic Computer Science Problems in Python");
        // l2.add(i2);
        // l1.add(i2);
        

        // jpaRepo.save(new Order_((long) 1, "some datetime", (long) 100, l1));
        // jpaRepo.save(new Order_((long) 2, "some datetime", (long) 50, l2));
        // System.out.println("YAY");
    }
    
}
