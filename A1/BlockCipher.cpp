#include <string>
#include <vector>

std::vector<uint8_t> get_key(){
};

std::vector<uint8_t> get_IV(){
};

std::string AES_CBC_256_encrypt(std::string message, std::vector<uint8_t> key, std::vector<uint8_t> IV){

};

std::string AES_CBC_256_decrypt(std::string message, std::vector<uint8_t> key, std::vector<uint8_t> IV){

};

std::string encrypt(std::string message)
{
    auto key = get_key();
    auto IV = get_IV();

    std::string ciphertext = std::string();

    for (int i = 0; i < 32; i++)
    {
        ciphertext.append(std::to_string(IV[i]));
    }

    ciphertext.append(AES_CBC_256_encrypt(message, key, IV));
    return ciphertext;
}

std::string decrypt(std::string ciphertext)
{
    auto key = get_key();
    uint8_t IV[32];

    for (int i = 0; i < 32; i++)
    {
        IV[i] = (uint8_t)(ciphertext[i] - '0');
    }

    ciphertext.erase(0, 32);

    return AES_CBC_256_decrypt(ciphertext, key, IV);
}