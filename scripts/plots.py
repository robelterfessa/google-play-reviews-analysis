import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_plots(input_path, output_dir="figures"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path)

    # 1) Rating distribution per bank
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="rating", hue="bank")
    plt.title("Rating distribution per bank")
    plt.xlabel("Rating (stars)")
    plt.ylabel("Count")
    plt.legend(title="Bank")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "rating_distribution_per_bank.png"))
    plt.close()

    # 2) Sentiment label counts per bank
    plt.figure(figsize=(8, 5))
    sns.countplot(
        data=df,
        x="sentiment_label",
        hue="bank",
        order=["negative", "neutral", "positive"]
    )
    plt.title("Sentiment labels per bank")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.legend(title="Bank")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sentiment_labels_per_bank.png"))
    plt.close()

    # 3) Average rating per bank
    avg_rating = df.groupby("bank")["rating"].mean().reset_index()

    plt.figure(figsize=(6, 4))
    sns.barplot(data=avg_rating, x="bank", y="rating")
    plt.title("Average rating per bank")
    plt.xlabel("Bank")
    plt.ylabel("Average rating")
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "average_rating_per_bank.png"))
    plt.close()

    print(f"Plots saved in {output_dir}/")

if __name__ == "__main__":
    make_plots("data/reviews_with_sentiment.csv")
