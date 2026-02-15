from zorp_lib import patching

folder = "F:/My Files/Applications/Games/Emulators/Gameboy Advance/mGBA-0.8.4-win32"

print("\nApplying patches...")
for path in (
        f"{folder}/Legend of Zelda, The - Oracle of Ages.gbc",
        f"{folder}/Legend of Zelda, The - Oracle of Seasons.gbc",
        ):
    print(path)
    patching.apply_patches(path)

input("Finished.")
