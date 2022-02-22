package cs302.orders.orders_;

import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.CollectionTable;
import javax.persistence.Column;
import javax.persistence.ElementCollection;
import javax.persistence.Embeddable;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import com.fasterxml.jackson.annotation.JsonIgnore;
import javax.persistence.JoinColumn;
import java.io.Serializable;



import lombok.*;

@Embeddable
public class ItemDetails implements Serializable{
    @Column
    private Long productId;

    @Column
    private Integer quantity;

    @Column 
    private String bookTitle;

    @Column
    private Long price;

    public ItemDetails(Long productId, Integer quantity,  Long price, String bookTitle) {
        this.productId = productId;
        this.quantity = quantity;
        this.price = price;
        this.bookTitle = bookTitle;
    }

    public ItemDetails() {
        
    }

    public Long getProductId(){
        return this.productId;
    }
    public Integer getQuantity(){
        return this.quantity;
    }
    public Long getPrice(){
        return this.price;
    }
    public String getBookTitle(){
        return this.bookTitle;
    }
    @Override
    public String toString() {
        return String.format("%d %d %d %s", productId, quantity, price, bookTitle);
    }

    public void setBookTitle(String bookTitle){
        this.bookTitle = bookTitle;
    }
    public void setQuantity(Integer quantity){
        this.quantity = quantity;
    }
    public void setProductId(Long productId){
        this.productId = productId;
    }
    public void setPrice(Long price){
        this.price = price;
    }
} 
    