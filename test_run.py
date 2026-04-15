import config
from fetcher import fetch_data
from screener import screen_stocks
import pprint

def test_fetch_and_screen():
    print("Fetching data for test...")
    # Get a much smaller subset to test quickly
    test_symbols = config.TARGET_SYMBOLS[:5]
    print(f"Test targets: {test_symbols}")
    
    data = fetch_data(test_symbols)
    if not data:
        print("Failed to fetch data.")
        return
        
    print("\nFetch successful. Sample data:")
    pprint.pprint(data)
    
    print("\nApplying screening conditions...")
    candidates = screen_stocks(data)
    
    if not candidates:
        print("No candidates found meeting all the strict criteria.")
    else:
        print(f"Found {len(candidates)} candidates:")
        for cand in candidates:
            print(cand)
            
if __name__ == "__main__":
    test_fetch_and_screen()
