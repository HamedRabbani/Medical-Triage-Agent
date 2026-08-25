from infrastructure.rag.rag_factory import (
    create_rag_service,
)


def main():

    rag = create_rag_service()

    queries = [
        "سردرد شدید دارم",
        "درد قفسه سینه دارم",
        "تب و لرز دارم",
        "درد شدید شکم دارم",
        "من ماشینم را دوست دارم",
    ]

    print("=" * 70)
    print("RAG DISTANCE THRESHOLD EVALUATION")
    print("=" * 70)

    for query in queries:

        results = rag.retrieve(
            query=query,
            top_k=3,
            distance_threshold=20,
        )

        print("\nQUERY:", query)
        print("-" * 70)

        if not results:
            print("NO RELEVANT RESULTS")
            continue

        for index, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{index}. "
                f"{result['source']} | "
                f"distance={result['distance']:.4f}"
            )


if __name__ == "__main__":
    main()