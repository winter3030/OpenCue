package com.imageworks.spcue.dao;

import com.imageworks.spcue.UserEntity;

public interface UserDao {

    public void createUser(UserEntity user);

    public UserEntity getUserInfo(String name);

    public void deleteUser(String name);

    public void updateUserInfo(UserEntity user);
}
