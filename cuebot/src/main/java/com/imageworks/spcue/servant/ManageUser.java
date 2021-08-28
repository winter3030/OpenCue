package com.imageworks.spcue.servant;

import com.imageworks.spcue.UserEntity;
import com.imageworks.spcue.grpc.opencueUser.OpencueUserInterfaceGrpc;
import com.imageworks.spcue.grpc.opencueUser.UserCreateRequest;
import com.imageworks.spcue.grpc.opencueUser.UserCreateResponse;
import com.imageworks.spcue.grpc.opencueUser.UserGetRequest;
import com.imageworks.spcue.grpc.opencueUser.UserGetResponse;
import com.imageworks.spcue.grpc.opencueUser.User;
import com.imageworks.spcue.service.AdminManager;
import com.imageworks.spcue.service.Whiteboard;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;

import org.apache.log4j.Logger;

//處理來自user端的grpc請求與回應
public class ManageUser extends OpencueUserInterfaceGrpc.OpencueUserInterfaceImplBase{
    private static final Logger logger = Logger.getLogger(ManageUser.class);
    private AdminManager adminManager; //處理請求
    private Whiteboard whiteboard; //處理回應

    @Override
    public void create(UserCreateRequest request, StreamObserver<UserCreateResponse> responseObserver) {
        try {
            User grpcUser = request.getUser();
            UserEntity user = new UserEntity();
            user.name = grpcUser.getName();
            user.admin = grpcUser.getAdmin();
            user.job_priority = grpcUser.getJobPriority();
            user.job_max_cores = grpcUser.getJobMaxCores();
            user.show = grpcUser.getShow();
            user.show_min_cores = grpcUser.getShowMinCores();
            user.show_max_cores = grpcUser.getShowMaxCores();
            user.activate = grpcUser.getActivate();
            user.priority_weight = grpcUser.getPriorityWeight();
            user.error_weight = grpcUser.getErrorWeight();
            user.submit_time_weight = grpcUser.getSubmitTimeWeight();
            adminManager.createUser(user);
            responseObserver.onNext(UserCreateResponse.newBuilder()
                    .setState("Successfully created user.")
                    .build());
            responseObserver.onCompleted();
        } catch (Exception e){
            logger.error("Failed to create user.", e);
            responseObserver.onError(Status.INTERNAL
                    .withDescription("Failed to create user: " + e.getMessage())
                    .withCause(e)
                    .asRuntimeException());
        }
    }

    @Override
    public void get(UserGetRequest request, StreamObserver<UserGetResponse> responseObserver) {
        try{
            //logger.error("ManageUser GET");
            responseObserver.onNext(UserGetResponse.newBuilder()
                    .setUser(whiteboard.getUserInfo(request.getName()))
                    .build());
            responseObserver.onCompleted();
        }catch (Exception e){
            logger.error("Failed to get user info.", e);
            responseObserver.onError(Status.INTERNAL
                    .withDescription("Failed to get user info: " + e.getMessage())
                    .withCause(e)
                    .asRuntimeException());
        }
    }

    public AdminManager getAdminManager() {
        return adminManager;
    }

    public void setAdminManager(AdminManager adminManager) {
        this.adminManager = adminManager;
    }

    public Whiteboard getWhiteboard() {
        return whiteboard;
    }

    public void setWhiteboard(Whiteboard whiteboard) {
        this.whiteboard = whiteboard;
    }
}
