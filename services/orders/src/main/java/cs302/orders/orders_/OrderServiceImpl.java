package cs302.orders.orders_;

import java.util.*;
import org.springframework.stereotype.Service;


@Service
public class OrderServiceImpl implements OrderService {
   
    private OrderRepository orders;
    

    public OrderServiceImpl(OrderRepository orders){
        this.orders = orders;
    }

    @Override
    public List<Order_> listOrders() {
        return orders.findAll();
    }

    
    @Override
    public Order_ getOrder(Long id){
        // Using Java Optional, as "findById" of Spring JPA returns an Optional object
        // Optional forces developers to explicitly handle the case of non-existent values
        // Here is an implementation using lambda expression to extract the value from Optional<Book>
        return orders.findById(id).map(order -> {
            return order;
        }).orElse(null);
    }
    
    @Override
    public Order_ addOrder(Order_ order) {
        return orders.save(order);
    }
    
    @Override
    public Order_ updateOrder(Long id, Order_ newOrderInfo){
        Optional<Order_> p = orders.findById(id);
        if (p.isPresent()){
            Order_ order = p.get();
            order.setDetails(newOrderInfo.getDetails());
            order.setUserId(newOrderInfo.getUserId());
            order.setDatetime(newOrderInfo.getDatetime());
            order.setTotalPrice(newOrderInfo.getTotalPrice());
            
            return orders.save(order);
        }else
            return null;
    }

    /**
     * Remove a book with the given id
     * Spring Data JPA does not return a value for delete operation
     * Cascading: removing a book will also remove all its associated reviews
     */
    @Override
    public void deleteOrder(Long id){
        orders.deleteById(id);
    }

    @Override
    public List<Order_> getOrderbyUserId(Long userId) {
        return orders.findByUserId(userId);
    }
}