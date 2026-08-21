#pragma once

#include "Header.h"
#include "Body.h"

class BCScript {
public:
    Header header;
    Body body;

    BCScript(Header hD, Body bd) : header{ hD }, body{ bd } {}

    BCScript(std::string bcscript) {
        std::regex pattern("<header>([\\s\\S]*)</header>[\\s\\S]*<body>([\\s\\S]*)</body>");
        auto begin = std::sregex_iterator(bcscript.begin(), bcscript.end(), pattern);
        auto end = std::sregex_iterator();

        for (auto it = begin; it != end; ++it) {
            const std::smatch& m = *it;

            Header header = Header::Header(m[1].str());
            Body body = Body::Body(m[2].str());

        }
    }
};