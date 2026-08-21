#pragma once

#include <string>
#include <fstream>
#include <sstream>

std::string readTextFile(std::string filename) {
    std::ifstream file("example.bcs");

    if (!file.is_open()) {
        std::cerr << "Failed to open the file.\n";
        return "";
    }

    std::stringstream buffer;
    buffer << file.rdbuf();       // Read the entire file buffer into the stream
	return buffer.str();

}

// TODO: An appropriate file manager?
