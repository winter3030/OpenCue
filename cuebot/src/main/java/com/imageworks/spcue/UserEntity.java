package com.imageworks.spcue;

public class UserEntity extends Entity{

    public boolean admin;
    public int job_priority;
    public int job_max_cores;
    public String show;
    public int show_min_cores;
    public int show_max_cores;
    public boolean activate;
    public int priority_weight;
    public int error_weight;
    public int submit_time_weight;

}
