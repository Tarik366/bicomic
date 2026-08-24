#pragma once

#include "BCScript/BCScript.h"
#include <Magick++.h>


class Episode
{
public:
	Episode(BCScript, std::list<Magick::Image>);
	~Episode();

private:
	BCScript TypesettingScript;
	std::list<Magick::Image> PageSet;
};

Episode::Episode(BCScript tss, std::list<Magick::Image> ps) : TypesettingScript{ tss }, PageSet{ps}
{
}

Episode::~Episode()
{
}
