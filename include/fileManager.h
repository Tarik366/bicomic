#pragma once

#include <string>

std::string readTextFile(std::string filename) {
	std::string filecont;

	std::fstream fs;
	fs.open(filename);

	if (!fs.is_open()) {
		fs.clear();
		if (std::ifstream is{ filename, std::ios::binary | std::ios::ate }) {
			auto size = is.tellg();
			std::string str(size, '\0'); // construct string to stream size
			is.seekg(0);
			if (is.read(&str[0], size)) {
				filecont = str;
			}
		}
		fs.close();
		return filecont;
	}
}