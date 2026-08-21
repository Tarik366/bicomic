#pragma once

#include "Stylesheet.h"

#include <Magick++.h>

class Header {
public:
    std::string title;
    textDirection paging = ltr;
    textDirection lineDirection = ttb;
    textDirection wordingDirection = ltr;

    std::map<std::string, styleSheet> styles;

    Header() {}

    explicit Header(std::string headerText) {
        // Grup 1 = tag, Grup 2 = settings (opsiyonel), Grup 3 = content
        std::regex pattern("<(?:(\\w+))(?:\\s+(?:([^>]*)))?>(?:([\\s\\S]*?))</\\1>");

        enum Group { TAG = 1, SETTINGS = 2, CONTENT = 3 };

        auto begin = std::sregex_iterator(headerText.begin(), headerText.end(), pattern);
        auto end = std::sregex_iterator();

        for (auto it = begin; it != end; ++it) {
            const std::smatch& m = *it;

            std::string tag = m[TAG].str();
            std::string content = m[CONTENT].str();

            // TODO: Must be rewritten to be more human-friendly readable form
            if (tag == "title") {
                title = content;
            }
            else if (tag == "order") {
                auto orderings = readCascading(content);

                paging = stringToDirections(orderings["paging"]);
                lineDirection = stringToDirections(orderings["line-direction"]);
                wordingDirection = stringToDirections(orderings["wording-direction"]);
            }
            else if (tag == "style") {
                styles = readStyleTag(content);
            }

            if (m[SETTINGS].matched) {
                break;
            }

        }
    };
};