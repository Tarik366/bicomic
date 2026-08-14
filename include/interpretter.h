#pragma once

#include <string>
#include <map>
#include <regex>
#include <string_view>
#include <ranges>
#include <Magick++.h>

#include <iostream>

// FIXME: Move this enums to a special file
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

class styleSheet
{
    std::string prefix;
    std::string* fontFamilies;
    int fontSize;
    direction spacing;
    int outlineSize;
    Magick::Color outlineColor;

public:
    styleSheet();
    ~styleSheet();

private:

};

styleSheet::styleSheet()
{
}

styleSheet::~styleSheet()
{
}

std::string trim(const std::string& str) {
    // Removes all whitespaces
    const std::string whitespace = "\t\n\r\f\v";
    const auto strBegin = str.find_first_not_of(whitespace);

    if (strBegin == std::string::npos) return ""; // Only whitespace found

    const auto strEnd = str.find_last_not_of(whitespace);
    const auto strRange = strEnd - strBegin + 1;

    return str.substr(strBegin, strRange);
}

std::string removeComments(std::string styleText) {
    // find all comment delimeters and pop until new-line character
    std::string result;
    std::regex comment("//.*\n");

    return trim(std::regex_replace(styleText, comment, ""));
}

std::map<std::string, std::string> readCascading(std::string styleText) {
    // split text or just use regex, i don't know man
    const std::map<std::string, std::string> result;
    for (const auto line : std::views::split(styleText, ';')) {
        // std::cout << std::views::split(line, ':')[0];
    }
    return result;
}

std::string parseBody(std::string bcscript) {
    std::regex pattern("<header>(?<header>[\s\S]*)</header>[\s\S]*<body>(?<body>[\s\S]*)</body>");
    std::smatch matches;
    if (std::regex_search(bcscript, matches, pattern)) {
        std::cout << matches[4];
    }
}

class Body {
    Body(std::string bodyText) {

    }
};

class Header {
public:
    std::string title;
    textDirection paging;
    textDirection lineDirection;
    textDirection wordingDirection;

    std::map<std::string, styleSheet> styles;

    Header(std::string headerText) {
        std::regex pattern("<(?<tag>\w+)(?:\s+(?<settings>[^>]*))?>(?<content>[\s\S]*?)<\/\k<tag>>");

        std::smatch matches;
        if (std::regex_search(headerText, matches, pattern)) {
            std::cout << matches[4];
        }
    };
};

class BCScript {
    Header header;
    Body body;

    BCScript(std::string bcscript) {
        std::regex pattern("<header>(?<header>[\s\S]*)</header>[\s\S]*<body>(?<body>[\s\S]*)</body>");
        std::smatch matches;
        if (std::regex_search(bcscript, matches, pattern)) {
            header = Header(matches[0].str());
            body = Body(matches[1].str());
        }
    }
};

class Episode
{
private:
    BCScript script;
    // Pageset pages;

};
