import pandas as pd
from insta_scraper import scrape_instagram_hashtag
from scoring import compute_score
from config import OUTPUT_CSV

def run_hashtag(tag):
    results = scrape_instagram_hashtag(tag)
    for r in results:
        r['viral_score'] = compute_score(r.get('likes'))
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print("✅ Résultats enregistrés dans", OUTPUT_CSV)
    return df

if __name__ == "__main__":
    run_hashtag("bikini")
