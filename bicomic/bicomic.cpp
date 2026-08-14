// bicomic.cpp: Uygulamanın giriş noktasını tanımlar.
//

#include "bicomic.h"

#include <interpretter.h>
#include <fileManager.h>

using namespace std;

int main()
{
    string exampleText = readTextFile("example.bcs");
    auto cascadian = removeComments(exampleText);

    cout << cascadian << endl;
    return 0;
}
