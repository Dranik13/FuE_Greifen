#include "camera_reader_base.hpp"

BaseCameraReader::BaseCameraReader(const std::string& config_file)
    : context_(1),
      socket_(context_, zmq::socket_type::pub) 
{
    loadConfig(config_file);
    std::string bind_addr = "tcp://*:" + std::to_string(zmq_port_);
    socket_.bind(bind_addr);
    std::cout << "ZMQ socket bound to " << bind_addr << "\n";
    initializeRealSense();
}

void BaseCameraReader::initializeRealSense()
{
    rs2::context ctx;
    auto devices = ctx.query_devices();
    if (devices.size() == 0) {
        std::cerr << "Keine RealSense Kamera gefunden\n";
        return;
    }

    bool selected_device_found = false;
    std::string serial;
    for (size_t i = 0; i < devices.size(); ++i) {
        serial = devices[i].get_info(RS2_CAMERA_INFO_SERIAL_NUMBER);
        if (serial == serial_number_) {
            selected_device_found = true;
            break;
        }
    }
    if (!selected_device_found) {
        std::cerr << "Configured camera serial number  '" << serial_number_
                    << "' not found. Available devices:\n";
        for (size_t i = 0; i < devices.size(); ++i) {
            std::cerr << "  [" << i << "] "
                        << devices[i].get_info(RS2_CAMERA_INFO_SERIAL_NUMBER) << "\n";
        }
        return;
    }

    rs2::config cfg;
    cfg.enable_device(serial);
    cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
    cfg.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);

    profile_ = pipeline_.start(cfg);
    running_ = true;

    try {
        for (int i = 0; i < 5; ++i) {
            pipeline_.wait_for_frames(3000);
        }
    } catch (const rs2::error& e) {
        std::cerr << "Warmup warning for device " << serial << ": " << e.what() << "\n";
    }

    std::cout << "Pipeline gestartet für Gerät: " << serial << "\n";
}

void BaseCameraReader::loadConfig(const std::string& config_file)
{
    cv::FileStorage fs(config_file, cv::FileStorage::READ);
    if (!fs.isOpened()) {
        std::cerr << "Config file not found: " << config_file << "\n";
        return;
    }

    // read simple scalar with defaults
    if (!fs["debug"].empty()) fs["debug"] >> debug_; else debug_ = 0;

    // ROI may be absent for some cameras; provide a safe default
    cv::FileNode fn = fs["roi"];
    if (!fn.empty()) {
        int x = 0, y = 0, w = 0, h = 0;
        fn["x"] >> x;
        fn["y"] >> y;
        fn["width"] >> w;
        fn["height"] >> h;
        roi_ = cv::Rect(x, y, w, h);
    } else {
        roi_ = cv::Rect(0, 0, 0, 0); // indicates "no ROI"; subclasses should handle
    }

    if (!fs["conveyor_z_dist"].empty()) fs["conveyor_z_dist"] >> conveyor_z_dist_; else conveyor_z_dist_ = 0;
    if (!fs["min_obj_height"].empty()) fs["min_obj_height"] >> min_obj_height_; else min_obj_height_ = 0;
    if (!fs["z_offset"].empty()) fs["z_offset"] >> z_offset_; else z_offset_ = 0;

    cv::FileNode ref = fs["ref_pt"];
    if (!ref.empty()) {
        ref["x"] >> ref_pt_.x;
        ref["y"] >> ref_pt_.y;
    } else {
        ref_pt_ = cv::Point2i(0, 0);
    }

    if (!fs["pos_tol"].empty()) fs["pos_tol"] >> pos_delta_; else pos_delta_ = 30.0f;
    if (!fs["orientation_tol"].empty()) fs["orientation_tol"] >> orientation_delta_; else orientation_delta_ = 0.5f;

    canny_thresh_.resize(2);
    if (!fs["canny_thresh1"].empty()) fs["canny_thresh1"] >> canny_thresh_.at(0); else canny_thresh_.at(0) = 50;
    if (!fs["canny_thresh2"].empty()) fs["canny_thresh2"] >> canny_thresh_.at(1); else canny_thresh_.at(1) = 150;

    if (!fs["zmq_port"].empty()) fs["zmq_port"] >> zmq_port_; else zmq_port_ = 5555;
    if (!fs["serial_number"].empty()) {
        cv::FileNode serial_node = fs["serial_number"];
        if (serial_node.isString()) {
            serial_node >> serial_number_;
        } else if (serial_node.isInt() || serial_node.isReal()) {
            double serial_numeric = 0.0;
            serial_node >> serial_numeric;
            serial_number_ = std::to_string(static_cast<unsigned long long>(serial_numeric + 0.5));
        }
    }

    if (!fs["max_obj_height_mm"].empty()) fs["max_obj_height_mm"] >> max_obj_height_mm_;
    if (!fs["min_contour_area"].empty()) fs["min_contour_area"] >> min_contour_area_;
    if (!fs["search_area_y_min"].empty()) fs["search_area_y_min"] >> search_area_y_min_;
    if (!fs["search_area_y_max"].empty()) fs["search_area_y_max"] >> search_area_y_max_;
    if (!fs["x_scale"].empty()) fs["x_scale"] >> x_scale_; else x_scale_ = 1.0f;
    if (!fs["y_scale"].empty()) fs["y_scale"] >> y_scale_; else y_scale_ = 1.0f;
    if (!fs["x_offset_mm"].empty()) fs["x_offset_mm"] >> x_offset_mm_; else x_offset_mm_ = 0.0f;
    if (!fs["y_offset_mm"].empty()) fs["y_offset_mm"] >> y_offset_mm_; else y_offset_mm_ = 0.0f;

    cv::Mat T;
    if (!fs["T_cam_to_board"].empty()){
        fs["T_cam_to_board"] >> T;
        for (int r = 0; r < 4; ++r)
            for (int c = 0; c < 4; ++c)
                T_cam_to_belt_(r, c) = T.at<double>(r, c);
        std::cout << "Loaded T_cam_to_board from config:\n" << T_cam_to_belt_ << "\n";
    }

    std::cout << "Config loaded from " << config_file << ": ROI=" << roi_
              << " (debug=" << debug_ << ", zmq_port=" << zmq_port_
              << "', serial_number=" << serial_number_ << ""
              << ", x_scale=" << x_scale_ << ", y_scale=" << y_scale_
              << ", x_offset_mm=" << x_offset_mm_ << ", y_offset_mm=" << y_offset_mm_
              << ")\n";
}

