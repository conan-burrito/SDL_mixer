#include <SDL_mixer.h>

#include <iostream>

int main() {
    SDL_version compile_version;
    const SDL_version *link_version=Mix_Linked_Version();
    SDL_MIXER_VERSION(&compile_version);
    std::cout << "compiled with SDL_mixer version: "
              << (int)compile_version.major << "."
              << (int)compile_version.minor << "."
              << (int)compile_version.patch << std::endl;
    std::cout << "running with SDL_mixer version: "
              << (int)link_version->major << "."
              << (int)link_version->minor << "."
              << (int)link_version->patch << std::endl;

    return 0;
}