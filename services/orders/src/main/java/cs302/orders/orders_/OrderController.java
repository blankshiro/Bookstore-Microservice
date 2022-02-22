package cs302.orders.orders_;

import java.util.List;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrderController {
    private OrderService orderService;

    public OrderController(OrderService os){
        this.orderService = os;
    }

    /**
     * List all orders in the system
     * @return list of all orders
     */
    @GetMapping("/orders")
    public List<Order_> getOrders(){
        System.out.println(orderService.listOrders());
        return orderService.listOrders();
    }

    /**
     * Search for order with the given id
     * If there is no order with the given "id", throw a orderNotFoundException
     * @param id
     * @return order with the given id
     */
    @GetMapping("/orders/{id}")
    public Order_ getOrders(@PathVariable Long id){
        Order_ order = orderService.getOrder(id);

        // Need to handle "order not found" error using proper HTTP status code
        // In this case it should be HTTP 404
        if(order == null) throw new OrderNotFoundException(id);
        return orderService.getOrder(id);

    }
    /**
     * Add a new order with POST request to "/orders"
     * Note the use of @RequestBody
     * @param order
     * @return list of all orders
     */
    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping("/orders")
    public Order_ addOrder(@RequestBody Order_ order){
        return orderService.addOrder(order);
    }

    /**
     * If there is no order with the given "id", throw a orderNotFoundException
     * @param id
     * @param newOrderInfo
     * @return the updated, or newly added order
     */
    @PutMapping("/orders/{id}")
    public Order_ updateOrder(@PathVariable Long id, @RequestBody Order_ newOrderInfo){
        Order_ order = orderService.updateOrder(id, newOrderInfo);
        if(order == null) throw new OrderNotFoundException(id);
        
        return order;
    }

    /**
     * Remove a order with the DELETE request to "/orders/{id}"
     * If there is no order with the given "id", throw a orderNotFoundException
     * @param id
     */
    @DeleteMapping("/orders/{id}")
    public void deleteOrder(@PathVariable Long id){
        try{
            orderService.deleteOrder(id);
         }catch(EmptyResultDataAccessException e) {
            throw new OrderNotFoundException(id);
         }
    }

        /**
     * Search for order with the given id
     * If there is no order with the given "id", throw a orderNotFoundException
     * @param id
     * @return order with the given id
     */
    @GetMapping("/ordersByUserId/{id}")
    public List<Order_> getOrdersByUserId(@PathVariable Long id){
        return orderService.getOrderbyUserId(id);

    }
}