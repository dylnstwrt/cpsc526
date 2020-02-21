#include <iostream>
#include <string>
#include <map>

using namespace std;

string some_hash(const string& input) {
    string retval = "\x0f\xff\x00";
    for (size_t i = 0; i < input.length(); ++i) {
        retval[0] ^= input[i];
        retval[1] &= input[i];
        retval[2] |= input[i];
    }
    return retval;
}

int main(){
    map<string, string> hashes = map<string, string>();
    // key == hash function output
    // value == input value for hash function

    for (int i = 32; i < 127; i++){         
        for (int j = 32; j < 127; j++ ){
            for (int k = 32; k < 127; k++){
                string input = string({char(i), char(j), char(k)});
                string output = some_hash(input);                  
                if (hashes.count(output) == 1){                     
                    cout << "\"" << input << "\"" << " -> "; 
                    cout << "\"" << output << "\"" << "\n";
                    cout << "\"" << hashes.at(output) << "\"" << " -> "; 
                    cout << "\"" << output << "\"" << "\n";
                    exit(0);
                }
                hashes.emplace(output, input);
            }
        }
    }
}
