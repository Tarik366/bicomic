#pragma once

#include <map>
#include <regex>
#include <string>
#include <string_view>
#include <ranges>
#include <Magick++.h>

#include <iostream>

#include <stylesheets.h>

std::string removeComments(std::string styleText) {
    // find all comment delimeters and pop until new-line character
    std::string result;
    std::regex comment("//.*\n");

    return trim(std::regex_replace(styleText, comment, ""));
}

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
            } else if (tag == "order") {
                auto orderings = readCascading(content);

                paging = stringToDirections(orderings["paging"]);
                lineDirection = stringToDirections(orderings["line-direction"]);
                wordingDirection = stringToDirections(orderings["wording-direction"]);
            } else if (tag == "style") {
                styles = readStyleTag(content);
            }

            if (m[SETTINGS].matched) {
                break;
            }

        }
    };
};

struct typeSet {
    std::string line;
    std::vector<int> positon;
};

class Body {
public:
    // TODO: Add .ass like inline text-rendering

    // Stores the text data with the pointer of the stylesheet
    // TODO: Create an exclusive struct for line
    std::list<std::string> typeSet;

    // Header header;

    Body() {}

    explicit Body(std::string bodyText, Header* constructHeader) {
        for (const auto subrange : std::views::split(bodyText, "\n")) {
            std::string_view line = std::string_view(subrange.begin(), subrange.end());
            
        }
    }
};

class BCScript {
    Header header;
    Body body;

    BCScript(std::string bcscript) {
        std::regex pattern("<header>(?<header>[\\s\\S]*)</header>[\\s\\S]*<body>(?<body>[\\s\\S]*)</body>");
        std::smatch matches;
        if (std::regex_search(bcscript, matches, pattern)) {
            header = Header::Header(matches[0].str());
            body = Body::Body(matches[1].str(), &header);
        }
    }
};

std::string parseBody(std::string bcscript) {
    std::regex pattern("<header>([\\s\\S]*)</header>[\\s\\S]*<body>([\\s\\S]*)</body>");
    auto begin = std::sregex_iterator(bcscript.begin(), bcscript.end(), pattern);
    auto end = std::sregex_iterator();


    for (auto it = begin; it != end; ++it) {
        const std::smatch& m = *it;

        Header header = Header::Header(m[1].str());
        Body body = Body::Body(m[2].str(), &header);

    }

    return "";
}

class Episode
{
private:
    // BCScript script;
    // Pageset pages;

};
