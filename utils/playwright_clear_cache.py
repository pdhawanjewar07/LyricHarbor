from pathlib import Path
import shutil

PROFILE = Path("playwright_profile")

SAFE_TO_DELETE = [
    "component_crx_cache",
    "Crashpad",
    "Default/Cache",
    "Default/Code Cache",
    "Default/DawnGraphiteCache",
    "Default/DawnWebGPUCache",
    "Default/GPUCache",
    # "Default/Service Worker/CacheStorage",
    "extensions_crx_cache",
    "GraphiteDawnCache",
    "GrShaderCache",
    "ShaderCache"
]

def clear_playwright_cache():
    for name in SAFE_TO_DELETE:
        path = PROFILE / name
        if path.exists():
            shutil.rmtree(path)
            # print(f"Deleted {path}")
    print("Playwright Cache was safely cleared!")
    return True
    
if __name__ == "__main__":
    clear_playwright_cache()