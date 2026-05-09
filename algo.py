import pandas as pd
import numpy as np

# =========================
# Run 4: Jaccard Similarity WITH genre
# =========================

# 1. קריאת הקובץ
file_path = "HW2 nurm table.xlsx"

df = pd.read_excel(file_path)

df = df.copy()

# =========================
# 2. הגדרת העמודות המספריות
# =========================

numeric_features = [
    "bpm",
    "danceability",
    "valence",
    "energy",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness"
]

# =========================
# 3. ניקוי בסיסי
# =========================

# בריצה 4 אנחנו חייבים genre, לכן מורידים שירים בלי genre
df = df.dropna(subset=["Track Name", "Artist Name", "genre"])

# מורידים שירים שחסר להם אחד מהמאפיינים המספריים
df = df.dropna(subset=numeric_features)

# יצירת שם תצוגה לשיר
df["song_display"] = df["Track Name"].astype(str) + " - " + df["Artist Name"].astype(str)

print("Number of songs after cleaning:", len(df))


# =========================
# 4. פונקציה שהופכת שיר ל-tags כולל genre
# =========================

def create_jaccard_tags_with_genre(row):
    tags = []

    # bpm tags
    if row["bpm"] <= 100:
        tags.append("bpm_slow")
    elif row["bpm"] >= 130:
        tags.append("bpm_fast")
    else:
        tags.append("bpm_medium")

    # other numeric features tags
    features_to_tag = [
        "danceability",
        "valence",
        "energy",
        "acousticness",
        "instrumentalness",
        "liveness",
        "speechiness"
    ]

    for feature in features_to_tag:
        value = row[feature]

        if value <= 0.33:
            tags.append(feature + "_low")
        elif value >= 0.66:
            tags.append(feature + "_high")
        else:
            tags.append(feature + "_medium")

    # genre tag
    tags.append("genre_" + str(row["genre"]))

    return tags


# יצירת עמודת tags לכל שיר
df["jaccard_tags_with_genre"] = df.apply(
    create_jaccard_tags_with_genre,
    axis=1
)


# =========================
# 5. פונקציה לחישוב Jaccard בין שתי קבוצות
# =========================

def jaccard_similarity(set_a, set_b):
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))

    if union == 0:
        return 0

    return intersection / union


# =========================
# 6. חישוב הזוגות הכי דומים
# =========================

def get_top_jaccard_pairs_with_genre(df, top_n=20):
    results = []

    n = len(df)

    for i in range(n):
        tags_i = set(df.iloc[i]["jaccard_tags_with_genre"])

        for j in range(i + 1, n):
            tags_j = set(df.iloc[j]["jaccard_tags_with_genre"])

            score = jaccard_similarity(tags_i, tags_j)

            results.append({
                "song_1": df.iloc[i]["song_display"],
                "song_2": df.iloc[j]["song_display"],
                "genre_1": df.iloc[i]["genre"],
                "genre_2": df.iloc[j]["genre"],
                "tags_1": ", ".join(df.iloc[i]["jaccard_tags_with_genre"]),
                "tags_2": ", ".join(df.iloc[j]["jaccard_tags_with_genre"]),
                "similarity_score": score
            })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="similarity_score",
        ascending=False
    ).head(top_n)

    return results_df


# =========================
# 7. הרצת ריצה 4
# =========================

top_jaccard_with_genre = get_top_jaccard_pairs_with_genre(
    df,
    top_n=20
)

print("Run 4: Jaccard Similarity WITH genre")

try:
    display(top_jaccard_with_genre)
except NameError:
    print(top_jaccard_with_genre.to_string(index=False))