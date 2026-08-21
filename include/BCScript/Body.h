#pragma once

#include <string>
#include <string_view>
#include <ranges>

#include "styleConstants.h"

struct typeSet {
    std::string line;
    Position positon;

};

class Body {
public:
    // TODO: Add .ass like inline text-rendering

    // Stores the text data with the pointer of the stylesheet
    // TODO: Create an exclusive struct for line
    std::list<std::string> typeSet;

    // Header header;

    Body() {}

    explicit Body(std::string bodyText) {
        for (const auto subrange : std::views::split(bodyText, "\n")) {
            std::string_view line = std::string_view(subrange.begin(), subrange.end());

        }
    }
};
