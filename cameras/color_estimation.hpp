#include <array>
#include <cmath>

enum class ColorClass : int {
    Red = 0,
    Yellow,
    Green,
    Blue,
    White,
    Black,
    Unknown,
    Count
};

ColorClass classifyHSV(const cv::Vec3b& hsv)
{
    const int h = hsv[0];
    const int s = hsv[1];
    const int v = hsv[2];

    if (v < 45) return ColorClass::Black;
    if (s < 35 && v > 170) return ColorClass::White;

    // OpenCV HSV hue range is [0, 179].
    if (h <= 10 || h >= 170) return ColorClass::Red;
    if (h <= 35) return ColorClass::Yellow;
    if (h <= 85) return ColorClass::Green;
    if (h <= 135) return ColorClass::Blue;

    return ColorClass::Unknown;
}

const char* colorClassToLabel(ColorClass c)
{
    switch (c) {
        case ColorClass::Red: return "red";
        case ColorClass::Yellow: return "yellow";
        case ColorClass::Green: return "green";
        case ColorClass::Blue: return "blue";
        case ColorClass::White: return "white";
        case ColorClass::Black: return "black";
        default: return "unknown";
    }
}

std::string estimateObjectColorLabel(
    const cv::Mat& hsv_img,
    const std::vector<cv::Point>& contour,
    const cv::Point& center_roi,
    int patch_radius_px = 2)
{
    std::array<int, static_cast<size_t>(ColorClass::Count)> votes{};
    votes.fill(0);

    const cv::Rect bounds(0, 0, hsv_img.cols, hsv_img.rows);

    for (int y = center_roi.y - patch_radius_px; y <= center_roi.y + patch_radius_px; ++y) {
        for (int x = center_roi.x - patch_radius_px; x <= center_roi.x + patch_radius_px; ++x) {
            if (!bounds.contains(cv::Point(x, y))) continue;
            if (cv::pointPolygonTest(contour, cv::Point2f(static_cast<float>(x), static_cast<float>(y)), false) < 0.0) continue;

            const ColorClass c = classifyHSV(hsv_img.at<cv::Vec3b>(y, x));
            votes[static_cast<size_t>(c)]++;
        }
    }

    // Fallback to exact center pixel if no patch pixel landed inside contour.
    if (std::all_of(votes.begin(), votes.end(), [](int v) { return v == 0; })) {
        const int cx = std::clamp(center_roi.x, 0, hsv_img.cols - 1);
        const int cy = std::clamp(center_roi.y, 0, hsv_img.rows - 1);
        const ColorClass c = classifyHSV(hsv_img.at<cv::Vec3b>(cy, cx));
        return colorClassToLabel(c);
    }

    size_t best_idx = static_cast<size_t>(ColorClass::Unknown);
    int best_votes = -1;
    for (size_t i = 0; i < votes.size(); ++i) {
        if (votes[i] > best_votes) {
            best_votes = votes[i];
            best_idx = i;
        }
    }

    return colorClassToLabel(static_cast<ColorClass>(best_idx));
}