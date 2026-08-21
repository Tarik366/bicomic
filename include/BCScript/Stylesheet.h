#pragma once

#include <map>
#include <string>
#include <regex>
#include <string_view>
#include <ranges>
#include <cmath>
#include <iomanip>

#include <Magick++.h>

#include "styleConstants.h"
#include <stringOperations.h>

// Turn any "18pt", "10%" like dimensions to pixels to be can processed by imageMagick
int turnToPixels(std::string dimension) {
    std::regex pattern("(\\d+)(\\w+)");

    auto begin = std::sregex_iterator(dimension.begin(), dimension.end(), pattern);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it) {
        const std::smatch& m = *it;

        if (m[2].str() == "px") {
            return std::stoi(m[1].str());
        }
        else if (m[2].str() == "pt") {
            return std::lround(std::stof(m[1].str()) * 1.3333f);
        }
    }
}

class styleSheet
{
public:
    std::string prefix;
    // TODO: Replace with new font system for optimizations
    std::list<std::string> fontFamilies = {};
    int fontSize = 16;
    Magick::Color color = "#000000";
    direction spacing = center;
    int outlineSize = 0;
    Magick::Color outlineColor = Magick::Color(1.0f, 1.0f, 1.0f, 1.0f);

    styleSheet(std::string t_prefix, std::list<std::string> t_fontFamilies, int t_fontSize, Magick::Color t_color, direction t_spacing, int t_outlineSize, Magick::Color t_outlineColor) : prefix{ std::move(t_prefix) }, fontFamilies{ std::move(t_fontFamilies) }, fontSize{ t_fontSize }, color{ std::move(t_color) }, spacing{ t_spacing }, outlineSize{ t_outlineSize }, outlineColor{ std::move(t_outlineColor) } {}

    explicit styleSheet(std::string styleText) {

        auto cascades = readCascading(styleText);

        if (!cascades.empty()) {
            prefix = cascades["prefix"];
            for (const auto subrange : std::views::split(cascades["font"], ", ")) {
                fontFamilies.emplace_back(subrange.begin(), subrange.end());
            }
            fontSize = 16;
            fontSize = turnToPixels(cascades["font-size"]);
            color = cascades["color"];
            spacing = strToDir(cascades["spacing"]);
            outlineSize = turnToPixels(cascades["outline-size"]);

            try {
                Magick::Color parsedColor(cascades["outline-color"]);
            }
            catch (const Magick::Exception& error) {
                std::cerr << "Error parsing color string: " << error.what() << std::endl;
            }

        }
    };

};

std::map<std::string, styleSheet> readStyleTag(std::string styleText) {
    std::map<std::string, styleSheet> result;

    std::regex solvePattern("(\\w+) (?:{([\\s\\S]+?)})");

    auto begin = std::sregex_iterator(styleText.begin(), styleText.end(), solvePattern);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it) {
        const std::smatch& m = *it;
        
        result.emplace(m[1].str(), styleSheet::styleSheet(m[2].str()));
    }

    return result;
}

