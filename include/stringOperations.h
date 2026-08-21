#pragma once

#include <string>
#include <regex>
#include <string_view>
#include <map>


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
    std::map<std::string, std::string> result;
    std::regex pattern("([\\w|-]+):(?:\\s+)(\\w+);");

    auto begin = std::sregex_iterator(styleText.begin(), styleText.end(), pattern);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it) {
        const std::smatch& m = *it;

        result[m[1].str()] = m[2].str();

        std::cout << m[2].str() << "\n";
    }

    return result;
}

