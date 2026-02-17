#include <iostream>
#include <zmq.hpp>
#include <string>
#include "objects_3D.pb.h"

class CameraSubscriber
{
public:
    explicit CameraSubscriber(const std::string& address);

    // blockierend: wartet auf nächste Nachricht
    bool receive(Objects3D_msg& out_msg);

private:
    zmq::context_t context_;
    zmq::socket_t socket_;
};

CameraSubscriber::CameraSubscriber(const std::string& address)
    : context_(1),
      socket_(context_, zmq::socket_type::sub)
{
    // Alle Nachrichten abonnieren
    socket_.set(zmq::sockopt::subscribe, "");

    socket_.connect(address);
}

bool CameraSubscriber::receive(Objects3D_msg& out_msg)
{
    zmq::message_t msg;

    try {
        auto res = socket_.recv(msg, zmq::recv_flags::none);
        if (!res) {
            return false;
        }
    }
    catch (const zmq::error_t& e) {
        std::cerr << "ZeroMQ recv error: " << e.what() << std::endl;
        return false;
    }

    if (msg.size() == 0)
        return false;

    return out_msg.ParseFromArray(msg.data(), msg.size());
}


int main()
{
    CameraSubscriber sub("tcp://localhost:5555");

    while (true) {
        Objects3D_msg list;
        if (sub.receive(list)) {
            std::cout << "Received " << list.objects_size()
                      << " objects" << std::endl;
        }
    }
}
