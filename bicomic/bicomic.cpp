// bicomic.cpp: Uygulamanın giriş noktasını tanımlar.
//

#include "bicomic.h"

#include <interpretter.h>
#include <fileManager.h>

#ifdef _WIN32
#include <windows.h>
#endif // _WIN32

using namespace std;

int main()
{
#if _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif // _WIN32

    string exampleText = readTextFile("./example.bcs");
    auto cascadian = removeComments(exampleText);

    auto parsed = parseBody(cascadian);

    cout << parsed << endl;
    return 0;
}
