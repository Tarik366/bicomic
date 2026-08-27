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

		img.annotate("—Çünkü", Magick::Geometry(188, 55, 1326, 369), Magick::CenterGravity);

		img.write("annotated_output.png");

	}
	catch (Exception &error_) {
		std::cout << error_.what() << std::endl;
		return 1;
	}

	return 0;
}