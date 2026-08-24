#pragma once

#include <Magick++.h>

#include <iostream>

using namespace Magick;

// Debug Method
int Test(int argc, char** argv) {
	std::cout << "Starting ImageMagick" << std::endl;
	MagickPlusPlusGenesis(*argv = nullptr);
	std::cout << "ImageMagick started" << std::endl;

	Image img;

	try {
		img.read("test.jpg");

		img.font("Arial");
		img.fontPointsize(26);
		img.fillColor("black");

		img.annotate("Hello World from C++", Magick::Geometry(200, 50, 1410, 300), Magick::CenterGravity);

		img.write("annotated_output.png");

	}
	catch (Exception &error_) {
		std::cout << error_.what() << std::endl;
		return 1;
	}

	return 0;
}