cv::Point3f BaseCameraReader::computeCenter(const std::vector<cv::Point3f>& corners)
{
    cv::Point3f c(0.f, 0.f, 0.f);
    for (const auto& p : corners) {
        c.x += p.x;
        c.y += p.y;
        c.z += p.z;
    }
    float n = static_cast<float>(corners.size());
    return cv::Point3f(c.x / n, c.y / n, c.z / n);
}

float BaseCameraReader::computeOrientation2D(const std::vector<cv::Point3f>& corners)
{
    const cv::Point3f& p0 = corners[0];
    const cv::Point3f& p1 = corners[1];
    float dx = p1.x - p0.x;
    float dy = p1.y - p0.y;
    return std::atan2(dy, dx);
}

bool BaseCameraReader::checkIfObjIsInList(const Object3D& new_obj, size_t& id)
{
    id = 0;
    for (const auto& obj : obj_list_)
    {
        float dx = std::abs(obj.x - new_obj.x);
        float dy = std::abs(obj.y - new_obj.y);
        float dz = std::abs(obj.z - new_obj.z);

        if (dx > pos_delta_ || dy > pos_delta_ || dz > pos_delta_)
        {
            id++;
            continue;
        }
        return true;
    }
    return false;
}

void BaseCameraReader::sendObjList()
{
    Objects3D_msg list;

    for (const auto& obj : obj_list_) {
        auto* o = list.add_objects();
        o->set_x(obj.x);
        o->set_y(obj.y);
        o->set_z(obj.z);
        o->set_orientation(obj.orientation);
        o->set_vy(obj.vy);
        o->set_width(obj.width);
        o->set_length(obj.length);
        o->set_height(obj.height);
        o->set_label(obj.label);
        o->set_id(obj.id);
    }

    std::string buffer;
    list.SerializeToString(&buffer);

    // Send with "obj_list" topic prefix
    std::string topic = "obj_list";
    zmq::message_t topic_msg(topic.data(), topic.size());
    zmq::message_t data_msg(buffer.data(), buffer.size());
    
    socket_.send(topic_msg, zmq::send_flags::sndmore);
    socket_.send(data_msg, zmq::send_flags::none);
}

void BaseCameraReader::sendCoordinates(float &x, float &y, float &z)
{
    Object3D_msg obj_msg;
    obj_msg.set_x(x);
    obj_msg.set_y(y);
    obj_msg.set_z(z);

    std::string buffer;
    obj_msg.SerializeToString(&buffer);

    // Send with "coordinates" topic prefix
    std::string topic = "coordinates";
    zmq::message_t topic_msg(topic.data(), topic.size());
    zmq::message_t data_msg(buffer.data(), buffer.size());
    
    socket_.send(topic_msg, zmq::send_flags::sndmore);
    socket_.send(data_msg, zmq::send_flags::none);
}