#include <iostream>
#include <zmq.hpp>
#include <string>
#include <thread>
#include <chrono>
#include "objects_3D.pb.h"

class CameraSubscriber
{
public:
    explicit CameraSubscriber(const std::string& address);

    // blockierend: wartet auf nächste Nachricht
    bool receiveObjectList(Objects3D_msg& out_msg);

private:
    zmq::context_t context_;
    zmq::socket_t socket_;
};

CameraSubscriber::CameraSubscriber(const std::string& address)
    : context_(1),
      socket_(context_, zmq::socket_type::sub)
{
    // Subscribe to "obj_list" topic
    socket_.set(zmq::sockopt::subscribe, "obj_list");

    socket_.connect(address);
}

bool CameraSubscriber::receiveObjectList(Objects3D_msg& out_msg)
{
    zmq::message_t topic_msg;
    zmq::message_t data_msg;

    try {
        // Receive topic first
        auto res_topic = socket_.recv(topic_msg, zmq::recv_flags::none);
        if (!res_topic) {
            return false;
        }
        
        std::string topic(static_cast<char*>(topic_msg.data()), topic_msg.size());
        
        // Receive data second
        auto res_data = socket_.recv(data_msg, zmq::recv_flags::none);
        if (!res_data) {
            return false;
        }
        
        std::cout << "Received topic: " << topic << ", data size: " << data_msg.size() << std::endl;
    }
    catch (const zmq::error_t& e) {
        std::cerr << "ZeroMQ recv error: " << e.what() << std::endl;
        return false;
    }

    if (data_msg.size() == 0)
        return false;

    return out_msg.ParseFromArray(data_msg.data(), data_msg.size());
}


int main()
{
    std::cout << "Connecting to camera publisher on tcp://localhost:5555..." << std::endl;
    CameraSubscriber sub("tcp://localhost:5555");
    
    std::cout << "Waiting for 'obj_list' messages..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));  // ZMQ slow joiner fix

    while (true) {
        Objects3D_msg objects;
        if (sub.receiveObjectList(objects)) {
            std::cout << "Received objects: " << objects.objects_size() << std::endl;
            for (int i = 0; i < objects.objects_size(); ++i) {
                const auto& obj = objects.objects(i);
                std::cout << "[" << i << "] X=" << obj.x()
                          << ", Y=" << obj.y()
                          << ", Z=" << obj.z()
                          << ", vy=" << obj.vy()
                          << ", label=" << obj.label() << std::endl;
            }
        }
    }
}
