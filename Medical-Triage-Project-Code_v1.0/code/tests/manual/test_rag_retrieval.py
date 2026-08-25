from infrastructure.rag.rag_factory import create_rag_service


def main():
    rag = create_rag_service()

    queries = [
        "سردرد شدید دارم",
        "I have severe headache",
        "درد قفسه سینه دارم",
        "تب و لرز دارم",
        "درد شدید شکم دارم",
        "من ماشینم را دوست دارم",
    ]

    print("=" * 70)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 70)

    for query in queries:
        print("\nQUERY:", query)
        print("-" * 50)

        results = rag.retrieve(
            query=query,
            top_k=3,
        )

        for index, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{index}. "
                f"Source: {result['source']} | "
                f"Distance: {result['distance']}"
            )


if __name__ == "__main__":
    main()