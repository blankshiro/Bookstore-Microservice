package cs302.orders.orders_;

import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.CollectionTable;
import javax.persistence.Column;
import javax.persistence.ElementCollection;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import com.fasterxml.jackson.annotation.JsonIgnore;
import javax.persistence.JoinColumn;


import lombok.*;


@Entity
@Getter
@Setter
@ToString
@AllArgsConstructor
@EqualsAndHashCode
public class Order_ {
    private @Id @GeneratedValue (strategy = GenerationType.IDENTITY) Long id;
    private Long userId;
    private String datetime;
    private Long totalPrice;
    
    
    @ElementCollection // 1
    @CollectionTable(name = "itemDetails", joinColumns = @JoinColumn(name = "id")) // 2
    @Column(name = "itemDetails") // 3
    private List<ItemDetails> details;

    
    
    public Order_() {

    }
    
    public Order_(Long userId, String datetime, Long totalPrice, List<ItemDetails> details){
        this.userId = userId;
        this.datetime = datetime;
        this.totalPrice = totalPrice;
        this.details = details;
    }

    public Long getId(){
        return this.id;
    }
    
    public Long getUserId(){
        return this.userId;
    }
    public String getDatetime(){
        return this.datetime;
    }
    public Long getTotalPrice(){
        return this.totalPrice;
    }
    public List<ItemDetails> getDetails(){
        return this.details;
    }


    public void setDetails(List<ItemDetails> details){
        this.details = details;
    }

    public void setUserId(Long userId){
        this.userId = userId;
    }
    public void setDatetime(String datetime){
        this.datetime = datetime;
    }
    public void setTotalPrice(Long totalPrice){
        this.totalPrice = totalPrice;
    }


}