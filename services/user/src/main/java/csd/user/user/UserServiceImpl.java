package csd.user.user;

import java.util.*;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    private UserRepository users;
    // private ProductRepository products;

    public UserServiceImpl(UserRepository users) {
        this.users = users;
    }

    @Override
    public List<User> listUsers() {
        return users.findAll();
    }

    @Override
    public User getUser(Long id) {
        // Using Java Optional, as "findById" of Spring JPA returns an Optional object
        // Optional forces developers to explicitly handle the case of non-existent
        // values
        // Here is an implementation using lambda expression to extract the value from
        // Optional<Book>
        return users.findById(id).map(user -> {
            return user;
        }).orElse(null);
    }

    
    @Override
    public User getUserByName(String name) {
        List<User> user_list = users.findByName(name);
        if (user_list.size() == 0) {
            return null;
        }
        return user_list.get(0);
    }

    @Override
    public User addUser(User user) {
        return users.save(user);
    }

    @Override
    public User updateUser(Long id, User newUserInfo) {
        Optional<User> p = users.findById(id);
        if (p.isPresent()) {
            User user = p.get();
            user.setName(newUserInfo.getName());
            user.setPhone(newUserInfo.getPhone());
            user.setEmail(newUserInfo.getEmail());

            // these might be problems!!
            user.setPassword(newUserInfo.getPassword());

            return users.save(user);
        } else
            return null;
    }

    /**
     * Remove a book with the given id Spring Data JPA does not return a value for
     * delete operation Cascading: removing a book will also remove all its
     * associated reviews
     */
    @Override
    public void deleteUser(Long id) {
        users.deleteById(id);
    }

}