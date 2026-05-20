"""Fallback synthetic Netflix dataset generator.

Runs only when the original CSV cannot be downloaded. Produces ~1500 rows
with realistic column shapes (some missing values, mixed durations, etc.)
so the cleaning and EDA steps in the notebook still have something to chew.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

COUNTRIES = [
    "United States", "India", "United Kingdom", "Canada", "France", "Japan",
    "South Korea", "Spain", "Germany", "Mexico", "Australia", "Brazil",
    "Italy", "Turkey", "Egypt", "Argentina", "Nigeria", "China", "Philippines",
    "Indonesia",
]
RATINGS = ["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "PG", "TV-Y", "TV-Y7", "G", "NR"]
GENRES = [
    "Dramas", "International Movies", "Comedies", "Action & Adventure",
    "Documentaries", "Romantic Movies", "Thrillers", "Horror Movies",
    "Children & Family Movies", "Sci-Fi & Fantasy", "Crime TV Shows",
    "TV Dramas", "TV Comedies", "Stand-Up Comedy", "Anime Series",
    "British TV Shows", "Korean TV Shows", "Reality TV", "Independent Movies",
    "Music & Musicals",
]
DIRECTORS = [
    "Martin Scorsese", "Christopher Nolan", "Anurag Kashyap", "Bong Joon-ho",
    "Greta Gerwig", "Denis Villeneuve", "Hayao Miyazaki", "Spike Lee",
    "Pedro Almodovar", "Mira Nair", "Park Chan-wook", "Ava DuVernay",
]
CAST_POOL = [
    "Tom Hardy", "Viola Davis", "Shah Rukh Khan", "Song Kang-ho",
    "Saoirse Ronan", "Idris Elba", "Penelope Cruz", "Deepika Padukone",
    "Lupita Nyong'o", "Oscar Isaac", "Tilda Swinton", "Mahershala Ali",
    "Florence Pugh", "Riz Ahmed", "Zendaya", "Daniel Kaluuya",
]
TITLE_WORDS_A = [
    "Lost", "Midnight", "Silent", "Crimson", "Hidden", "Eternal", "Broken",
    "Wild", "Frozen", "Velvet", "Iron", "Golden", "Sacred", "Dark", "Bright",
]
TITLE_WORDS_B = [
    "Empire", "Kingdom", "Promise", "Garden", "Storm", "Whisper", "Shadow",
    "Heart", "Legacy", "Code", "Hour", "Memory", "Truth", "Project", "City",
]


def random_date(start=date(2008, 1, 1), end=date(2021, 12, 31)):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def make_row(idx):
    show_type = random.choices(["Movie", "TV Show"], weights=[7, 3])[0]
    title = f"{random.choice(TITLE_WORDS_A)} {random.choice(TITLE_WORDS_B)} {idx}"
    director = random.choice(DIRECTORS) if random.random() > 0.25 else ""
    cast = ", ".join(random.sample(CAST_POOL, k=random.randint(2, 5))) if random.random() > 0.1 else ""
    country = random.choice(COUNTRIES) if random.random() > 0.08 else ""
    added = random_date() if random.random() > 0.03 else None
    release_year = random.randint(1990, 2021)
    rating = random.choice(RATINGS) if random.random() > 0.02 else ""
    if show_type == "Movie":
        duration = f"{random.randint(45, 200)} min"
    else:
        duration = f"{random.randint(1, 9)} Season{'s' if random.random() > 0.4 else ''}"
    listed_in = ", ".join(random.sample(GENRES, k=random.randint(1, 3)))
    description = f"A {show_type.lower()} about {random.choice(['love', 'crime', 'family', 'survival', 'identity', 'power'])} set in {country or 'an unnamed place'}."
    return {
        "show_id": f"s{idx}",
        "type": show_type,
        "title": title,
        "director": director,
        "cast": cast,
        "country": country,
        "date_added": added.strftime("%B %d, %Y") if added else "",
        "release_year": release_year,
        "rating": rating,
        "duration": duration,
        "listed_in": listed_in,
        "description": description,
    }


def main(n=1500, out_path="netflix_titles.csv"):
    rows = [make_row(i) for i in range(1, n + 1)]
    # Inject a handful of duplicate rows so the cleaning step has work to do.
    rows.extend(random.sample(rows, k=20))
    fields = list(rows[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
