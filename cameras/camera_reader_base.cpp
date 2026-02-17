#include "camera_reader_base.hpp"

BaseCameraReader::BaseCameraReader(const std::string& config_file)
    : context_(1),
      socket_(context_, zmq::socket_type::pub) 
{
    loadConfig(config_file);
    socket_.bind("tcp://*:5555");
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

    serial_ = devices[0].get_info(RS2_CAMERA_INFO_SERIAL_NUMBER);

    rs2::config cfg;
    cfg.enable_device(serial_);
    cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
    cfg.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);

    pipeline_.start(cfg);
    running_ = true;

    std::cout << "Pipeline gestartet für Gerät: " << serial_ << "\n";
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
    if (!fs["size_tol"].empty()) fs["size_tol"] >> size_delta_; else size_delta_ = 30.0f;
    if (!fs["orientation_tol"].empty()) fs["orientation_tol"] >> orientation_delta_; else orientation_delta_ = 0.5f;

    canny_thresh_.resize(2);
    if (!fs["canny_thresh1"].empty()) fs["canny_thresh1"] >> canny_thresh_.at(0); else canny_thresh_.at(0) = 50;
    if (!fs["canny_thresh2"].empty()) fs["canny_thresh2"] >> canny_thresh_.at(1); else canny_thresh_.at(1) = 150;

    // Load velocity reference region (optional)
    if (!fs["velocity_region"].empty()) {
        cv::FileNode vreg = fs["velocity_region"];
        velocity_region_x_min_ = (float)vreg["x_min"];
        velocity_region_x_max_ = (float)vreg["x_max"];
        velocity_region_y_min_ = (float)vreg["y_min"];
        velocity_region_y_max_ = (float)vreg["y_max"];
    }

    std::cout << "Config loaded from " << config_file << ": ROI=" << roi_ << " (debug=" << debug_ << ")\n";
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
        o->set_width(obj.width);
        o->set_length(obj.length);
        o->set_height(obj.height);
        o->set_label(obj.label);
    }

    std::string buffer;
    list.SerializeToString(&buffer);

    zmq::message_t msg(buffer.size());
    memcpy(msg.data(), buffer.data(), buffer.size());
    socket_.send(msg, zmq::send_flags::none);
}
