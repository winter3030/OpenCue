package com.imageworks.spcue.dao.postgres;

import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.support.JdbcDaoSupport;

import com.imageworks.spcue.UserEntity;
import com.imageworks.spcue.dao.UserDao;

import java.sql.ResultSet;
import java.sql.SQLException;

public class UserDaoJdbc extends JdbcDaoSupport implements UserDao {
    public static final RowMapper<UserEntity> USER_MAPPER = new RowMapper<UserEntity>() {
        @Override
        public UserEntity mapRow(ResultSet rs, int rowNum) throws SQLException {
            UserEntity user = new UserEntity();
            user.name = rs.getString("pk_name");
            user.admin = rs.getBoolean("b_admin");
            user.job_priority = rs.getInt("int_job_priority");
            user.job_max_cores = rs.getInt("int_job_max_cores");
            user.show = rs.getString("str_show");
            user.show_min_cores = rs.getInt("int_show_min_cores");
            user.show_max_cores = rs.getInt("int_show_max_cores");
            user.activate = rs.getBoolean("b_activate");
            user.priority_weight = rs.getInt("int_priority_weight");
            user.error_weight = rs.getInt("int_error_weight");
            user.submit_time_weight = rs.getInt("int_submit_time_weight");
            return user;
        }
    };
    @Override
    public void createUser(UserEntity user) {
        getJdbcTemplate().update(
                "INSERT INTO " +
                        "opencue_user " +
                        "(pk_name,b_admin,int_job_priority,int_job_max_cores,str_show," +
                        "int_show_min_cores,int_show_max_cores,b_activate,int_priority_weight," +
                        "int_error_weight,int_submit_time_weight) " +
                        "VALUES " +
                        "(?,?,?,?,?,?,?,?,?,?,?)",
                user.name, user.admin, user.job_priority, user.job_max_cores, user.show,
                user.show_min_cores, user.show_max_cores, user.activate, user.priority_weight,
                user.error_weight, user.submit_time_weight
        );
    }

    @Override
    public UserEntity getUserInfo(String name) {
        String getUserInfoQuery = "SELECT * FROM opencue_user WHERE pk_name = ?";
        return getJdbcTemplate().queryForObject(getUserInfoQuery,USER_MAPPER,name);
    }

    @Override
    public void deleteUser(String name) {
        getJdbcTemplate().update(
                "UPDATE opencue_user SET b_activate = false WHERE pk_name = ?", name);
    }

    @Override
    public void updateUserInfo(UserEntity user) {
        getJdbcTemplate().update(
                "UPDATE opencue_user SET b_admin=?, int_job_priority=?, int_job_max_cores=?," +
                        " str_show=?, int_show_min_cores=?, int_show_max_cores=?, b_activate=?," +
                        " int_priority_weight=?, int_error_weight=?, int_submit_time_weight=? " +
                        "WHERE pk_name = ?",
                user.admin, user.job_priority, user.job_max_cores, user.show, user.show_min_cores,
                user.show_max_cores, user.activate, user.priority_weight, user.error_weight,
                user.submit_time_weight, user.name);
    }
}
