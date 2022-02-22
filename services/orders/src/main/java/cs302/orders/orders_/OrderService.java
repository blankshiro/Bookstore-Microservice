package cs302.orders.orders_;

import java.util.List;

public interface OrderService {
    List<Order_> listOrders();
    Order_ getOrder(Long id);
    Order_ addOrder(Order_ order);
    Order_ updateOrder(Long id, Order_ order);
    List<Order_> getOrderbyUserId(Long userId);

    /**
     * Change method's signature: do not return a value for delete operation
     * @param id
     */
    void deleteOrder(Long id);
}