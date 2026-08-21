#pragma once

#include "BCScript/BCScript.h"

class Episode
{
public:
	Episode();
	~Episode();

private:
	BCScript TypesettingScript;
	std::list<std::string> images;
};

Episode::Episode()
{
}

Episode::~Episode()
{
}
