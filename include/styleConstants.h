#include <string>

struct Position {
    int x;
    int y;
};

enum textDirection
{
    ltr,
    rtl,
    ttb,
    btt
};

enum direction
{
    left, center, right
};

// String to textDirection
textDirection stringToDirections(std::string dir) {
    if (dir == "ltr") {
        return textDirection::ltr;
    } else if (dir == "rtl") {
        return textDirection::rtl;
    } else if (dir == "ttb") {
        return textDirection::ttb;
    } else if (dir == "btt") {
        return textDirection::btt;
    }
}

direction strToDir(std::string dir) {
    if (dir == "left") {
        return direction::left;
    }
    else if (dir == "center") {
        return direction::center;
    }
    else if (dir == "right") {
        return direction::right;
    }
}